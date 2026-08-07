"""Minimum Path Sum

Cheapest top-left to bottom-right path through a weighted grid.
"""

def min_path_sum(grid):
    if not grid:
        return 0
    row = [float("inf")] * len(grid[0])
    row[0] = 0
    for line in grid:
        row[0] += line[0]
        for j in range(1, len(line)):
            row[j] = min(row[j], row[j - 1]) + line[j]
    return row[-1]


if __name__ == "__main__":
    assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    print("min-path-sum: ok")
