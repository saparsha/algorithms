"""Breadth-First Search

Shortest unweighted path lengths from a source vertex.
"""

from collections import deque


def bfs(graph, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph.get(node, ()):
            if nxt not in dist:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist


if __name__ == "__main__":
    g = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    assert bfs(g, "a") == {"a": 0, "b": 1, "c": 1, "d": 2}
    print("bfs: ok")
