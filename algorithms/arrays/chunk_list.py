"""Chunk a List

Split a sequence into consecutive fixed-size chunks.
"""

def chunk(xs, size):
    if size <= 0:
        raise ValueError("size must be positive")
    return [xs[i:i + size] for i in range(0, len(xs), size)]


if __name__ == "__main__":
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert chunk([], 3) == []
    print("chunk-list: ok")
