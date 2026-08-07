"""Finding the inputs that make each sort behave at its worst.

Average-case timing flatters an algorithm. What matters operationally is what
an adversary — or an unlucky data distribution — can provoke, and the honest way
to find that is to go looking rather than to quote the textbook worst case.

Comparisons are counted exactly rather than timed. `Counted` wraps an integer
and increments a counter on every ordering operation, so the algorithms are
measured without being modified: no instrumentation in the implementations, no
profiler overhead, and a number that is identical on every machine. Wall time
would conflate the thing being measured with cache behaviour and interpreter
noise.

Two sources of bad inputs:

- **A fixed battery** of the structures known to hurt sorting — already sorted,
  reversed, all-equal, organ pipe, sawtooth.
- **A hill-climbing search** that starts from a random permutation and keeps
  swapping pairs whenever the swap costs more comparisons. It finds inputs no
  fixed battery contains, because it is searching against *this* implementation
  rather than against sorting in general.
"""

from __future__ import annotations

import importlib
import math
import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Sequence, Tuple


class Comparisons:
    """Process-wide comparison counter."""

    count = 0

    @classmethod
    def reset(cls) -> None:
        cls.count = 0


class Counted:
    """An integer that reports every time it is compared.

    Only ordering operations are defined. A sort that reaches for arithmetic —
    `counting_sort` indexing by value, `radix_sort` shifting bits — will raise
    rather than silently report a comparison count that means nothing, which is
    why only the comparison sorts are instrumented below.
    """

    __slots__ = ("value",)

    def __init__(self, value: int):
        self.value = value

    def __lt__(self, other):
        Comparisons.count += 1
        return self.value < other.value

    def __le__(self, other):
        Comparisons.count += 1
        return self.value <= other.value

    def __gt__(self, other):
        Comparisons.count += 1
        return self.value > other.value

    def __ge__(self, other):
        Comparisons.count += 1
        return self.value >= other.value

    def __eq__(self, other):
        Comparisons.count += 1
        return isinstance(other, Counted) and self.value == other.value

    def __ne__(self, other):
        Comparisons.count += 1
        return not (isinstance(other, Counted) and self.value == other.value)

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return repr(self.value)


COMPARISON_SORTS = {
    "merge_sort": ("sorting.merge_sort", "merge_sort"),
    "quick_sort": ("sorting.quick_sort", "quick_sort"),
    "insertion_sort": ("sorting.insertion_sort", "insertion_sort"),
    "selection_sort": ("sorting.selection_sort", "selection_sort"),
    "heap_sort": ("sorting.heap_sort", "heap_sort"),
    "bubble_sort": ("sorting.bubble_sort", "bubble_sort"),
}


def load(path: str, attr: str) -> Callable:
    return getattr(importlib.import_module(f"algorithms.{path}"), attr)


# --------------------------------------------------------------------------
# Input patterns
# --------------------------------------------------------------------------


def pattern_random(n: int, rng: random.Random) -> List[int]:
    xs = list(range(n))
    rng.shuffle(xs)
    return xs


def pattern_sorted(n: int, rng: random.Random) -> List[int]:
    return list(range(n))


def pattern_reversed(n: int, rng: random.Random) -> List[int]:
    return list(range(n - 1, -1, -1))


def pattern_all_equal(n: int, rng: random.Random) -> List[int]:
    return [7] * n


def pattern_organ_pipe(n: int, rng: random.Random) -> List[int]:
    half = n // 2
    return list(range(half)) + list(range(n - half - 1, -1, -1))


def pattern_sawtooth(n: int, rng: random.Random) -> List[int]:
    period = max(2, n // 8)
    return [i % period for i in range(n)]


def pattern_almost_sorted(n: int, rng: random.Random) -> List[int]:
    xs = list(range(n))
    for _ in range(max(1, n // 20)):
        i, j = rng.randrange(n), rng.randrange(n)
        xs[i], xs[j] = xs[j], xs[i]
    return xs


PATTERNS: Dict[str, Callable[[int, random.Random], List[int]]] = {
    "random": pattern_random,
    "sorted": pattern_sorted,
    "reversed": pattern_reversed,
    "all_equal": pattern_all_equal,
    "organ_pipe": pattern_organ_pipe,
    "sawtooth": pattern_sawtooth,
    "almost_sorted": pattern_almost_sorted,
}


# --------------------------------------------------------------------------
# Measurement
# --------------------------------------------------------------------------


def comparisons_for(fn: Callable, values: Sequence[int]) -> int:
    wrapped = [Counted(v) for v in values]
    Comparisons.reset()
    fn(wrapped)
    return Comparisons.count


def search_worst_case(
    fn: Callable, n: int, iterations: int = 400, seed: int = 0
) -> Tuple[List[int], int]:
    """Hill-climb toward the permutation costing the most comparisons.

    Accepts equal-cost swaps as well as improvements, so the search can drift
    across plateaus instead of stalling on the first local maximum. Not a proof
    of the worst case — a lower bound on it, found empirically.
    """
    rng = random.Random(seed)
    current = pattern_random(n, rng)
    best_cost = comparisons_for(fn, current)
    best = current[:]

    for _ in range(iterations):
        candidate = best[:]
        i, j = rng.randrange(n), rng.randrange(n)
        candidate[i], candidate[j] = candidate[j], candidate[i]
        cost = comparisons_for(fn, candidate)
        if cost >= best_cost:
            best, best_cost = candidate, cost
    return best, best_cost


@dataclass
class SortProfile:
    name: str
    n: int
    by_pattern: Dict[str, int] = field(default_factory=dict)
    searched_worst: int = 0
    baseline_random: int = 0

    @property
    def information_bound(self) -> float:
        """log2(n!) — no comparison sort can do better on average."""
        return math.lgamma(self.n + 1) / math.log(2)

    @property
    def quadratic_bound(self) -> int:
        return self.n * (self.n - 1) // 2

    @property
    def worst_seen(self) -> int:
        return max([self.searched_worst, *self.by_pattern.values()])

    @property
    def degradation(self) -> float:
        """Worst input over random input. 1.0 means nothing found hurts it."""
        return self.worst_seen / self.baseline_random if self.baseline_random else 0.0


def profile(n: int = 64, iterations: int = 400, seed: int = 0) -> List[SortProfile]:
    rng = random.Random(seed)
    out: List[SortProfile] = []
    for name, (path, attr) in COMPARISON_SORTS.items():
        fn = load(path, attr)
        result = SortProfile(name=name, n=n)
        for pattern_name, make in PATTERNS.items():
            result.by_pattern[pattern_name] = comparisons_for(fn, make(n, rng))
        result.baseline_random = result.by_pattern["random"]
        _, result.searched_worst = search_worst_case(fn, n, iterations=iterations, seed=seed)
        out.append(result)
    return out
