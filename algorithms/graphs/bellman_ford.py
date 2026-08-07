"""Bellman-Ford

Shortest paths tolerating negative edges, with cycle detection.
"""

def bellman_ford(vertices, edges, start):
    dist = {v: float("inf") for v in vertices}
    dist[start] = 0
    for _ in range(len(vertices) - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            raise ValueError("negative cycle")
    return dist


if __name__ == "__main__":
    d = bellman_ford(["a", "b", "c"], [("a", "b", 4), ("a", "c", 5), ("b", "c", -3)], "a")
    assert d == {"a": 0, "b": 4, "c": 1}
    print("bellman-ford: ok")
