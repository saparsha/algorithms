"""Insertion Sort

Simple stable sort; O(n) on nearly-sorted input.
"""

def insertion_sort(xs):
    xs = list(xs)
    for i in range(1, len(xs)):
        key, j = xs[i], i - 1
        while j >= 0 and xs[j] > key:
            xs[j + 1] = xs[j]
            j -= 1
        xs[j + 1] = key
    return xs


if __name__ == "__main__":
    assert insertion_sort([4, 1, 3]) == [1, 3, 4]
    assert insertion_sort([1, 2, 3]) == [1, 2, 3]
    print("insertion-sort: ok")
