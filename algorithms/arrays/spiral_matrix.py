"""Spiral Matrix Traversal

Read a matrix in clockwise spiral order.
"""

def spiral(matrix):
    out = []
    m = [list(r) for r in matrix]
    while m:
        out.extend(m.pop(0))
        m = [list(r) for r in zip(*m)][::-1]
    return out


if __name__ == "__main__":
    assert spiral([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    print("spiral-matrix: ok")
