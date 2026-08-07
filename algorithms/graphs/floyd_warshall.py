"""Floyd-Warshall

All-pairs shortest paths by dynamic programming over intermediates.
"""

def floyd_warshall(vertices, edges):
    dist = {u: {v: (0 if u == v else float("inf")) for v in vertices} for u in vertices}
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


if __name__ == "__main__":
    d = floyd_warshall("abc", [("a", "b", 1), ("b", "c", 2)])
    assert d["a"]["c"] == 3
    print("floyd-warshall: ok")
