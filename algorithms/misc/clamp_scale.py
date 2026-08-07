"""Clamp and Rescale

Constrain a value to a range and map between two ranges.
"""

def clamp(value, low, high):
    return max(low, min(high, value))


def rescale(value, from_range, to_range):
    lo, hi = from_range
    to_lo, to_hi = to_range
    if hi == lo:
        return to_lo
    ratio = (value - lo) / (hi - lo)
    return to_lo + ratio * (to_hi - to_lo)


if __name__ == "__main__":
    assert clamp(15, 0, 10) == 10
    assert rescale(5, (0, 10), (0, 100)) == 50
    print("clamp-scale: ok")
