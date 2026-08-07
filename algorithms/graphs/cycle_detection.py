"""Cycle Detection

Detect a cycle in a directed graph with three-colour DFS.
"""

def has_cycle(graph):
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {node: WHITE for node in graph}

    def visit(node):
        colour[node] = GREY
        for nxt in graph.get(node, ()):
            if colour.get(nxt, WHITE) == GREY:
                return True
            if colour.get(nxt, WHITE) == WHITE and visit(nxt):
                return True
        colour[node] = BLACK
        return False

    return any(visit(n) for n in graph if colour[n] == WHITE)


if __name__ == "__main__":
    assert has_cycle({"a": ["b"], "b": ["a"]})
    assert not has_cycle({"a": ["b"], "b": []})
    print("cycle-detection: ok")
