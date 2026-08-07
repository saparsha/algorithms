"""Connected Components

Partition an undirected graph into its connected components.
"""

def components(graph):
    seen, groups = set(), []
    for start in graph:
        if start in seen:
            continue
        stack, group = [start], []
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            group.append(node)
            stack.extend(graph.get(node, ()))
        groups.append(sorted(group))
    return sorted(groups)


if __name__ == "__main__":
    g = {1: [2], 2: [1], 3: []}
    assert components(g) == [[1, 2], [3]]
    print("connected-components: ok")
