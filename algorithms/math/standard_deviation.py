"""Standard Deviation

Population and sample standard deviation from raw values.
"""

def variance(xs, sample=False):
    n = len(xs)
    if n < 2 and sample:
        raise ValueError("need at least two values")
    m = sum(xs) / n
    return sum((x - m) ** 2 for x in xs) / (n - 1 if sample else n)


def stddev(xs, sample=False):
    return variance(xs, sample) ** 0.5


if __name__ == "__main__":
    assert abs(stddev([2, 4, 4, 4, 5, 5, 7, 9]) - 2.0) < 1e-9
    print("standard-deviation: ok")
