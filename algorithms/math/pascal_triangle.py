"""Pascal's Triangle

Generate the first n rows of Pascal's triangle.
"""

def pascal(n):
    rows = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = rows[-1][j - 1] + rows[-1][j]
        rows.append(row)
    return rows


if __name__ == "__main__":
    assert pascal(4) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]
    assert pascal(0) == []
    print("pascal-triangle: ok")
