"""Merge Intervals

Collapse overlapping [start, end] ranges into a minimal set.
"""

def merge_intervals(intervals):
    out = []
    for start, end in sorted(intervals):
        if out and start <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], end))
        else:
            out.append((start, end))
    return out


if __name__ == "__main__":
    assert merge_intervals([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]
    assert merge_intervals([]) == []
    print("merge-intervals: ok")
