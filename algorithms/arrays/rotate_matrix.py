"""Rotate Matrix 90 Degrees

Rotate a square matrix clockwise in place.
"""

def rotate_matrix(matrix):
    n = len(matrix)
    m = [list(r) for r in matrix]
    for i in range(n):
        for j in range(i + 1, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]
    for row in m:
        row.reverse()
    return m


if __name__ == "__main__":
    assert rotate_matrix([[1, 2], [3, 4]]) == [[3, 1], [4, 2]]
    print("rotate-matrix: ok")
