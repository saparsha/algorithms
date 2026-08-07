"""Dependency Batches

Group DAG nodes into levels that may be processed in parallel.
"""

def batches(graph):
    indeg = {n: 0 for n in graph}
    for n in graph:
        for m in graph[n]:
            indeg[m] = indeg.get(m, 0) + 1
    out, ready = [], sorted(n for n, d in indeg.items() if d == 0)
    while ready:
        out.append(ready)
        nxt = []
        for n in ready:
            for m in graph.get(n, ()):
                indeg[m] -= 1
                if indeg[m] == 0:
                    nxt.append(m)
        ready = sorted(nxt)
    if sum(len(b) for b in out) != len(indeg):
        raise ValueError("graph has a cycle")
    return out


if __name__ == "__main__":
    assert batches({"a": ["c"], "b": ["c"], "c": []}) == [["a", "b"], ["c"]]
    print("topological-batches: ok")
