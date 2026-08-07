"""Heapsort

In-place O(n log n) sort built on a binary max-heap.
"""

def heap_sort(xs):
    xs = list(xs)
    n = len(xs)

    def sift(root, size):
        while True:
            big, l, r = root, 2 * root + 1, 2 * root + 2
            if l < size and xs[l] > xs[big]:
                big = l
            if r < size and xs[r] > xs[big]:
                big = r
            if big == root:
                return
            xs[root], xs[big] = xs[big], xs[root]
            root = big

    for i in range(n // 2 - 1, -1, -1):
        sift(i, n)
    for end in range(n - 1, 0, -1):
        xs[0], xs[end] = xs[end], xs[0]
        sift(0, end)
    return xs


if __name__ == "__main__":
    assert heap_sort([5, 3, 8, 1]) == [1, 3, 5, 8]
    print("heap-sort: ok")
