"""Segment Tree

Iterative segment tree for range-minimum queries.
"""

class SegmentTree:
    def __init__(self, values):
        self.n = len(values)
        self.tree = [float("inf")] * (2 * self.n)
        for i, v in enumerate(values):
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, value):
        i += self.n
        self.tree[i] = value
        while i > 1:
            i //= 2
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, lo, hi):
        lo, hi = lo + self.n, hi + self.n
        best = float("inf")
        while lo < hi:
            if lo & 1:
                best = min(best, self.tree[lo]); lo += 1
            if hi & 1:
                hi -= 1; best = min(best, self.tree[hi])
            lo //= 2; hi //= 2
        return best


if __name__ == "__main__":
    st = SegmentTree([5, 2, 8, 1])
    assert st.query(0, 3) == 2
    st.update(1, 9)
    assert st.query(0, 3) == 5
    print("segment-tree: ok")
