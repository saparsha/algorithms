"""Unique Grid Paths

Count monotone lattice paths across an m x n grid.
"""

def unique_paths(m, n):
    row = [1] * n
    for _ in range(m - 1):
        for j in range(1, n):
            row[j] += row[j - 1]
    return row[-1]


if __name__ == "__main__":
    assert unique_paths(3, 7) == 28
    assert unique_paths(1, 1) == 1
    print("unique-paths: ok")
