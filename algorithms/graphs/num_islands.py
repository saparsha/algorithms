"""Count Islands

Number of connected land regions in a binary grid.
"""

def count_islands(grid):
    if not grid:
        return 0
    g = [list(r) for r in grid]
    count = 0
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] != 1:
                continue
            count += 1
            stack = [(i, j)]
            while stack:
                r, c = stack.pop()
                if 0 <= r < len(g) and 0 <= c < len(g[0]) and g[r][c] == 1:
                    g[r][c] = 0
                    stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])
    return count


if __name__ == "__main__":
    assert count_islands([[1, 1, 0], [0, 0, 0], [1, 0, 1]]) == 3
    print("num-islands: ok")
