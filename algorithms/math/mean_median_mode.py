"""Mean, Median and Mode

The three classical measures of central tendency.
"""

from collections import Counter


def mean(xs):
    return sum(xs) / len(xs)


def median(xs):
    s = sorted(xs)
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2


def mode(xs):
    counts = Counter(xs)
    top = max(counts.values())
    return sorted(k for k, v in counts.items() if v == top)


if __name__ == "__main__":
    assert mean([1, 2, 3]) == 2
    assert median([1, 3, 2, 4]) == 2.5
    assert mode([1, 1, 2, 2, 3]) == [1, 2]
    print("mean-median-mode: ok")
