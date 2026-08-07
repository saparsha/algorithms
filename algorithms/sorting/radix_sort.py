"""Radix Sort

Least-significant-digit base-256 sort for non-negative integers.
"""

def radix_sort(xs):
    xs = list(xs)
    if not xs:
        return xs
    shift = 0
    while max(xs) >> shift:
        buckets = [[] for _ in range(256)]
        for x in xs:
            buckets[(x >> shift) & 255].append(x)
        xs = [x for b in buckets for x in b]
        shift += 8
    return xs


if __name__ == "__main__":
    assert radix_sort([300, 1, 70000, 5]) == [1, 5, 300, 70000]
    print("radix-sort: ok")
