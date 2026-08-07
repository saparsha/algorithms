"""Kadane's Algorithm

Largest sum of any contiguous subarray, in linear time.
"""

def max_subarray(xs):
    if not xs:
        return 0
    best = cur = xs[0]
    for x in xs[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


if __name__ == "__main__":
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray([-3, -1]) == -1
    print("max-subarray: ok")
