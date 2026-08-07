"""Hamming Distance

Count differing positions between two equal-length sequences.
"""

def hamming(a, b):
    if len(a) != len(b):
        raise ValueError("lengths differ")
    return sum(x != y for x, y in zip(a, b))


if __name__ == "__main__":
    assert hamming("karolin", "kathrin") == 3
    assert hamming("", "") == 0
    print("hamming-distance: ok")
