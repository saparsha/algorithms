"""Union-Find

Disjoint sets with path compression and union by rank.
"""

class UnionFind:
    def __init__(self, items=()):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x):
        self.parent.setdefault(x, x)
        self.rank.setdefault(x, 0)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


if __name__ == "__main__":
    uf = UnionFind("abcd")
    assert uf.union("a", "b")
    assert not uf.union("a", "b")
    assert uf.find("a") == uf.find("b") != uf.find("c")
    print("union-find: ok")
