"""Dutch National Flag

Three-way partition of a sequence around a pivot in one pass.
"""

def three_way_partition(xs, pivot):
    xs = list(xs)
    lo, i, hi = 0, 0, len(xs) - 1
    while i <= hi:
        if xs[i] < pivot:
            xs[lo], xs[i] = xs[i], xs[lo]
            lo += 1
            i += 1
        elif xs[i] > pivot:
            xs[hi], xs[i] = xs[i], xs[hi]
            hi -= 1
        else:
            i += 1
    return xs


if __name__ == "__main__":
    assert three_way_partition([2, 0, 1, 2, 0], 1) == [0, 0, 1, 2, 2]
    print("dutch-flag: ok")
