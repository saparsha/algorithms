"""Bipartite Check

Two-colour a graph with BFS to test bipartiteness.
"""

from collections import deque


def is_bipartite(graph):
    colour = {}
    for start in graph:
        if start in colour:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in graph.get(node, ()):
                if nxt not in colour:
                    colour[nxt] = 1 - colour[node]
                    queue.append(nxt)
                elif colour[nxt] == colour[node]:
                    return False
    return True


if __name__ == "__main__":
    assert is_bipartite({1: [2], 2: [1]})
    assert not is_bipartite({1: [2, 3], 2: [1, 3], 3: [1, 2]})
    print("bipartite-check: ok")
