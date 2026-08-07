"""Command line entry point for the verification harness.

    python -m verify complexity      empirical O() against declared O()
    python -m verify properties      property-based tests with shrinking
    python -m verify adversarial     worst-case comparison counts
    python -m verify crossover       where the better algorithm starts winning
    python -m verify all             everything, non-zero exit on failure
    python -m verify report          everything, written to docs/VERIFICATION.md

Exit status is non-zero when a property fails or a complexity claim is wrong in
a way that was not declared expected. That is the point: a claim nothing checks
is a comment.
"""

from __future__ import annotations

import argparse
import os
import sys

from . import adversarial, crossover, properties, report
from .subjects import SUBJECTS


def _progress(index, total, name):
    # Carriage-return progress only makes sense on a terminal; piped to a file
    # or a log it produces one very long line.
    if not sys.stderr.isatty():
        return
    sys.stderr.write(f"\r  [{index}/{total}] {name:<28}")
    sys.stderr.flush()
    if index == total:
        sys.stderr.write("\r" + " " * 48 + "\r")


def _subjects(pattern):
    if not pattern:
        return SUBJECTS
    chosen = [s for s in SUBJECTS if pattern in s.name or pattern in s.category]
    if not chosen:
        sys.exit(f"no subjects match {pattern!r}")
    return chosen


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="verify")
    parser.add_argument("command",
                        choices=["complexity", "properties", "adversarial",
                                 "crossover", "all", "report"])
    parser.add_argument("--only", help="restrict to subjects matching this substring")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--trials", type=int, default=200, help="property trials")
    parser.add_argument("--n", type=int, default=64, help="adversarial input size")
    parser.add_argument("--budget", type=float, default=0.05,
                        help="seconds allowed per input size before stopping the series")
    parser.add_argument("--all", action="store_true",
                        help="show matching subjects too, not just the interesting ones")
    parser.add_argument("--out", default="docs/VERIFICATION.md")
    args = parser.parse_args(argv)

    summary = report.Summary()
    want = args.command

    if want in ("complexity", "all", "report"):
        summary.verdicts = report.run_complexity(
            _subjects(args.only), seed=args.seed,
            per_size_budget=args.budget, on_progress=_progress,
        )
    if want in ("properties", "all", "report"):
        summary.properties = properties.run(
            trials=args.trials, seed=args.seed, only=args.only
        )
    if want in ("adversarial", "all", "report"):
        summary.profiles = adversarial.profile(n=args.n, seed=args.seed)
    if want in ("crossover", "all", "report"):
        summary.crossovers = crossover.run(seed=args.seed)

    if want == "report":
        markdown = report.render_markdown(
            summary.verdicts, summary.properties, summary.profiles, summary.crossovers
        )
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(markdown + "\n")
        print(f"wrote {args.out} ({len(markdown.splitlines())} lines)")
    else:
        if summary.verdicts:
            print(report.render_complexity(summary.verdicts, show_all=args.all))
            print()
        if summary.properties:
            print(report.render_properties(summary.properties))
            print()
        if summary.profiles:
            print(report.render_adversarial(summary.profiles))
            print()
        if summary.crossovers:
            print(report.render_crossover(summary.crossovers))

    if not summary.ok:
        for v in summary.unexpected_mismatches:
            measured = v.fit.best if v.fit else "unmeasurable"
            print(f"FAIL {v.subject}: declared {v.declared}, measured {measured}",
                  file=sys.stderr)
        for r in summary.property_failures:
            print(f"FAIL {r.subject}.{r.name}: {r.counterexample!r}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
