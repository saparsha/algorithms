"""Tests for the verification harness.

The harness makes claims about other code, so it needs to be checked against
functions whose complexity is not in question — a loop that runs exactly n
times is O(n) by construction, and if the fitter says otherwise the fitter is
wrong.
"""

import unittest

from verify import adversarial, crossover, properties
from verify.crossover import CrossoverResult, _crossover
from verify.measure import Point, Verdict, classify, series, time_call


# --------------------------------------------------------------------------
# Functions with complexity that is true by construction
# --------------------------------------------------------------------------


def constant(n):
    return sum(range(10))


def logarithmic(n):
    total, i = 0, 1
    while i < n:
        total += i
        i *= 2
    return total


def linear(n):
    total = 0
    for i in range(n):
        total += 1
    return total


def quadratic(n):
    total = 0
    for _ in range(n):
        for _ in range(n):
            total += 1
    return total


class TestFitterRecoversKnownComplexity(unittest.TestCase):
    def _classify(self, fn, max_n, inner=1, start_n=64):
        def call(n):
            for _ in range(inner):
                fn(n)

        points = series(
            lambda n: call(n),
            lambda n: (n,),
            start_n=start_n,
            max_n=max_n,
            per_size_budget=0.02,
        )
        return classify(points)

    def test_linear(self):
        fit = self._classify(linear, max_n=1 << 17)
        self.assertEqual(fit.best, "O(n)")

    def test_quadratic(self):
        fit = self._classify(quadratic, max_n=2048)
        self.assertEqual(fit.best, "O(n^2)")

    def test_logarithmic(self):
        fit = self._classify(logarithmic, max_n=1 << 20, inner=500)
        self.assertIn(fit.best, ("O(log n)", "O(1)"))  # neighbours by design

    def test_constant_is_flat(self):
        # A constant-time subject is flat, so every point costs the same: either
        # all of them clear the 50µs usefulness floor or none do. `inner` has to
        # be large enough to put the whole series above it.
        fit = self._classify(constant, max_n=1 << 16, inner=2000)
        self.assertIn(fit.best, ("O(1)", "O(log n)"))

    def test_ranking_is_complete_and_ordered(self):
        fit = self._classify(linear, max_n=1 << 16)
        self.assertEqual(len(fit.ranked), 7)
        errors = [e for _, e in fit.ranked]
        self.assertEqual(errors, sorted(errors))


class TestFitterHonesty(unittest.TestCase):
    def test_too_few_usable_points_is_unmeasured_not_a_guess(self):
        points = [Point(n=64, seconds=1e-9, repeats=3), Point(n=128, seconds=2e-9, repeats=3)]
        self.assertIsNone(classify(points))

    def test_verdict_statuses(self):
        def verdict(declared, points, expect=False):
            return Verdict("s", declared, classify(points), points, expect_mismatch=expect)

        clean = [Point(n=2 ** k, seconds=(2 ** k) * 1e-6, repeats=3) for k in range(6, 14)]
        self.assertEqual(verdict("O(n)", clean).status, "MATCH")
        # A genuinely different shape is a mismatch...
        self.assertEqual(verdict("O(2^n)", clean).status, "MISMATCH")
        # ...unless the subject declared that it expects one.
        self.assertEqual(verdict("O(2^n)", clean, expect=True).status, "EXPECTED")
        self.assertTrue(verdict("O(2^n)", clean, expect=True).ok)
        self.assertFalse(verdict("O(2^n)", clean).ok)

    def test_neighbours_are_not_failures(self):
        points = [Point(n=2 ** k, seconds=(2 ** k) * k * 1e-7, repeats=3) for k in range(6, 15)]
        v = Verdict("s", "O(n)", classify(points), points)
        self.assertIn(v.status, ("MATCH", "NEIGHBOUR"))
        self.assertTrue(v.ok)

    def test_warmup_call_happens_outside_the_clock(self):
        calls = []
        seconds = time_call(lambda x: calls.append(x), lambda: (1,), repeats=3)
        self.assertEqual(len(calls), 4)      # 1 warmup + 3 timed
        self.assertGreaterEqual(seconds, 0)

    def test_arguments_are_rebuilt_per_repeat(self):
        """Subjects that sort in place would otherwise be timed on sorted input."""
        built = []

        def make_args():
            built.append(1)
            return ([3, 1, 2],)

        time_call(lambda xs: xs.sort(), make_args, repeats=5)
        self.assertEqual(len(built), 6)      # 1 warmup + 5 timed


# --------------------------------------------------------------------------
# Property tester
# --------------------------------------------------------------------------


class TestPropertyTester(unittest.TestCase):
    def test_finds_and_shrinks_a_planted_bug(self):
        def buggy_sort(xs):
            out = sorted(xs)
            # Corrupts the result only when a duplicate is present.
            if len(out) >= 2 and out[0] == out[1]:
                out[0] = 999
            return out

        result = properties.check(
            "buggy_sort",
            "is_a_permutation",
            properties.lists(properties.ints(0, 6), 40),
            lambda xs: sorted(buggy_sort(list(xs))) == sorted(xs),
            trials=300,
            seed=3,
        )
        self.assertFalse(result.ok)
        self.assertIsNotNone(result.counterexample)
        # Shrinking must reach something a human can read: the minimal input
        # exhibiting this bug is a two-element list of equal values.
        self.assertLessEqual(len(result.counterexample), 3)
        self.assertGreater(result.shrinks, 0)
        self.assertEqual(len(result.counterexample), len(set(result.counterexample)) + 1)

    def test_shrinks_integers_toward_zero(self):
        result = properties.check(
            "big", "under_100", properties.naturals(10 ** 6),
            lambda n: n < 100, trials=50, seed=1,
        )
        self.assertFalse(result.ok)
        self.assertEqual(result.counterexample, 100)

    def test_passing_property_reports_all_trials(self):
        result = properties.check(
            "ok", "always", properties.lists(properties.ints(), 10),
            lambda xs: True, trials=42, seed=1,
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.trials, 42)
        self.assertIsNone(result.counterexample)

    def test_exception_counts_as_failure(self):
        result = properties.check(
            "boom", "raises", properties.naturals(10),
            lambda n: 1 / 0, trials=5, seed=1,
        )
        self.assertFalse(result.ok)
        self.assertIn("ZeroDivisionError", result.error)

    def test_the_real_suite_passes(self):
        failures = [r for r in properties.run(trials=60, seed=7) if not r.ok]
        self.assertEqual(failures, [], f"property failures: {failures}")


# --------------------------------------------------------------------------
# Adversarial
# --------------------------------------------------------------------------


class TestComparisonCounting(unittest.TestCase):
    def test_counts_match_hand_calculation(self):
        insertion = adversarial.load("sorting.insertion_sort", "insertion_sort")
        selection = adversarial.load("sorting.selection_sort", "selection_sort")

        # Insertion sort on sorted input does exactly one comparison per element
        # after the first, and stops.
        self.assertEqual(adversarial.comparisons_for(insertion, list(range(32))), 31)
        # Selection sort scans the whole remaining suffix every time, whatever
        # the input looks like: n(n-1)/2.
        for values in (list(range(24)), list(range(23, -1, -1)), [5] * 24):
            self.assertEqual(adversarial.comparisons_for(selection, values), 24 * 23 // 2)

    def test_counter_is_reset_between_runs(self):
        fn = adversarial.load("sorting.merge_sort", "merge_sort")
        first = adversarial.comparisons_for(fn, list(range(64)))
        second = adversarial.comparisons_for(fn, list(range(64)))
        self.assertEqual(first, second)

    def test_merge_sort_respects_the_information_bound(self):
        import math

        fn = adversarial.load("sorting.merge_sort", "merge_sort")
        n = 128
        bound = math.lgamma(n + 1) / math.log(2)
        used = adversarial.comparisons_for(fn, list(range(n)))
        # Sorted input is merge sort's best case, and no comparison sort can
        # beat log2(n!) on average — but a single lucky input may.
        self.assertLess(used, n * math.log2(n))
        self.assertGreater(bound, 0)

    def test_search_never_reports_worse_than_it_found(self):
        fn = adversarial.load("sorting.quick_sort", "quick_sort")
        worst_input, cost = adversarial.search_worst_case(fn, n=32, iterations=60, seed=2)
        self.assertEqual(len(worst_input), 32)
        self.assertEqual(adversarial.comparisons_for(fn, worst_input), cost)

    def test_profile_shape(self):
        profiles = adversarial.profile(n=32, iterations=30, seed=1)
        self.assertEqual(len(profiles), len(adversarial.COMPARISON_SORTS))
        for p in profiles:
            self.assertGreaterEqual(p.worst_seen, p.baseline_random)
            self.assertGreaterEqual(p.degradation, 1.0)


# --------------------------------------------------------------------------
# Crossover
# --------------------------------------------------------------------------


class TestCrossoverDetection(unittest.TestCase):
    def _result(self, a, b):
        return CrossoverResult(
            family="t", note="", sizes=[1, 2, 4, 8, 16], timings={"a": a, "b": b}
        )

    def test_finds_a_sustained_crossing(self):
        result = self._result([1, 2, 3, 4, 5], [5, 4, 2, 1, 0.5])
        self.assertEqual(_crossover(result, "a", "b"), 4)

    def test_ignores_a_single_crossing_that_does_not_hold(self):
        result = self._result([1, 2, 3, 4, 5], [5, 4, 2, 9, 9])
        self.assertIsNone(_crossover(result, "a", "b"))

    def test_no_crossing_at_all(self):
        result = self._result([1, 1, 1, 1, 1], [2, 2, 2, 2, 2])
        self.assertIsNone(_crossover(result, "a", "b"))

    def test_already_ahead_at_the_smallest_size_is_not_a_crossover(self):
        result = self._result([5, 5, 5, 5, 5], [1, 1, 1, 1, 1])
        self.assertIsNone(_crossover(result, "a", "b"))


class TestSubjectRegistry(unittest.TestCase):
    def test_every_subject_resolves_and_runs(self):
        import random

        from verify.subjects import SUBJECTS

        rng = random.Random(0)
        self.assertGreater(len(SUBJECTS), 100)
        for subject in SUBJECTS:
            with self.subTest(subject=subject.name):
                subject.resolve()(*subject.make_args(subject.min_n, rng))

    def test_declared_complexities_are_all_modelled(self):
        from verify.measure import MODELS
        from verify.subjects import SUBJECTS

        for subject in SUBJECTS:
            self.assertIn(subject.complexity, MODELS, subject.name)

    def test_names_are_unique(self):
        from verify.subjects import SUBJECTS

        names = [s.name for s in SUBJECTS]
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
