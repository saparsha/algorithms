"""Prefix Sum Range Queries

Precompute cumulative sums for O(1) range-sum lookups.
"""

class PrefixSum:
    def __init__(self, xs):
        self.acc = [0]
        for x in xs:
            self.acc.append(self.acc[-1] + x)

    def range_sum(self, lo, hi):
        return self.acc[hi] - self.acc[lo]


if __name__ == "__main__":
    ps = PrefixSum([1, 2, 3, 4])
    assert ps.range_sum(1, 3) == 5
    assert ps.range_sum(0, 4) == 10
    print("prefix-sums: ok")
