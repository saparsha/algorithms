"""Longest Increasing Subsequence

Length of the longest strictly increasing subsequence in O(n log n).
"""

from bisect import bisect_left


def lis_length(xs):
    tails = []
    for x in xs:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


if __name__ == "__main__":
    assert lis_length([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_length([]) == 0
    print("lis: ok")
