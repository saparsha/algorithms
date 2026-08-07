"""Longest Consecutive Run

Longest run of consecutive integers present in an unsorted list.
"""

def longest_consecutive(xs):
    s = set(xs)
    best = 0
    for x in s:
        if x - 1 not in s:
            length = 1
            while x + length in s:
                length += 1
            best = max(best, length)
    return best


if __name__ == "__main__":
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([]) == 0
    print("longest-consecutive: ok")
