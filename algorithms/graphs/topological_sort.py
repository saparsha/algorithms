"""Topological Sort

Kahn's algorithm for ordering a DAG, raising on cycles.
"""

from collections import deque


def topological_sort(graph):
    indeg = {node: 0 for node in graph}
    for node in graph:
        for nxt in graph[node]:
            indeg[nxt] = indeg.get(nxt, 0) + 1
    queue = deque(sorted(n for n, d in indeg.items() if d == 0))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, ()):
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    if len(order) != len(indeg):
        raise ValueError("graph has a cycle")
    return order


if __name__ == "__main__":
    assert topological_sort({"a": ["b"], "b": ["c"], "c": []}) == ["a", "b", "c"]
    print("topological-sort: ok")
