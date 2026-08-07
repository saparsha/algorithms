"""Counting Sort

Linear-time sort for small non-negative integer keys.
"""

def counting_sort(xs):
    if not xs:
        return []
    hi = max(xs)
    counts = [0] * (hi + 1)
    for x in xs:
        counts[x] += 1
    out = []
    for value, c in enumerate(counts):
        out.extend([value] * c)
    return out


if __name__ == "__main__":
    assert counting_sort([3, 1, 3, 0]) == [0, 1, 3, 3]
    assert counting_sort([]) == []
    print("counting-sort: ok")
