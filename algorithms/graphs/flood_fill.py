"""Flood Fill

Replace a connected region of equal values in a grid.
"""

def flood_fill(grid, row, col, new_value):
    g = [list(r) for r in grid]
    if not g or g[row][col] == new_value:
        return g
    old = g[row][col]
    stack = [(row, col)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < len(g) and 0 <= c < len(g[0]) and g[r][c] == old:
            g[r][c] = new_value
            stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])
    return g


if __name__ == "__main__":
    assert flood_fill([[1, 1], [1, 0]], 0, 0, 2) == [[2, 2], [2, 0]]
    print("flood-fill: ok")
