"""Timing, and fitting a growth curve to what the timer saw.

The claim `O(n log n)` in a docstring is an assertion about the code that
nobody usually checks. This module checks it: run the function across
geometrically increasing inputs, fit every candidate growth model to the
measured times, and report which one actually describes the data.

Three things make the measurement worth trusting:

- **Setup is never timed.** Inputs are rebuilt before each repeat, outside the
  clock. Several subjects sort in place, so reusing one input would time a
  sorted array on the second repeat and report the wrong curve entirely.
- **Minimum, not mean.** Noise on a wall clock is one-sided — scheduling, page
  faults and GC only ever make a run slower. The minimum of k repeats is the
  closest estimate of the true cost; averaging folds interference into the
  signal.
- **Sizes grow until the timer is no longer the bottleneck.** A run of 30µs on
  a clock with ~1µs resolution carries a few percent of quantisation error, and
  fitting through that noise picks whichever model the jitter favours.
"""

from __future__ import annotations

import gc
import math
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

# Below this, timer resolution and interpreter noise dominate the signal.
MIN_USEFUL_SECONDS = 50e-6


@dataclass
class Point:
    n: int
    seconds: float
    repeats: int


# --------------------------------------------------------------------------
# Timing
# --------------------------------------------------------------------------


def time_call(
    call: Callable, make_args: Callable[[], tuple], repeats: int, warmup: bool = True
) -> float:
    """Minimum wall time over `repeats`, with arguments rebuilt each time.

    One untimed call first. Without it the first measured size absorbs import
    resolution, first-touch page faults and CPU frequency ramp, which showed up
    as a smaller input timing slower than a larger one — enough to break the
    monotonicity that crossover detection depends on.
    """
    if warmup:
        call(*make_args())
    best = math.inf
    gc_was_enabled = gc.isenabled()
    gc.disable()
    try:
        for _ in range(repeats):
            args = make_args()          # rebuilt outside the clock
            start = time.perf_counter()
            call(*args)
            elapsed = time.perf_counter() - start
            if elapsed < best:
                best = elapsed
    finally:
        if gc_was_enabled:
            gc.enable()
    return best


def series(
    call: Callable,
    make_args: Callable[[int], tuple],
    start_n: int = 64,
    max_n: int = 1 << 16,
    per_size_budget: float = 0.05,
    min_points: int = 6,
    repeats: int = 3,
    step_mode: str = "double",
) -> List[Point]:
    """Measure across doubling input sizes until a size costs too much.

    Adaptive rather than a fixed size list because the subjects span O(log n)
    to O(2^n): a list large enough to characterise binary search would take
    geological time on bubble sort, and one small enough for bubble sort leaves
    binary search entirely inside timer noise.
    """
    points: List[Point] = []
    n = start_n
    while n <= max_n:
        seconds = time_call(call, lambda: make_args(n), repeats)
        points.append(Point(n=n, seconds=seconds, repeats=repeats))
        # Stop once a single size is expensive, but never before we have enough
        # points to distinguish models.
        if seconds > per_size_budget and len(points) >= min_points:
            break
        # Exponential subjects need additive steps: doubling n squares the work,
        # so a doubling series yields two or three usable points before the
        # budget stops it — too few to fit anything.
        n = n * 2 if step_mode == "double" else n + 1
    return points


# --------------------------------------------------------------------------
# Model fitting
# --------------------------------------------------------------------------

MODELS: Dict[str, Callable[[float], float]] = {
    "O(1)": lambda n: 1.0,
    "O(log n)": lambda n: math.log2(n),
    "O(n)": lambda n: float(n),
    "O(n log n)": lambda n: n * math.log2(n),
    "O(n^2)": lambda n: float(n) ** 2,
    "O(n^3)": lambda n: float(n) ** 3,
    "O(2^n)": lambda n: float(2 ** min(n, 60)),
}

# Pairs that measurement cannot reliably separate over a decade or two of n.
# n log n differs from n by a factor of log n — over n = 64..16384 that is a
# spread of 6 to 14, which sits inside the noise of a Python microbenchmark
# more often than it does outside it.
NEIGHBOURS = {
    ("O(n)", "O(n log n)"),
    ("O(n log n)", "O(n)"),
    ("O(1)", "O(log n)"),
    ("O(log n)", "O(1)"),
}


@dataclass
class Fit:
    best: str
    error: float
    confidence: float               # second-best error / best error, >= 1
    ranked: List[Tuple[str, float]] = field(default_factory=list)
    points_used: int = 0

    @property
    def ambiguous(self) -> bool:
        """Whether the runner-up fits nearly as well as the winner."""
        return self.confidence < 1.25


def _relative_rmse(points: Sequence[Point], model: Callable[[float], float]) -> float:
    """Fit t = c * f(n) through the origin and return relative RMSE.

    Relative rather than absolute, because absolute residuals are dominated by
    the largest n — every model then looks equally good on the small sizes that
    actually discriminate between them.
    """
    numerator = sum(p.seconds * model(p.n) for p in points)
    denominator = sum(model(p.n) ** 2 for p in points)
    if denominator == 0:
        return math.inf
    c = numerator / denominator
    if c <= 0:
        return math.inf
    total = 0.0
    for p in points:
        predicted = c * model(p.n)
        total += ((predicted - p.seconds) / p.seconds) ** 2
    return math.sqrt(total / len(points))


def classify(points: Sequence[Point]) -> Optional[Fit]:
    """Rank growth models against measured times."""
    usable = [p for p in points if p.seconds >= MIN_USEFUL_SECONDS]
    if len(usable) < 3:
        return None

    scored = sorted(
        ((name, _relative_rmse(usable, model)) for name, model in MODELS.items()),
        key=lambda pair: pair[1],
    )
    best_name, best_error = scored[0]
    runner_up_error = scored[1][1] if len(scored) > 1 else math.inf
    confidence = (runner_up_error / best_error) if best_error > 0 else math.inf
    return Fit(
        best=best_name,
        error=best_error,
        confidence=confidence,
        ranked=scored,
        points_used=len(usable),
    )


@dataclass
class Verdict:
    subject: str
    declared: str
    fit: Optional[Fit]
    points: List[Point]
    expect_mismatch: bool = False
    scaling: str = ""

    @property
    def status(self) -> str:
        """MATCH, NEIGHBOUR, AMBIGUOUS, MISMATCH or UNMEASURED.

        `NEIGHBOUR` exists because failing a build over an n-versus-n-log-n
        call would make the check noise-driven and therefore ignored. It is
        reported, not fatal. `MISMATCH` means the measured curve is a different
        shape altogether — that is the finding worth acting on.
        """
        if self.fit is None:
            return "UNMEASURED"
        if self.fit.best == self.declared:
            return "MATCH"
        if self.expect_mismatch:
            # Declared under the textbook assumption that arithmetic is O(1).
            # Python's integers are arbitrary-precision, so it is not, and the
            # divergence is the finding rather than a defect.
            return "EXPECTED"
        if (self.declared, self.fit.best) in NEIGHBOURS:
            return "NEIGHBOUR"
        if self.fit.ambiguous:
            top_two = {name for name, _ in self.fit.ranked[:2]}
            if self.declared in top_two:
                return "AMBIGUOUS"
        return "MISMATCH"

    @property
    def ok(self) -> bool:
        return self.status in ("MATCH", "NEIGHBOUR", "AMBIGUOUS", "EXPECTED")
