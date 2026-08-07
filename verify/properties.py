"""A small property-based tester, and the properties worth asserting.

The assertions in each module are examples: they pin behaviour the author
already thought of. Properties are different — they state something that must
hold for *every* input, and the runner goes looking for inputs where it does
not.

Shrinking is what makes the difference practical. A failure on
`[773, 12, 918, 4, 331, 88, 12, 605]` tells you almost nothing; the same failure
shrunk to `[1, 0, 0]` usually tells you the bug. The loop below repeatedly
replaces a failing input with a smaller one that still fails, until no smaller
candidate does.

Written rather than imported (hypothesis does this better) because a dependency
is a poor trade for eighty lines, and because the shrinking is the part actually
worth showing.
"""

from __future__ import annotations

import importlib
import random
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, List, Optional, Sequence

MAX_SHRINK_STEPS = 300


# --------------------------------------------------------------------------
# Generators
# --------------------------------------------------------------------------


@dataclass
class Gen:
    produce: Callable[[random.Random], Any]
    shrink: Callable[[Any], Iterable[Any]]


def _shrink_int(value: int) -> Iterable[int]:
    if value == 0:
        return
    for candidate in (0, value // 2, abs(value) - 1 if value > 0 else value + 1):
        if abs(candidate) < abs(value):
            yield candidate


def ints(lo: int = -1000, hi: int = 1000) -> Gen:
    return Gen(lambda rng: rng.randint(lo, hi), _shrink_int)


def naturals(hi: int = 1000) -> Gen:
    return Gen(lambda rng: rng.randint(0, hi), _shrink_int)


def _shrink_seq(value):
    """Try empty, then halves, then each single deletion, then smaller elements.

    Ordered cheapest-and-most-drastic first: the fastest route to a minimal
    counterexample is usually a big cut that still fails.
    """
    n = len(value)
    if n == 0:
        return
    yield value[:0]
    if n > 1:
        yield value[: n // 2]
        yield value[n // 2 :]
    for i in range(min(n, 40)):
        yield value[:i] + value[i + 1 :]
    if value and isinstance(value[0], int):
        for i in range(min(n, 40)):
            if value[i] != 0:
                yield value[:i] + type(value)([0]) + value[i + 1 :]


def lists(element: Gen, max_len: int = 60) -> Gen:
    def produce(rng):
        return [element.produce(rng) for _ in range(rng.randint(0, max_len))]

    return Gen(produce, _shrink_seq)


def texts(alphabet: str = "abc", max_len: int = 40) -> Gen:
    def produce(rng):
        return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len)))

    def shrink(value):
        n = len(value)
        if n == 0:
            return
        yield ""
        if n > 1:
            yield value[: n // 2]
            yield value[n // 2 :]
        for i in range(min(n, 40)):
            yield value[:i] + value[i + 1 :]

    return Gen(produce, shrink)


def pairs(first: Gen, second: Gen) -> Gen:
    def produce(rng):
        return (first.produce(rng), second.produce(rng))

    def shrink(value):
        a, b = value
        for sa in first.shrink(a):
            yield (sa, b)
        for sb in second.shrink(b):
            yield (a, sb)

    return Gen(produce, shrink)


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------


@dataclass
class PropertyResult:
    subject: str
    name: str
    ok: bool
    trials: int
    counterexample: Any = None
    shrinks: int = 0
    error: str = ""


def _fails(prop: Callable[[Any], bool], value: Any) -> bool:
    try:
        return not prop(value)
    except Exception:
        return True


def _describe_failure(prop: Callable[[Any], bool], value: Any) -> str:
    try:
        return "returned False" if not prop(value) else ""
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


def check(
    subject: str,
    name: str,
    gen: Gen,
    prop: Callable[[Any], bool],
    trials: int = 200,
    seed: int = 0,
) -> PropertyResult:
    rng = random.Random(f"{seed}:{subject}:{name}")
    for trial in range(trials):
        value = gen.produce(rng)
        if not _fails(prop, value):
            continue

        # Found one. Now make it small enough to read.
        current, shrinks = value, 0
        for _ in range(MAX_SHRINK_STEPS):
            for candidate in gen.shrink(current):
                if _fails(prop, candidate):
                    current, shrinks = candidate, shrinks + 1
                    break
            else:
                break
        return PropertyResult(
            subject=subject,
            name=name,
            ok=False,
            trials=trial + 1,
            counterexample=current,
            shrinks=shrinks,
            error=_describe_failure(prop, current),
        )
    return PropertyResult(subject=subject, name=name, ok=True, trials=trials)


# --------------------------------------------------------------------------
# Properties
# --------------------------------------------------------------------------


def load(path: str, attr: str):
    return getattr(importlib.import_module(f"algorithms.{path}"), attr)


SORTS = {
    "merge_sort": ("sorting.merge_sort", "merge_sort"),
    "quick_sort": ("sorting.quick_sort", "quick_sort"),
    "insertion_sort": ("sorting.insertion_sort", "insertion_sort"),
    "selection_sort": ("sorting.selection_sort", "selection_sort"),
    "heap_sort": ("sorting.heap_sort", "heap_sort"),
    "bubble_sort": ("sorting.bubble_sort", "bubble_sort"),
    "counting_sort": ("sorting.counting_sort", "counting_sort"),
    "radix_sort": ("sorting.radix_sort", "radix_sort"),
}


def _sort_properties() -> List[tuple]:
    """Four independent claims per sort.

    `matches_reference` subsumes the others when it passes, but keeping them
    separate means a failure says *which* invariant broke — a result that is
    ordered but not a permutation is a very different bug from the reverse.
    """
    out = []
    for name, (path, attr) in SORTS.items():
        fn = load(path, attr)
        # counting and radix sort require non-negative values.
        gen = lists(naturals(500) if name in ("counting_sort", "radix_sort") else ints())

        out.append((name, "ordered", gen,
                    lambda xs, f=fn: all(a <= b for a, b in zip(f(list(xs)), f(list(xs))[1:]))))
        out.append((name, "is_a_permutation", gen,
                    lambda xs, f=fn: sorted(f(list(xs))) == sorted(xs)))
        out.append((name, "idempotent", gen,
                    lambda xs, f=fn: f(list(f(list(xs)))) == f(list(xs))))
        out.append((name, "matches_reference", gen,
                    lambda xs, f=fn: list(f(list(xs))) == sorted(xs)))
    return out


def _search_properties() -> List[tuple]:
    binary_search = load("search.binary_search", "binary_search")
    lower_bound = load("search.lower_bound", "lower_bound")
    upper_bound = load("search.upper_bound", "upper_bound")
    quickselect = load("sorting.kth_largest", "quickselect")

    sorted_pair = pairs(lists(ints(-50, 50)), ints(-50, 50))

    def found_iff_present(value):
        xs, target = value
        xs = sorted(xs)
        index = binary_search(xs, target)
        if target in xs:
            return index is not None and xs[index] == target
        return index is None

    def bounds_bracket_equal_range(value):
        xs, target = value
        xs = sorted(xs)
        lo, hi = lower_bound(xs, target), upper_bound(xs, target)
        return lo <= hi and xs[lo:hi] == [x for x in xs if x == target]

    def bounds_agree_with_insertion(value):
        xs, target = value
        xs = sorted(xs)
        lo = lower_bound(xs, target)
        return all(x < target for x in xs[:lo]) and all(x >= target for x in xs[lo:])

    def select_matches_sorted(value):
        xs, _ = value
        if not xs:
            return True
        k = len(xs) // 2
        return quickselect(list(xs), k) == sorted(xs)[k]

    return [
        ("binary_search", "found_iff_present", sorted_pair, found_iff_present),
        ("lower_bound", "brackets_equal_range", sorted_pair, bounds_bracket_equal_range),
        ("lower_bound", "is_the_insertion_point", sorted_pair, bounds_agree_with_insertion),
        ("quickselect", "matches_sorted_index", sorted_pair, select_matches_sorted),
    ]


def _roundtrip_properties() -> List[tuple]:
    rle_encode = load("strings.run_length_encoding", "rle_encode")
    rle_decode = load("strings.run_length_encoding", "rle_decode")
    to_base = load("math.base_convert", "to_base")
    to_roman = load("math.roman_numerals", "to_roman")
    from_roman = load("math.roman_numerals", "from_roman")
    caesar = load("strings.caesar_cipher", "caesar")
    reverse_bits = load("bits.swap_bits", "reverse_bits")

    return [
        ("rle", "decode_undoes_encode", texts("aab"),
         lambda s: rle_decode(rle_encode(s)) == s),
        ("to_base", "parses_back", naturals(10 ** 6),
         lambda n: int(to_base(n, 7), 7) == n),
        ("roman", "parses_back", Gen(lambda rng: rng.randint(1, 3999), _shrink_int),
         lambda n: from_roman(to_roman(n)) == n),
        ("caesar", "shift_is_invertible", texts("abcXYZ ,.", 30),
         lambda s: caesar(caesar(s, 7), -7) == s),
        ("reverse_bits", "is_an_involution", naturals((1 << 32) - 1),
         lambda n: reverse_bits(reverse_bits(n, 32), 32) == n),
    ]


def _metric_properties() -> List[tuple]:
    """Levenshtein claims to be a metric; a metric has three obligations."""
    levenshtein = load("strings.levenshtein", "levenshtein")
    triple = Gen(
        lambda rng: tuple(
            "".join(rng.choice("ab") for _ in range(rng.randint(0, 12))) for _ in range(3)
        ),
        lambda t: (
            (t[0][:-1], t[1], t[2]),
            (t[0], t[1][:-1], t[2]),
            (t[0], t[1], t[2][:-1]),
        )
        if all(t)
        else (),
    )
    return [
        ("levenshtein", "identity_of_indiscernibles", triple,
         lambda t: (levenshtein(t[0], t[0]) == 0) and (levenshtein(t[0], t[1]) == 0) == (t[0] == t[1])),
        ("levenshtein", "symmetric", triple,
         lambda t: levenshtein(t[0], t[1]) == levenshtein(t[1], t[0])),
        ("levenshtein", "triangle_inequality", triple,
         lambda t: levenshtein(t[0], t[2]) <= levenshtein(t[0], t[1]) + levenshtein(t[1], t[2])),
    ]


def _brute_force_properties() -> List[tuple]:
    """Compare against a definition that is obviously correct but too slow."""
    max_subarray = load("arrays.max_subarray", "max_subarray")
    window_max = load("arrays.sliding_window_max", "window_max")
    lis_length = load("dp.lis", "lis_length")
    longest_unique = load("strings.longest_unique_substring", "longest_unique")
    gcd = load("math.gcd_lcm", "gcd")
    popcount = load("bits.count_bits", "popcount")
    is_prime = load("math.is_prime", "is_prime")
    dedupe = load("arrays.dedupe_stable", "dedupe")

    def brute_max_subarray(xs):
        if not xs:
            return True
        best = max(
            sum(xs[i:j]) for i in range(len(xs)) for j in range(i + 1, len(xs) + 1)
        )
        return max_subarray(xs) == best

    def brute_window_max(value):
        xs, k = value
        k = max(1, min(k, len(xs))) if xs else 1
        if not xs:
            return True
        expected = [max(xs[i : i + k]) for i in range(len(xs) - k + 1)]
        return window_max(xs, k) == expected

    def brute_lis(xs):
        best = 0
        for mask in range(1 << len(xs)):
            picked = [xs[i] for i in range(len(xs)) if mask >> i & 1]
            if all(a < b for a, b in zip(picked, picked[1:])):
                best = max(best, len(picked))
        return lis_length(xs) == best

    def brute_longest_unique(s):
        best = 0
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                if len(set(s[i:j])) == j - i:
                    best = max(best, j - i)
        return longest_unique(s) == best

    return [
        ("max_subarray", "matches_brute_force", lists(ints(-20, 20), 12), brute_max_subarray),
        ("window_max", "matches_brute_force",
         pairs(lists(ints(-20, 20), 20), naturals(6)), brute_window_max),
        ("lis_length", "matches_brute_force", lists(ints(0, 10), 10), brute_lis),
        ("longest_unique", "matches_brute_force", texts("abc", 12), brute_longest_unique),
        ("gcd", "divides_both_and_pairs_with_lcm",
         pairs(naturals(10 ** 5), naturals(10 ** 5)),
         lambda p: (p[0] % gcd(p[0], p[1]) == 0 and p[1] % gcd(p[0], p[1]) == 0)
         if gcd(p[0], p[1]) else p == (0, 0)),
        ("popcount", "matches_bin_count", naturals(1 << 40),
         lambda n: popcount(n) == bin(n).count("1")),
        ("is_prime", "matches_trial_division", naturals(20000),
         lambda n: is_prime(n) == (n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1)))),
        ("dedupe", "keeps_first_occurrences", lists(ints(0, 8), 30),
         lambda xs: dedupe(xs) == [x for i, x in enumerate(xs) if x not in xs[:i]]),
    ]


def _structure_properties() -> List[tuple]:
    Trie = load("structures.trie", "Trie")
    MinHeap = load("structures.min_heap", "MinHeap")
    FenwickTree = load("structures.fenwick_tree", "FenwickTree")
    SegmentTree = load("structures.segment_tree", "SegmentTree")
    LRUCache = load("structures.lru_cache", "LRUCache")
    topological_sort = load("graphs.topological_sort", "topological_sort")

    word_list = lists(texts("ab", 6), 12)

    def trie_contains_inserted(ws):
        trie = Trie()
        for w in ws:
            trie.insert(w)
        return all(w in trie for w in ws)

    def heap_pops_in_order(xs):
        heap = MinHeap()
        for x in xs:
            heap.push(x)
        return [heap.pop() for _ in range(len(xs))] == sorted(xs)

    def fenwick_matches_naive(xs):
        tree = FenwickTree(len(xs))
        for i, x in enumerate(xs):
            tree.add(i, x)
        return all(
            tree.range_sum(lo, hi) == sum(xs[lo:hi])
            for lo in range(len(xs))
            for hi in range(lo, len(xs) + 1)
        )

    def segment_tree_matches_naive(xs):
        if not xs:
            return True
        tree = SegmentTree(xs)
        return all(
            tree.query(lo, hi) == min(xs[lo:hi])
            for lo in range(len(xs))
            for hi in range(lo + 1, len(xs) + 1)
        )

    def lru_never_exceeds_capacity(xs):
        cache = LRUCache(4)
        for x in xs:
            cache.put(x, x)
        return len(cache._data) <= 4

    def topo_respects_every_edge(xs):
        n = max(2, min(len(xs), 12))
        graph = {i: [j for j in range(i + 1, n) if (i + j) % 3 == 0] for i in range(n)}
        order = topological_sort(graph)
        position = {node: i for i, node in enumerate(order)}
        return all(position[u] < position[v] for u in graph for v in graph[u])

    return [
        ("trie", "contains_what_was_inserted", word_list, trie_contains_inserted),
        ("min_heap", "pops_in_sorted_order", lists(ints(-50, 50), 30), heap_pops_in_order),
        ("fenwick_tree", "matches_naive_prefix_sums", lists(ints(-20, 20), 16),
         fenwick_matches_naive),
        ("segment_tree", "matches_naive_range_min", lists(ints(-20, 20), 16),
         segment_tree_matches_naive),
        ("lru_cache", "never_exceeds_capacity", lists(ints(0, 20), 40),
         lru_never_exceeds_capacity),
        ("topological_sort", "respects_every_edge", lists(ints(0, 5), 12),
         topo_respects_every_edge),
    ]


def all_properties() -> List[tuple]:
    return (
        _sort_properties()
        + _search_properties()
        + _roundtrip_properties()
        + _metric_properties()
        + _brute_force_properties()
        + _structure_properties()
    )


def run(trials: int = 200, seed: int = 0, only: Optional[str] = None) -> List[PropertyResult]:
    results = []
    for subject, name, gen, prop in all_properties():
        if only and only not in subject:
            continue
        results.append(check(subject, name, gen, prop, trials=trials, seed=seed))
    return results
