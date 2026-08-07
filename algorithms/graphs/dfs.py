"""Depth-First Search

Iterative DFS returning vertices in visit order.
"""

def dfs(graph, start):
    seen, order, stack = set(), [], [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        stack.extend(reversed(graph.get(node, ())))
    return order


if __name__ == "__main__":
    g = {1: [2, 3], 2: [4], 3: [], 4: []}
    assert dfs(g, 1) == [1, 2, 4, 3]
    print("dfs: ok")
