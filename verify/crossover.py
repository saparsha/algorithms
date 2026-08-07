"""Where the asymptotically better algorithm actually starts winning.

Complexity classes describe behaviour as n goes to infinity. Nothing anyone
runs is at infinity. An O(n^2) sort with a tight inner loop beats an O(n log n)
sort with recursion and allocation for every input below some size, and that
size is a measurement, not a derivation — it depends on the constant factors of
this implementation on this interpreter.

Crossovers are found by requiring the faster algorithm to *stay* faster at
every larger size measured, not merely to win once. A single crossing is noise;
a crossing that holds is a property.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from .measure import time_call
from .properties import load


@dataclass
class Family:
    name: str
    members: Dict[str, Callable]
    make_input: Callable[[int, random.Random], tuple]
    sizes: Sequence[int]
    note: str = ""


@dataclass
class CrossoverResult:
    family: str
    note: str
    sizes: List[int]
    timings: Dict[str, List[float]] = field(default_factory=dict)
    crossovers: List[Tuple[str, str, Optional[int]]] = field(default_factory=list)

    def fastest_at(self, index: int) -> str:
        return min(self.timings, key=lambda name: self.timings[name][index])


def _random_ints(n, rng):
    return ([rng.randrange(1_000_000) for _ in range(n)],)


def sorting_family() -> Family:
    return Family(
        name="sorting",
        members={
            "insertion_sort": load("sorting.insertion_sort", "insertion_sort"),
            "selection_sort": load("sorting.selection_sort", "selection_sort"),
            "merge_sort": load("sorting.merge_sort", "merge_sort"),
            "quick_sort": load("sorting.quick_sort", "quick_sort"),
            "heap_sort": load("sorting.heap_sort", "heap_sort"),
            "builtin_sorted": sorted,
        },
        make_input=_random_ints,
        sizes=[4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048],
        note=(
            "builtin_sorted is Timsort implemented in C. It is included as the "
            "floor: it shows how much of the gap between these implementations "
            "is algorithmic and how much is simply the interpreter."
        ),
    )


def selection_family() -> Family:
    quickselect = load("sorting.kth_largest", "quickselect")
    import heapq

    return Family(
        name="median selection",
        members={
            "quickselect": lambda xs: quickselect(xs, len(xs) // 2),
            "sort_then_index": lambda xs: sorted(xs)[len(xs) // 2],
            "heapq_nsmallest": lambda xs: heapq.nsmallest(len(xs) // 2 + 1, xs)[-1],
        },
        make_input=_random_ints,
        sizes=[16, 64, 256, 1024, 4096, 16384],
        note=(
            "Quickselect is O(n) against sorting's O(n log n), but sorting runs "
            "in C. The asymptotics and the measurement disagree over the whole "
            "practical range."
        ),
    )


def membership_family() -> Family:
    binary_search = load("search.binary_search", "binary_search")

    def linear_scan(xs, target):
        for i, x in enumerate(xs):
            if x == target:
                return i
        return None

    def make_input(n, rng):
        xs = sorted(rng.randrange(1_000_000) for _ in range(n))
        # A batch of targets spread across the array rather than one random
        # target. A single lookup is below timer resolution, and taking the
        # minimum over repeats of a single random target measures whichever
        # repeat happened to hit position zero.
        targets = [xs[rng.randrange(n)] for _ in range(200)]
        return (xs, targets)

    def over_targets(fn):
        def run(xs, targets):
            for target in targets:
                fn(xs, target)

        return run

    return Family(
        name="membership",
        members={
            "binary_search": over_targets(binary_search),
            "linear_scan": over_targets(linear_scan),
            "python_in": over_targets(lambda xs, t: t in xs),
        },
        make_input=make_input,
        sizes=[8, 16, 32, 64, 128, 256, 1024, 4096],
        note=(
            "O(log n) against O(n), but `in` is a C loop while binary search is "
            "interpreted arithmetic. Each timing is 200 lookups at positions "
            "spread across the array, so this is average-case, not worst-case."
        ),
    )


def measure_family(family: Family, repeats: int = 5, seed: int = 0) -> CrossoverResult:
    rng = random.Random(seed)
    result = CrossoverResult(family=family.name, note=family.note, sizes=list(family.sizes))

    for name, fn in family.members.items():
        timings = []
        for n in family.sizes:
            # Arguments are rebuilt per repeat inside time_call, which matters
            # here: several of these sort in place.
            seconds = time_call(fn, lambda n=n: family.make_input(n, rng), repeats)
            timings.append(seconds)
        result.timings[name] = timings

    # Both directions: "when does b overtake a" and "when does a overtake b"
    # are different questions, and only one of them has an answer per pair.
    names = list(family.members)
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            result.crossovers.append((a, b, _crossover(result, a, b)))
            result.crossovers.append((b, a, _crossover(result, b, a)))
    return result


def _crossover(result: CrossoverResult, a: str, b: str) -> Optional[int]:
    """Smallest n where b overtakes a and never loses the lead again."""
    ta, tb = result.timings[a], result.timings[b]
    for i in range(len(result.sizes)):
        if tb[i] < ta[i] and all(tb[j] < ta[j] for j in range(i, len(result.sizes))):
            return result.sizes[i] if i > 0 else None  # already ahead at the smallest size
    return None


def run(seed: int = 0) -> List[CrossoverResult]:
    return [
        measure_family(sorting_family(), seed=seed),
        measure_family(selection_family(), seed=seed),
        measure_family(membership_family(), seed=seed),
    ]
