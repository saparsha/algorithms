# algorithms

A growing library of small, self-contained algorithm and utility implementations in Python.

Every entry is a single file that stands on its own: no third-party dependencies, no
shared framework, no imports between modules. Each one carries a short docstring
explaining what it does and a block of assertions that exercise it. If you can read the
file top to bottom, you have the whole thing.

The point is not to replace the standard library — `bisect`, `heapq` and `collections`
already do most of this better. The point is to have a readable reference
implementation of each idea in one place.

## Layout

| Directory | Contents |
| --- | --- |
| `algorithms/arrays/` | Sequence manipulation, sliding windows, two-pointer techniques |
| `algorithms/bits/` | Bit-twiddling and bitmask enumeration |
| `algorithms/dp/` | Dynamic programming: knapsack, subsequences, path counting |
| `algorithms/graphs/` | Traversal, shortest paths, spanning trees, connectivity |
| `algorithms/math/` | Number theory, combinatorics, basic statistics |
| `algorithms/misc/` | General-purpose utilities that fit nowhere else |
| `algorithms/search/` | Binary search and its many disguises |
| `algorithms/sorting/` | Comparison sorts, distribution sorts, selection, partitioning |
| `algorithms/strings/` | Pattern matching, edit distance, parsing |
| `algorithms/structures/` | Stacks, queues, trees, tries, heaps, caches |

## Running the tests

Each file is executable and checks itself:

```sh
python3 algorithms/search/binary_search.py
```

To run everything at once:

```sh
python3 run_tests.py
```

The runner executes every module as a subprocess and reports any that fail. It exits
non-zero if anything breaks, so it works as a pre-commit or CI check.

## Conventions

- Python 3.8+, standard library only.
- One idea per file; the filename matches the primary function or class.
- Functions do not mutate their arguments unless the name says so.
- Edge cases — empty input, single elements, absent values — are covered by the
  assertions rather than described in prose.
