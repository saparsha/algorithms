"""Prim's MST

Minimum spanning tree grown from a single vertex with a heap.
"""

import heapq


def prim(graph, start):
    seen = {start}
    heap = [(w, start, v) for v, w in graph.get(start, ())]
    heapq.heapify(heap)
    total = 0
    while heap:
        w, _, v = heapq.heappop(heap)
        if v in seen:
            continue
        seen.add(v)
        total += w
        for nxt, weight in graph.get(v, ()):
            if nxt not in seen:
                heapq.heappush(heap, (weight, v, nxt))
    return total


if __name__ == "__main__":
    g = {"a": [("b", 1), ("c", 2)], "b": [("a", 1), ("c", 3)], "c": [("a", 2), ("b", 3)]}
    assert prim(g, "a") == 3
    print("prim: ok")
