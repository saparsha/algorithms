"""Kruskal's MST

Minimum spanning tree by sorting edges and unioning components.
"""

def kruskal(vertices, edges):
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, chosen = 0, []
    for w, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[rv] = ru
            total += w
            chosen.append((u, v, w))
    return total, chosen


if __name__ == "__main__":
    total, _ = kruskal("abcd", [(1, "a", "b"), (3, "b", "c"), (2, "a", "c"), (4, "c", "d")])
    assert total == 7
    print("kruskal: ok")
