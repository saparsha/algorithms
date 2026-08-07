"""What gets verified, and the inputs it gets verified on.

Every subject declares the complexity its implementation claims. The claim is
kept here rather than in a decorator on each of the 150 modules for one
reason: a complexity is only meaningful relative to *what is being scaled*.
`counting_sort` is linear when values are bounded by n and quadratic when they
are bounded by n squared; `levenshtein` is quadratic when both strings grow and
linear when only one does. The generator and the claim have to sit next to each
other or the claim means nothing.

Coverage is partial and deliberately so — roughly seventy of the hundred and
fifty modules. The rest either need bespoke setup that would swamp the harness,
or have a true complexity that no closed-form model in `measure.MODELS`
expresses (`permutations` is O(n! · n)).

Some subjects are included *expecting* a mismatch. Textbook analysis assumes
arithmetic costs O(1). Python's integers are arbitrary-precision, so it does
not, and `factorial`, `fib` and `catalan` are here to show the harness noticing.
"""

from __future__ import annotations

import importlib
import random
import string
from dataclasses import dataclass
from typing import Callable, List, Optional

SUBJECTS: List["Subject"] = []


@dataclass
class Subject:
    name: str
    module: str
    attr: str
    complexity: str
    make_args: Callable[[int, random.Random], tuple]
    scaling: str
    category: str = ""
    min_n: int = 64
    max_n: int = 1 << 15
    inner: int = 1          # invocations per timed call, for very fast subjects
    step_mode: str = "double"   # 'increment' for exponential subjects
    call: Optional[Callable] = None
    expect_mismatch: bool = False   # textbook claim assumes O(1) arithmetic

    def resolve(self) -> Callable:
        """The callable to time, honouring `inner`."""
        fn = self.call or getattr(importlib.import_module(self.module), self.attr)
        if self.inner <= 1:
            return fn

        def repeated(*args):
            for _ in range(self.inner):
                fn(*args)

        return repeated


def add(name, module, attr, complexity, make_args, scaling, **kw):
    SUBJECTS.append(
        Subject(
            name=name,
            module=f"algorithms.{module}",
            attr=attr,
            complexity=complexity,
            make_args=make_args,
            scaling=scaling,
            category=module.split(".")[0],
            **kw,
        )
    )


# --------------------------------------------------------------------------
# Input generators
# --------------------------------------------------------------------------

ALPHABET = "abcdefgh"


def ints(n, rng):
    return ([rng.randrange(1_000_000) for _ in range(n)],)


def ints_bounded(n, rng):
    """Values bounded by n — the regime where counting sort is linear."""
    return ([rng.randrange(n) for _ in range(n)],)


def sorted_ints(n, rng):
    xs = sorted(rng.randrange(1_000_000) for _ in range(n))
    return (xs, xs[rng.randrange(n)])


def text(n, rng):
    return ("".join(rng.choice(ALPHABET) for _ in range(n)),)


def two_texts(n, rng):
    return (
        "".join(rng.choice(ALPHABET) for _ in range(n)),
        "".join(rng.choice(ALPHABET) for _ in range(n)),
    )


def text_and_pattern(n, rng):
    body = "".join(rng.choice(ALPHABET) for _ in range(n))
    return (body, body[n // 2 : n // 2 + 8])


def words(n, rng):
    return ([("".join(rng.choice(ALPHABET) for _ in range(6))) for _ in range(n)],)


def graph(n, rng, degree=3, dag=False, weighted=False):
    """Random graph. `dag=True` only ever points forward, so it is acyclic by
    construction rather than by hoping the random edges happen not to close a
    loop."""
    g = {u: [] for u in range(n)}
    for u in range(n):
        for _ in range(degree):
            if dag:
                if u + 1 >= n:
                    continue
                v = rng.randrange(u + 1, n)
            else:
                v = rng.randrange(n)
            if v == u:
                continue
            g[u].append((v, rng.randint(1, 20)) if weighted else v)
    return g


def edge_list(n, rng):
    vertices = list(range(n))
    edges = [
        (rng.randrange(n), rng.randrange(n), rng.randint(1, 20)) for _ in range(n * 2)
    ]
    return vertices, edges


def balanced_brackets(n, rng):
    """A *properly nested* bracket string.

    Random brackets are almost never balanced, so the validator bails out after
    a few characters and the timing measures the early-exit path rather than the
    algorithm. This was measured at 3µs for n=32768 before the fix.
    """
    closing = {"(": ")", "[": "]", "{": "}"}
    stack, out = [], []
    for _ in range(n):
        if stack and (len(out) + len(stack) >= n or rng.random() < 0.5):
            out.append(closing[stack.pop()])
        else:
            ch = rng.choice("([{")
            stack.append(ch)
            out.append(ch)
    out.extend(closing[c] for c in reversed(stack))
    return ("".join(out),)


def isomorphic_pair(n, rng):
    """Two strings that genuinely are isomorphic, so the check runs to the end."""
    mapping = dict(zip("abcdefgh", "stuvwxyz"))
    left = "".join(rng.choice("abcdefgh") for _ in range(n))
    return (left, "".join(mapping[c] for c in left))


def bipartite_graph(n, rng):
    """An actually bipartite graph — a random one is not, and the check knows
    it within a handful of edges."""
    half = max(1, n // 2)
    g = {u: [] for u in range(n)}
    for u in range(half):
        for _ in range(3):
            v = rng.randrange(half, n) if half < n else u
            if v == u:
                continue
            g[u].append(v)
            g[v].append(u)
    return (g,)


def repeated_char(n, rng):
    """The worst case for expand-around-centre: every centre expands fully."""
    return ("a" * n,)


def square_grid(n, rng):
    return ([[rng.randrange(100) for _ in range(n)] for _ in range(n)],)


# --------------------------------------------------------------------------
# sorting
# --------------------------------------------------------------------------

add("merge_sort", "sorting.merge_sort", "merge_sort", "O(n log n)", ints, "list length")
add("quick_sort", "sorting.quick_sort", "quick_sort", "O(n log n)", ints, "list length")
add("heap_sort", "sorting.heap_sort", "heap_sort", "O(n log n)", ints, "list length")
add("insertion_sort", "sorting.insertion_sort", "insertion_sort", "O(n^2)", ints,
    "list length", max_n=4096)
add("selection_sort", "sorting.selection_sort", "selection_sort", "O(n^2)", ints,
    "list length", max_n=4096)
add("bubble_sort", "sorting.bubble_sort", "bubble_sort", "O(n^2)", ints,
    "list length", max_n=2048)
add("counting_sort", "sorting.counting_sort", "counting_sort", "O(n)", ints_bounded,
    "list length, values bounded by n")
add("radix_sort", "sorting.radix_sort", "radix_sort", "O(n)", ints,
    "list length, values below 10^6 so passes are constant")
add("quickselect", "sorting.kth_largest", "quickselect", "O(n)",
    lambda n, rng: (ints(n, rng)[0], n // 2), "list length, k at the median")
add("three_way_partition", "sorting.dutch_flag", "three_way_partition", "O(n)",
    lambda n, rng: (ints_bounded(n, rng)[0], n // 2), "list length")
add("merge_intervals", "sorting.merge_intervals", "merge_intervals", "O(n log n)",
    lambda n, rng: ([(s := rng.randrange(n * 4), s + rng.randrange(50)) for _ in range(n)],),
    "interval count")

# --------------------------------------------------------------------------
# search — sub-microsecond, so each timed call makes `inner` invocations
# --------------------------------------------------------------------------

add("binary_search", "search.binary_search", "binary_search", "O(log n)", sorted_ints,
    "sorted list length", max_n=1 << 19, inner=2000)
add("lower_bound", "search.lower_bound", "lower_bound", "O(log n)", sorted_ints,
    "sorted list length", max_n=1 << 19, inner=2000)
add("upper_bound", "search.upper_bound", "upper_bound", "O(log n)", sorted_ints,
    "sorted list length", max_n=1 << 19, inner=2000)
add("search_rotated", "search.search_rotated", "search_rotated", "O(log n)",
    lambda n, rng: (
        (lambda xs, k: (xs[k:] + xs[:k], xs[rng.randrange(n)]))(
            sorted(rng.randrange(1_000_000) for _ in range(n)), rng.randrange(n)
        )
    ),
    "rotated sorted list length", max_n=1 << 18, inner=2000)
add("find_peak", "search.peak_element", "find_peak", "O(log n)",
    lambda n, rng: (list(range(n)),), "list length", max_n=1 << 19, inner=2000)
add("first_true", "search.binary_search_answer", "first_true", "O(log n)",
    lambda n, rng: (0, n, lambda m: m * m >= n), "search range", max_n=1 << 20, inner=1000)
add("isqrt", "search.sqrt_newton", "isqrt", "O(log n)",
    lambda n, rng: (n,), "the value itself", max_n=1 << 24, inner=2000)
add("ternary_search", "search.ternary_search", "ternary_search", "O(1)",
    lambda n, rng: (lambda t: -((t - 2) ** 2), -float(n), float(n)),
    "interval width; iteration count is fixed at 200 regardless", max_n=1 << 20, inner=20)

# --------------------------------------------------------------------------
# strings
# --------------------------------------------------------------------------

add("is_palindrome", "strings.is_palindrome", "is_palindrome", "O(n)", text, "string length")
add("reverse_words", "strings.reverse_words", "reverse_words", "O(n)",
    lambda n, rng: (" ".join("".join(rng.choice(ALPHABET) for _ in range(5)) for _ in range(n // 6)),),
    "string length", max_n=1 << 18)
add("is_anagram", "strings.anagram_check", "is_anagram", "O(n)", two_texts, "string length")
add("rle_encode", "strings.run_length_encoding", "rle_encode", "O(n)", text, "string length")
add("kmp_search", "strings.kmp_search", "kmp_search", "O(n)", text_and_pattern,
    "text length, pattern fixed at 8")
add("rabin_karp", "strings.rabin_karp", "rabin_karp", "O(n)", text_and_pattern,
    "text length, pattern fixed at 8")
add("longest_unique", "strings.longest_unique_substring", "longest_unique", "O(n)", text,
    "string length")
add("z_function", "strings.z_function", "z_function", "O(n)", text, "string length")
add("is_balanced", "strings.valid_parentheses", "is_balanced", "O(n)",
    balanced_brackets, "string length, properly nested so there is no early exit")
add("is_isomorphic", "strings.is_isomorphic", "is_isomorphic", "O(n)", isomorphic_pair,
    "string length, genuinely isomorphic so there is no early exit")
add("normalise_whitespace", "strings.compress_whitespace", "normalise_whitespace", "O(n)",
    lambda n, rng: ("".join(rng.choice("ab  \t") for _ in range(n)),), "string length")
add("word_frequency", "strings.word_frequency", "word_frequency", "O(n)",
    lambda n, rng: (" ".join(rng.choice(("alpha", "beta", "gamma")) for _ in range(n // 6)),),
    "string length")
add("group_anagrams", "strings.group_anagrams", "group_anagrams", "O(n)", words,
    "word count, each word fixed at 6 characters")
add("caesar", "strings.caesar_cipher", "caesar", "O(n)",
    lambda n, rng: (text(n, rng)[0], 3), "string length")
add("levenshtein", "strings.levenshtein", "levenshtein", "O(n^2)", two_texts,
    "both strings of length n", max_n=2048)
add("similarity", "misc.levenshtein_ratio", "similarity", "O(n^2)", two_texts,
    "both strings of length n", max_n=2048)
# The same function, two input distributions, two different true complexities.
# Expand-around-centre is quadratic in the worst case, but on random text the
# palindromes are tiny and every centre stops almost immediately.
add("longest_palindrome", "strings.longest_palindromic_substring", "longest_palindrome",
    "O(n)", text, "random text; centres collapse immediately, so this is average case",
    max_n=1 << 14)
add("longest_palindrome_worst", "strings.longest_palindromic_substring", "longest_palindrome",
    "O(n^2)", repeated_char, "a single repeated character; every centre expands fully",
    max_n=4096)
add("min_window", "strings.min_window_substring", "min_window", "O(n)",
    lambda n, rng: (text(n, rng)[0], "abc"), "text length, pattern fixed")

# --------------------------------------------------------------------------
# arrays
# --------------------------------------------------------------------------

add("two_sum", "arrays.two_sum", "two_sum", "O(n)",
    lambda n, rng: (ints(n, rng)[0], 1_999_999), "list length")
add("max_subarray", "arrays.max_subarray", "max_subarray", "O(n)", ints, "list length")
add("rotate", "arrays.rotate_array", "rotate", "O(n)",
    lambda n, rng: (ints(n, rng)[0], n // 3), "list length")
# Declared O(n) because it makes 2n multiplications. It is not: the running
# product of n values has O(n log n) bits, so each multiplication gets steadily
# more expensive. The least obvious instance of the arbitrary-precision effect
# in the whole registry.
add("product_except_self", "arrays.product_except_self", "product_except_self", "O(n)",
    ints_bounded, "list length; the accumulated product grows without bound",
    expect_mismatch=True)
add("move_zeroes", "arrays.move_zeroes", "move_zeroes", "O(n)", ints_bounded, "list length")
add("dedupe", "arrays.dedupe_stable", "dedupe", "O(n)", ints, "list length")
add("majority", "arrays.majority_element", "majority", "O(n)", ints, "list length")
add("window_max", "arrays.sliding_window_max", "window_max", "O(n)",
    lambda n, rng: (ints(n, rng)[0], 16), "list length, window fixed at 16")
add("trap", "arrays.trapping_rain_water", "trap", "O(n)", ints_bounded, "list length")
add("max_area", "arrays.container_most_water", "max_area", "O(n)", ints_bounded, "list length")
add("longest_consecutive", "arrays.longest_consecutive", "longest_consecutive", "O(n)",
    ints_bounded, "list length")
add("chunk", "arrays.chunk_list", "chunk", "O(n)",
    lambda n, rng: (ints(n, rng)[0], 8), "list length")
add("flatten", "arrays.flatten_nested", "flatten", "O(n)",
    lambda n, rng: ([[i, [i + 1]] for i in range(n // 2)],), "leaf count")
add("prefix_sum_build", "arrays.prefix_sums", "PrefixSum", "O(n)", ints, "list length")
add("binary_gap", "arrays.binary_gap", "binary_gap", "O(log n)",
    lambda n, rng: (n,), "the value itself", max_n=1 << 24, inner=2000)
add("transpose", "arrays.transpose", "transpose", "O(n^2)", square_grid,
    "square matrix of side n", max_n=1024)

# --------------------------------------------------------------------------
# math — the arbitrary-precision cases are here on purpose
# --------------------------------------------------------------------------

add("gcd", "math.gcd_lcm", "gcd", "O(log n)",
    lambda n, rng: (n, rng.randrange(1, n)), "operand magnitude",
    max_n=1 << 24, inner=2000)
add("primes_below", "math.sieve_eratosthenes", "primes_below", "O(n)",
    lambda n, rng: (n,), "the limit; true cost is n log log n, which no model here expresses",
    max_n=1 << 20)
add("power_mod", "math.power_mod", "power_mod", "O(log n)",
    lambda n, rng: (rng.randrange(2, 1000), n, 1_000_003), "exponent magnitude",
    max_n=1 << 24, inner=1000)
add("to_base", "math.base_convert", "to_base", "O(log n)",
    lambda n, rng: (n, 7), "the value itself", max_n=1 << 24, inner=2000)
add("digital_root", "math.digits_sum", "digital_root", "O(1)",
    lambda n, rng: (n,), "the value itself", max_n=1 << 24, inner=5000)
add("pascal", "math.pascal_triangle", "pascal", "O(n^2)",
    lambda n, rng: (n,), "row count", max_n=1024)
add("factorial", "math.factorial", "factorial", "O(n)",
    lambda n, rng: (n,), "the value; declared O(n) assuming O(1) multiplication",
    max_n=8192, expect_mismatch=True)
add("fib", "math.fibonacci", "fib", "O(log n)",
    lambda n, rng: (n,), "the index; declared O(log n) assuming O(1) arithmetic",
    max_n=1 << 18, inner=20, expect_mismatch=True)
add("catalan", "dp.catalan", "catalan", "O(n^2)",
    lambda n, rng: (n,), "the index; declared O(n^2) assuming O(1) multiplication",
    max_n=2048, expect_mismatch=True)

# --------------------------------------------------------------------------
# dp
# --------------------------------------------------------------------------

add("coin_change", "dp.coin_change", "coin_change", "O(n)",
    lambda n, rng: ([1, 5, 12, 19], n), "target amount, coin set fixed")
add("knapsack", "dp.knapsack", "knapsack", "O(n^2)",
    lambda n, rng: ([(rng.randint(1, 20), rng.randint(1, 50)) for _ in range(n)], n),
    "item count and capacity both n", max_n=2048)
add("lis_length", "dp.lis", "lis_length", "O(n log n)", ints, "list length")
add("lcs_length", "dp.lcs", "lcs_length", "O(n^2)", two_texts,
    "both strings of length n", max_n=1024)
add("rob", "dp.house_robber", "rob", "O(n)", ints, "list length")
add("climb_stairs", "dp.climbing_stairs", "climb_stairs", "O(n)",
    lambda n, rng: (n,), "step count; result is a Fibonacci number, so digits grow with n",
    max_n=1 << 15, expect_mismatch=True)
add("word_break", "dp.word_break", "word_break", "O(n^2)",
    lambda n, rng: (text(n, rng)[0], ["a", "b", "ab", "abc", "cd", "d"]),
    "string length", max_n=2048)
add("unique_paths", "dp.unique_paths", "unique_paths", "O(n^2)",
    lambda n, rng: (n, n), "grid side", max_n=1024)
add("lps_length", "dp.longest_palindromic_subseq", "lps_length", "O(n^2)", text,
    "string length", max_n=1024)
add("min_path_sum", "dp.min_path_sum", "min_path_sum", "O(n^2)", square_grid,
    "grid side", max_n=1024)
add("matrix_chain", "dp.matrix_chain", "matrix_chain", "O(n^3)",
    lambda n, rng: ([rng.randint(5, 50) for _ in range(n + 1)],),
    "matrix count", min_n=8, max_n=192)

# --------------------------------------------------------------------------
# bits
# --------------------------------------------------------------------------

add("popcount", "bits.count_bits", "popcount", "O(log n)",
    lambda n, rng: (n,), "the value; work is proportional to set bits",
    max_n=1 << 24, inner=2000)
add("is_power_of_two", "bits.is_power_of_two", "is_power_of_two", "O(1)",
    lambda n, rng: (n,), "the value itself", max_n=1 << 24, inner=5000)
add("single_number", "bits.single_number", "single_number", "O(n)", ints, "list length")
add("reverse_bits", "bits.swap_bits", "reverse_bits", "O(1)",
    lambda n, rng: (n, 32), "value; width fixed at 32 so the loop count is constant",
    max_n=1 << 24, inner=1000)
add("gray_code", "bits.gray_code", "gray_code", "O(2^n)",
    lambda n, rng: (n,), "bit count", min_n=8, max_n=22, step_mode="increment")
add("subsets", "bits.subsets_bitmask", "subsets", "O(2^n)",
    lambda n, rng: (list(range(n)),), "element count", min_n=8, max_n=22,
    step_mode="increment")

# --------------------------------------------------------------------------
# graphs
# --------------------------------------------------------------------------

add("bfs", "graphs.bfs", "bfs", "O(n)",
    lambda n, rng: (graph(n, rng), 0), "vertex count, out-degree fixed at 3", max_n=1 << 14)
add("dfs", "graphs.dfs", "dfs", "O(n)",
    lambda n, rng: (graph(n, rng), 0), "vertex count, out-degree fixed at 3", max_n=1 << 14)
add("dijkstra", "graphs.dijkstra", "dijkstra", "O(n log n)",
    lambda n, rng: (graph(n, rng, weighted=True), 0),
    "vertex count, out-degree fixed at 3", max_n=1 << 13)
add("topological_sort", "graphs.topological_sort", "topological_sort", "O(n log n)",
    lambda n, rng: (graph(n, rng, dag=True),),
    "vertex count; the initial queue is sorted, hence n log n", max_n=1 << 13)
add("components", "graphs.connected_components", "components", "O(n log n)",
    lambda n, rng: (graph(n, rng),), "vertex count; groups are sorted", max_n=1 << 13)
add("is_bipartite", "graphs.bipartite_check", "is_bipartite", "O(n)", bipartite_graph,
    "vertex count, actually bipartite so the whole graph is explored", max_n=1 << 13)
add("bellman_ford", "graphs.bellman_ford", "bellman_ford", "O(n^2)",
    lambda n, rng: (*edge_list(n, rng), 0), "vertex count with 2n edges", max_n=512)
add("floyd_warshall", "graphs.floyd_warshall", "floyd_warshall", "O(n^3)",
    lambda n, rng: edge_list(n, rng), "vertex count", min_n=8, max_n=192)

# --------------------------------------------------------------------------
# structures — sequences of operations, wrapped so the timed unit is the batch
# --------------------------------------------------------------------------


def _fill(cls_path, method, prepare=None):
    """Build n items into a structure and time the whole batch."""
    module_name, _, attr = cls_path.rpartition(".")

    def run(items):
        cls = getattr(importlib.import_module(f"algorithms.{module_name}"), attr)
        instance = cls(*(prepare(items) if prepare else ()))
        bound = getattr(instance, method)
        for item in items:
            bound(item)
        return instance

    return run


add("trie_insert", "structures.trie", "Trie", "O(n)", words, "word count",
    call=_fill("structures.trie.Trie", "insert"), max_n=1 << 14)
add("lru_put", "structures.lru_cache", "LRUCache", "O(n)",
    lambda n, rng: ([(i, i) for i in range(n)],), "insertion count",
    call=lambda pairs: [
        c.put(k, v)
        for c in [getattr(importlib.import_module("algorithms.structures.lru_cache"), "LRUCache")(256)]
        for k, v in pairs
    ],
    max_n=1 << 14)
add("min_heap_push", "structures.min_heap", "MinHeap", "O(n log n)", ints, "push count",
    call=_fill("structures.min_heap.MinHeap", "push"), max_n=1 << 14)
add("fenwick_add", "structures.fenwick_tree", "FenwickTree", "O(n log n)",
    lambda n, rng: ([(i, rng.randrange(100)) for i in range(n)], n),
    "update count",
    call=lambda updates, size: [
        t.add(i, d)
        for t in [getattr(importlib.import_module("algorithms.structures.fenwick_tree"), "FenwickTree")(size)]
        for i, d in updates
    ],
    max_n=1 << 14)
add("segment_tree_build", "structures.segment_tree", "SegmentTree", "O(n)", ints,
    "value count", max_n=1 << 14)
add("bst_insert", "structures.binary_search_tree", "BST", "O(n log n)", ints,
    "insertion count",
    call=_fill("structures.binary_search_tree.BST", "insert"), max_n=4096)
add("bloom_add", "structures.bloom_filter", "BloomFilter", "O(n)", words, "insertion count",
    call=_fill("structures.bloom_filter.BloomFilter", "add"), max_n=1 << 13)
add("frequency_counter", "structures.ordered_dict_lru", "FrequencyCounter", "O(n)", ints,
    "item count", max_n=1 << 14)

# --------------------------------------------------------------------------
# misc
# --------------------------------------------------------------------------

add("moving_average", "misc.chunked_average", "moving_average", "O(n)",
    lambda n, rng: (ints(n, rng)[0], 16), "list length, window fixed")
add("group_by", "misc.group_by", "group_by", "O(n)",
    lambda n, rng: (list(range(n)), lambda x: x % 7), "item count")
add("runs", "misc.run_length_groups", "runs", "O(n)", ints_bounded, "list length")
add("jaccard", "misc.jaccard", "jaccard", "O(n)",
    lambda n, rng: (list(range(n)), list(range(n // 2, n + n // 2))), "set size")
add("luhn_valid", "misc.luhn_check", "luhn_valid", "O(n)",
    lambda n, rng: ("".join(rng.choice("0123456789") for _ in range(n)),), "digit count")
add("flatten_dict", "misc.flatten_dict", "flatten_dict", "O(n)",
    lambda n, rng: ({str(i): {"a": i, "b": {"c": i}} for i in range(n // 3)},), "leaf count")
add("natural_key", "misc.roman_sort_key", "natural_key", "O(n)",
    lambda n, rng: ("".join(rng.choice("ab123") for _ in range(n)),), "string length")
add("hamming", "misc.hamming_distance", "hamming", "O(n)", two_texts, "string length")
add("batches", "misc.topological_batches", "batches", "O(n log n)",
    lambda n, rng: ({u: ([rng.randrange(u + 1, n)] if u + 1 < n else []) for u in range(n)},),
    "vertex count; levels are sorted", max_n=1 << 13)


def by_name(name: str) -> Optional[Subject]:
    return next((s for s in SUBJECTS if s.name == name), None)


def categories() -> List[str]:
    return sorted({s.category for s in SUBJECTS})
