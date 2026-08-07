"""Dijkstra's Algorithm

Shortest paths from a source in a non-negatively weighted graph.
"""

import heapq


def dijkstra(graph, start):
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float("inf")):
            continue
        for nxt, weight in graph.get(node, ()):
            nd = d + weight
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return dist


if __name__ == "__main__":
    g = {"a": [("b", 1), ("c", 4)], "b": [("c", 2)], "c": []}
    assert dijkstra(g, "a") == {"a": 0, "b": 1, "c": 3}
    print("dijkstra: ok")
