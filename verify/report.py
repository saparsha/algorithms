"""Run the checks and render what they found."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from . import adversarial, crossover, properties
from .measure import Verdict, classify, series
from .subjects import SUBJECTS, Subject

STATUS_ORDER = ["MISMATCH", "UNMEASURED", "EXPECTED", "AMBIGUOUS", "NEIGHBOUR", "MATCH"]


def run_complexity(
    subjects: Optional[Sequence[Subject]] = None,
    seed: int = 0,
    per_size_budget: float = 0.05,
    on_progress=None,
) -> List[Verdict]:
    rng = random.Random(seed)
    out: List[Verdict] = []
    chosen = list(subjects if subjects is not None else SUBJECTS)
    for index, subject in enumerate(chosen, 1):
        if on_progress:
            on_progress(index, len(chosen), subject.name)
        points = series(
            subject.resolve(),
            lambda n, s=subject: s.make_args(n, rng),
            start_n=subject.min_n,
            max_n=subject.max_n,
            per_size_budget=per_size_budget,
            step_mode=subject.step_mode,
        )
        out.append(
            Verdict(
                subject=subject.name,
                declared=subject.complexity,
                fit=classify(points),
                points=points,
                expect_mismatch=subject.expect_mismatch,
                scaling=subject.scaling,
            )
        )
    return out


# --------------------------------------------------------------------------
# Text rendering
# --------------------------------------------------------------------------


def render_complexity(verdicts: Sequence[Verdict], show_all: bool = False) -> str:
    counts: Dict[str, int] = {}
    for v in verdicts:
        counts[v.status] = counts.get(v.status, 0) + 1

    lines = [
        f"complexity  {len(verdicts)} subjects  "
        + "  ".join(f"{s}={counts[s]}" for s in STATUS_ORDER if s in counts),
        "",
    ]
    interesting = [v for v in verdicts if show_all or v.status not in ("MATCH", "NEIGHBOUR")]
    if interesting:
        lines.append(f"  {'subject':<22}{'declared':<12}{'measured':<12}{'conf':>6}  status")
        for v in sorted(interesting, key=lambda v: STATUS_ORDER.index(v.status)):
            measured = v.fit.best if v.fit else "-"
            conf = f"{v.fit.confidence:.1f}" if v.fit else "-"
            lines.append(
                f"  {v.subject:<22}{v.declared:<12}{measured:<12}{conf:>6}  {v.status}"
            )
    return "\n".join(lines)


def render_properties(results: Sequence[properties.PropertyResult]) -> str:
    failures = [r for r in results if not r.ok]
    lines = [
        f"properties  {len(results)} checked, {len(failures)} failing "
        f"({results[0].trials if results else 0} trials each)",
    ]
    for r in failures:
        lines.append(f"  FAIL {r.subject}.{r.name}: {r.error}")
        lines.append(
            f"       minimal counterexample after {r.shrinks} shrinks: {r.counterexample!r}"
        )
    return "\n".join(lines)


def render_adversarial(profiles: Sequence[adversarial.SortProfile]) -> str:
    if not profiles:
        return ""
    n = profiles[0].n
    patterns = list(profiles[0].by_pattern)
    lines = [
        f"adversarial  comparison counts at n={n} "
        f"(information bound log2(n!) = {profiles[0].information_bound:.0f}, "
        f"quadratic bound = {profiles[0].quadratic_bound})",
        "",
        "  " + f"{'sort':<16}" + "".join(f"{p[:9]:>11}" for p in patterns) + f"{'searched':>11}{'ratio':>8}",
    ]
    for p in profiles:
        row = "".join(f"{p.by_pattern[k]:>11}" for k in patterns)
        lines.append(f"  {p.name:<16}{row}{p.searched_worst:>11}{p.degradation:>8.2f}")
    return "\n".join(lines)


def render_crossover(results: Sequence[crossover.CrossoverResult]) -> str:
    lines = []
    for r in results:
        lines.append(f"crossover  {r.family}")
        header = "  " + f"{'n':>7}" + "".join(f"{k[:14]:>16}" for k in r.timings)
        lines.append(header)
        for i, n in enumerate(r.sizes):
            lines.append(
                f"  {n:>7}" + "".join(f"{r.timings[k][i]*1e6:>16.1f}" for k in r.timings)
            )
        found = [(a, b, c) for a, b, c in r.crossovers if c]
        for a, b, c in found:
            lines.append(f"    {b} overtakes {a} at n = {c}")
        if not found:
            lines.append("    no crossover in the measured range")
        lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------


def render_markdown(
    verdicts: Sequence[Verdict],
    prop_results: Sequence[properties.PropertyResult],
    profiles: Sequence[adversarial.SortProfile],
    crossovers: Sequence[crossover.CrossoverResult],
) -> str:
    out: List[str] = []
    add = out.append

    add("# Verification report")
    add("")
    add(
        "Generated by `python -m verify report`. Every figure here is measured on "
        "the machine that ran it — timings will differ on yours, and the "
        "conclusions drawn from them should not."
    )
    add("")

    # -- complexity --------------------------------------------------------
    counts: Dict[str, int] = {}
    for v in verdicts:
        counts[v.status] = counts.get(v.status, 0) + 1
    add("## Complexity")
    add("")
    add(
        f"{len(verdicts)} subjects. "
        + ", ".join(f"**{counts[s]}** {s.lower()}" for s in STATUS_ORDER if s in counts)
        + "."
    )
    add("")
    add(
        "`MATCH` means the measured growth curve is the one the implementation "
        "claims. `NEIGHBOUR` covers the pairs measurement cannot separate over a "
        "couple of decades of n — O(n) against O(n log n) differ by a factor of "
        "log n, which is 6 to 14 across the sizes used here and sits inside the "
        "noise as often as outside it. `EXPECTED` marks claims that are correct "
        "under the textbook assumption of O(1) arithmetic and wrong in Python."
    )
    add("")
    add("| subject | declared | measured | confidence | status | scaling |")
    add("| --- | --- | --- | ---: | --- | --- |")
    for v in sorted(verdicts, key=lambda v: (STATUS_ORDER.index(v.status), v.subject)):
        measured = v.fit.best if v.fit else "—"
        conf = f"{v.fit.confidence:.1f}×" if v.fit else "—"
        add(f"| `{v.subject}` | {v.declared} | {measured} | {conf} | {v.status} | {v.scaling} |")
    add("")

    surprises = [v for v in verdicts if v.status in ("EXPECTED", "MISMATCH")]
    if surprises:
        add("### Where the textbook is wrong about Python")
        add("")
        add(
            "Complexity analysis assumes arithmetic is a constant-time operation. "
            "Python integers are arbitrary-precision, so addition costs time "
            "proportional to the number of digits and multiplication rather more. "
            "Any algorithm whose *result* grows with n therefore has a hidden "
            "factor the textbook analysis omits:"
        )
        add("")
        for v in surprises:
            measured = v.fit.best if v.fit else "—"
            add(f"- **`{v.subject}`** — declared {v.declared}, measured {measured}.")
        add("")
        add(
            "`fib` is the sharpest case. Fast doubling really is O(log n) "
            "*operations*, but the n-th Fibonacci number has O(n) digits, so those "
            "O(log n) multiplications are each on enormous integers. The claim and "
            "the measurement are both right; they are counting different things."
        )
        add("")

    # -- properties --------------------------------------------------------
    failures = [r for r in prop_results if not r.ok]
    add("## Properties")
    add("")
    add(
        f"{len(prop_results)} properties, {len(failures)} failing, "
        f"{prop_results[0].trials if prop_results else 0} generated inputs each."
    )
    add("")
    if failures:
        add("| subject | property | counterexample | shrinks |")
        add("| --- | --- | --- | ---: |")
        for r in failures:
            add(f"| `{r.subject}` | {r.name} | `{r.counterexample!r}` | {r.shrinks} |")
    else:
        add("All properties hold. The interesting ones being asserted:")
        add("")
        add(
            "- every sort is **ordered**, a **permutation** of its input, "
            "**idempotent**, and **agrees with `sorted()`** — kept as four separate "
            "claims so a failure says which invariant broke\n"
            "- `levenshtein` satisfies the three obligations of a **metric**: "
            "identity, symmetry, and the triangle inequality\n"
            "- `lower_bound` **is** the insertion point: everything below it is "
            "strictly less, everything from it is greater or equal\n"
            "- `fenwick_tree` and `segment_tree` agree with naive recomputation "
            "over **every** sub-range, not a sampled few\n"
            "- round trips are involutions: `rle`, `roman`, `to_base`, `caesar`, "
            "`reverse_bits`"
        )
    add("")

    # -- adversarial -------------------------------------------------------
    if profiles:
        n = profiles[0].n
        add("## Adversarial inputs")
        add("")
        add(
            f"Exact comparison counts at n={n}, collected by wrapping each element "
            "in a type that increments a counter when compared — no changes to the "
            "implementations and no profiler overhead. `searched` is the worst "
            "input found by hill-climbing from a random permutation, accepting any "
            "swap that costs more comparisons."
        )
        add("")
        add(
            f"For reference: log2({n}!) = **{profiles[0].information_bound:.0f}** is the "
            f"information-theoretic floor for any comparison sort, and "
            f"n(n−1)/2 = **{profiles[0].quadratic_bound}** is what a quadratic sort costs."
        )
        add("")
        patterns = list(profiles[0].by_pattern)
        add("| sort | " + " | ".join(patterns) + " | searched | worst/random |")
        add("| --- | " + " | ".join("---:" for _ in patterns) + " | ---: | ---: |")
        for p in profiles:
            row = " | ".join(str(p.by_pattern[k]) for k in patterns)
            add(f"| `{p.name}` | {row} | {p.searched_worst} | {p.degradation:.2f}× |")
        add("")
        add("What the table says:")
        add("")
        best = min(profiles, key=lambda p: p.by_pattern["random"])
        excess = best.by_pattern["random"] / best.information_bound - 1
        add(
            f"- **`{best.name}` comes within {excess:.1%} of the "
            "information-theoretic bound** on random input "
            f"({best.by_pattern['random']} comparisons against a floor of "
            f"{best.information_bound:.0f}). There is almost nothing left to win."
        )
        oblivious = [p for p in profiles if len(set(p.by_pattern.values())) == 1]
        for p in oblivious:
            add(
                f"- **`{p.name}` is input-oblivious**: identical count on every "
                "pattern, and hill-climbing finds nothing worse. It always performs "
                "exactly n(n−1)/2 comparisons, which makes it predictable and "
                "unimprovable in equal measure."
            )
        adaptive = [
            p for p in profiles
            if p.by_pattern["sorted"] < p.by_pattern["random"] / 4
        ]
        for p in adaptive:
            add(
                f"- **`{p.name}` is adaptive**: {p.by_pattern['sorted']} comparisons "
                f"on sorted input against {p.by_pattern['reversed']} on reversed — a "
                f"{p.by_pattern['reversed'] / max(1, p.by_pattern['sorted']):.0f}× "
                "spread driven entirely by input order."
            )
        worst_hit = max(profiles, key=lambda p: p.degradation)
        searched_beat_battery = [
            p for p in profiles
            if p.searched_worst > max(p.by_pattern.values())
        ]
        add(
            f"- Hill-climbing hurt **`{worst_hit.name}`** most, finding an input "
            f"{worst_hit.degradation:.2f}× worse than random."
        )
        if searched_beat_battery:
            names = ", ".join(f"`{p.name}`" for p in searched_beat_battery)
            add(
                f"- For {names}, the search found inputs worse than **anything in "
                "the fixed battery**. That is the argument for searching rather "
                "than quoting known-bad patterns: it optimises against this "
                "implementation's specific decisions, not against sorting in "
                "general."
            )
        add("")

    # -- crossover ---------------------------------------------------------
    add("## Crossover points")
    add("")
    add(
        "Where the asymptotically better algorithm actually starts winning. A "
        "crossover is only recorded when the faster algorithm *stays* faster at "
        "every larger size measured — one crossing is noise."
    )
    add("")
    for r in crossovers:
        add(f"### {r.family}")
        add("")
        if r.note:
            add(r.note)
            add("")
        add("| n | " + " | ".join(f"`{k}`" for k in r.timings) + " |")
        add("| ---: | " + " | ".join("---:" for _ in r.timings) + " |")
        for i, n in enumerate(r.sizes):
            add(
                f"| {n} | "
                + " | ".join(f"{r.timings[k][i]*1e6:.1f}µs" for k in r.timings)
                + " |"
            )
        add("")
        found = [(a, b, c) for a, b, c in r.crossovers if c]
        if found:
            for a, b, c in found:
                add(f"- `{b}` overtakes `{a}` at **n = {c}**")
        else:
            add("- no crossover inside the measured range")
        add("")
    return "\n".join(out)


@dataclass
class Summary:
    verdicts: List[Verdict] = field(default_factory=list)
    properties: List[properties.PropertyResult] = field(default_factory=list)
    profiles: List[adversarial.SortProfile] = field(default_factory=list)
    crossovers: List[crossover.CrossoverResult] = field(default_factory=list)

    @property
    def unexpected_mismatches(self) -> List[Verdict]:
        return [v for v in self.verdicts if not v.ok]

    @property
    def property_failures(self) -> List[properties.PropertyResult]:
        return [r for r in self.properties if not r.ok]

    @property
    def ok(self) -> bool:
        return not self.unexpected_mismatches and not self.property_failures
