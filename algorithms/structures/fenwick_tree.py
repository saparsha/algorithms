"""Fenwick Tree

Binary indexed tree for prefix sums with point updates.
"""

class FenwickTree:
    def __init__(self, size):
        self._tree = [0] * (size + 1)

    def add(self, i, delta):
        i += 1
        while i < len(self._tree):
            self._tree[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        total = 0
        while i > 0:
            total += self._tree[i]
            i -= i & -i
        return total

    def range_sum(self, lo, hi):
        return self.prefix_sum(hi) - self.prefix_sum(lo)


if __name__ == "__main__":
    f = FenwickTree(5)
    for i, v in enumerate([1, 2, 3, 4, 5]):
        f.add(i, v)
    assert f.range_sum(1, 4) == 9
    print("fenwick-tree: ok")
