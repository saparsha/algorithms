"""Merge Sort

Stable divide-and-conquer sort running in O(n log n).
"""

def merge_sort(xs):
    if len(xs) <= 1:
        return list(xs)
    mid = len(xs) // 2
    left, right = merge_sort(xs[:mid]), merge_sort(xs[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


if __name__ == "__main__":
    assert merge_sort([5, 2, 9, 1]) == [1, 2, 5, 9]
    assert merge_sort([]) == []
    print("merge-sort: ok")
