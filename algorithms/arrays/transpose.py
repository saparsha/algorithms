"""Transpose a Matrix

Swap rows and columns of a rectangular matrix.
"""

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


if __name__ == "__main__":
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([]) == []
    print("transpose: ok")
