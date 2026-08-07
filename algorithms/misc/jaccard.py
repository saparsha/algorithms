"""Jaccard Similarity

Intersection over union for two sets.
"""

def jaccard(a, b):
    a, b = set(a), set(b)
    union = a | b
    return 1.0 if not union else len(a & b) / len(union)


if __name__ == "__main__":
    assert jaccard({1, 2, 3}, {2, 3, 4}) == 0.5
    assert jaccard(set(), set()) == 1.0
    print("jaccard: ok")
