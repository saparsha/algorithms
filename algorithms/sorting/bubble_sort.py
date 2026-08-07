"""Bubble Sort

Textbook exchange sort with an early-exit pass counter.
"""

def bubble_sort(xs):
    xs = list(xs)
    for end in range(len(xs) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if xs[i] > xs[i + 1]:
                xs[i], xs[i + 1] = xs[i + 1], xs[i]
                swapped = True
        if not swapped:
            break
    return xs


if __name__ == "__main__":
    assert bubble_sort([2, 1, 3]) == [1, 2, 3]
    print("bubble-sort: ok")
