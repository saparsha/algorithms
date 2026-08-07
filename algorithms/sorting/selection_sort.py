"""Selection Sort

Repeatedly move the smallest remaining element into place.
"""

def selection_sort(xs):
    xs = list(xs)
    for i in range(len(xs)):
        m = min(range(i, len(xs)), key=lambda k: xs[k])
        xs[i], xs[m] = xs[m], xs[i]
    return xs


if __name__ == "__main__":
    assert selection_sort([3, 1, 2]) == [1, 2, 3]
    print("selection-sort: ok")
