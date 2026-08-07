# algorithms

A library of 150 self-contained algorithm implementations, and a harness that
checks whether they do what they claim.

The implementations are the ordinary part. The interesting part is `verify/`,
which treats them as subjects rather than as the product: it measures the growth
curve of every one and fails the build when the measured complexity is not the
declared one, tests them against properties rather than examples, searches for
the inputs that make each sort behave at its worst, and measures where the
asymptotically better algorithm actually starts winning.

```sh
python -m verify all          # everything; non-zero exit on a real failure
python -m verify report       # the same, written to docs/VERIFICATION.md
python3 run_tests.py          # the 150 modules' own assertions
```

The current report is committed at **[docs/VERIFICATION.md](docs/VERIFICATION.md)**.

---

## What the harness does

### 1. Empirical complexity verification

Every subject declares the complexity its implementation claims. The harness
runs it across geometrically increasing inputs, fits each candidate growth model
to the measured times, and reports which one actually describes the data.

```
complexity  105 subjects  EXPECTED=5  AMBIGUOUS=1  NEIGHBOUR=10  MATCH=89
```

Three things make the measurement worth trusting:

- **Setup is never timed.** Inputs are rebuilt before every repeat, outside the
  clock. Several subjects sort in place, and reusing one input would time a
  sorted array on the second repeat and report the wrong curve entirely.
- **Minimum, not mean.** Wall-clock noise is one-sided — scheduling, page faults
  and GC only ever make a run slower — so the minimum of k repeats is the best
  estimate of the true cost. Averaging folds interference into the signal.
- **Sizes grow until the timer stops being the bottleneck.** Runs below 50µs are
  discarded: at that scale quantisation error picks whichever model the jitter
  favours.

The verdict is deliberately not binary. `NEIGHBOUR` covers pairs that
measurement cannot separate — O(n) and O(n log n) differ by a factor of log n,
which is 6 to 14 across the sizes used here and sits inside the noise as often
as outside it. Failing a build on that would make the check noise-driven, and a
noise-driven check gets ignored. `MISMATCH` means a genuinely different shape,
and that fails.

**The finding worth reading the report for:** five subjects are correct under
textbook analysis and wrong in Python.

| subject | declared | measured |
| --- | --- | --- |
| `fib` | O(log n) | O(n²) |
| `factorial` | O(n) | O(n²) |
| `catalan` | O(n²) | O(n³) |
| `climb_stairs` | O(n) | O(n²) |
| `product_except_self` | O(n) | O(n³) |

Complexity analysis assumes arithmetic costs O(1). Python's integers are
arbitrary-precision, so it does not. Fast-doubling `fib` really does perform
O(log n) multiplications — but the n-th Fibonacci number has O(n) digits, so
each of those multiplications is on an enormous integer. The claim and the
measurement are both right; they are counting different things.

`product_except_self` is the one nobody expects. It looks like an unremarkable
two-pass linear scan, and it is — until you notice the running product of n
values has O(n log n) bits.

### 2. Property-based testing, with shrinking

The assertions inside each module are examples: they pin behaviour the author
already thought of. Properties state something that must hold for *every* input,
and the runner goes looking for inputs where it does not.

58 properties across the library. The ones worth naming:

- Every sort is **ordered**, a **permutation** of its input, **idempotent**, and
  **agrees with `sorted()`** — kept as four separate claims so a failure says
  which invariant broke. Ordered-but-not-a-permutation is a very different bug
  from the reverse.
- `levenshtein` satisfies the three obligations of a **metric**: identity,
  symmetry, and the triangle inequality.
- `lower_bound` **is** the insertion point — everything below it strictly less,
  everything from it greater or equal.
- `fenwick_tree` and `segment_tree` agree with naive recomputation over **every**
  sub-range, not a sampled few.
- Round trips are involutions: `rle`, `roman`, `to_base`, `caesar`,
  `reverse_bits`.

Shrinking is what makes this practical. A failure on
`[773, 12, 918, 4, 331, 88, 12, 605]` tells you almost nothing; the same failure
shrunk to `[0, 0]` usually tells you the bug. The tester is ~80 lines and has no
dependencies — `hypothesis` does this better, but the shrinking is the part
actually worth showing.

### 3. Adversarial input search

Average-case timing flatters an algorithm. What matters is what an adversary, or
an unlucky data distribution, can provoke.

Comparisons are counted **exactly** rather than timed: `Counted` wraps an integer
and increments a counter on every ordering operation, so the algorithms are
measured without being modified. No instrumentation in the implementations, no
profiler overhead, and a number that is identical on every machine.

Inputs come from a fixed battery of known-bad shapes *and* from a hill-climbing
search that starts from a random permutation and keeps any swap that costs more
comparisons.

At n=64, where log2(64!) = 296 is the floor for any comparison sort and
n(n−1)/2 = 2016 is what a quadratic sort costs:

| sort | random | sorted | reversed | organ_pipe | searched worst |
| --- | ---: | ---: | ---: | ---: | ---: |
| `merge_sort` | 300 | 192 | 192 | 223 | 321 |
| `quick_sort` | 634 | 527 | 571 | **883** | 814 |
| `insertion_sort` | 1156 | **63** | **2016** | 1055 | 1831 |
| `selection_sort` | 2016 | 2016 | 2016 | 2016 | 2016 |
| `heap_sort` | 575 | 593 | 525 | 590 | 601 |
| `bubble_sort` | 1971 | **63** | 2016 | 2016 | 2016 |

- **`merge_sort` comes within 1.4% of the information-theoretic bound** on random
  input — 300 comparisons against a floor of 296. There is almost nothing left
  to win.
- **`selection_sort` is input-oblivious**: exactly 2016 comparisons on every
  pattern, and the search finds nothing worse. Predictable and unimprovable in
  equal measure.
- **`insertion_sort` spans 32×** on input order alone, 63 to 2016.
- **`quick_sort`'s worst battery input is organ-pipe**, not reversed — a direct
  consequence of its median-of-three pivot.
- For `merge_sort` and `heap_sort` the search found inputs worse than anything in
  the battery. That is the argument for searching rather than quoting known-bad
  patterns: it optimises against *this* implementation's decisions.

### 4. Crossover measurement

Complexity classes describe behaviour as n approaches infinity. Nothing anyone
runs is at infinity.

| n | `insertion_sort` | `merge_sort` | `quick_sort` | `builtin_sorted` |
| ---: | ---: | ---: | ---: | ---: |
| 16 | 3.1µs | 8.2µs | 5.8µs | 0.6µs |
| 64 | 33.8µs | 42.5µs | 26.3µs | 2.7µs |
| 128 | 143.9µs | 93.5µs | 57.9µs | 6.3µs |
| 2048 | 52988µs | 2163µs | 1632µs | 140µs |

- **`merge_sort` does not overtake `insertion_sort` until n = 128.** Below that,
  the O(n²) algorithm wins on constant factors — which is why real sorts switch
  to insertion sort for small partitions.
- **`python_in` beats `binary_search` up to n = 256.** A C loop doing O(n) work
  beats interpreted arithmetic doing O(log n) work over most practical sizes.
- **`quickselect` loses to `sorted(xs)[k]` until n = 16384**, despite being O(n)
  against O(n log n), for the same reason.
- `builtin_sorted` is 12× faster than the best implementation here at n=2048.
  It is in the table as the floor: it shows how much of the gap is algorithmic
  and how much is simply the interpreter.

---

## Layout

```
algorithms/          150 modules across 10 categories, each self-checking
verify/
  measure.py         adaptive timing, growth-model fitting, verdicts
  subjects.py        105 subjects: declared complexity + input generator
  properties.py      property tester with shrinking, and the properties
  adversarial.py     comparison counting, input battery, hill-climbing search
  crossover.py       where the better algorithm starts winning
  report.py          aggregation and rendering
  cli.py             complexity / properties / adversarial / crossover / report
tests/               27 tests for the harness itself
docs/VERIFICATION.md generated report
```

Every module under `algorithms/` is executable and asserts its own behaviour:

```sh
python3 algorithms/search/binary_search.py
```

## Verifying the verifier

A harness that makes claims about other code needs checking against code whose
behaviour is not in question. `tests/` does that:

- The fitter is run against functions whose complexity is true by construction —
  a loop that runs exactly n times is O(n), and if the fitter disagrees, the
  fitter is wrong.
- The property tester is run against a **deliberately planted bug** — a sort that
  corrupts its output only when the input contains duplicates — and asserted to
  both find it and shrink the counterexample to three elements or fewer.
- The comparison counter is checked against hand-calculated values: insertion
  sort on sorted input performs exactly n−1 comparisons; selection sort performs
  exactly n(n−1)/2 on every input.
- Crossover detection is fed synthetic timings, including a curve that crosses
  once and then crosses back, which must **not** be reported.

## Known limits

- **Coverage is partial**: 105 of the 150 modules have subjects. The rest need
  bespoke setup, or have a true complexity no closed-form model here expresses
  (`permutations` is O(n!·n)).
- **The measured complexity is the complexity of the generator's input
  distribution**, not the worst case. `longest_palindrome` measures O(n) on
  random text because palindromes there are tiny, and O(n²) on a repeated
  character. Both subjects are registered, which is the honest way to show it.
- **Timings are machine-specific.** The classifications are stable; the
  microseconds are not.
- An early version measured `is_balanced` at 3µs for n=32768 — because random
  bracket strings are almost never balanced, so it was timing the early-exit
  path. The generators now produce inputs that reach the end. Worth stating
  because it is the easiest way to build a benchmark that measures nothing.
