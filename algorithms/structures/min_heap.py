"""Binary Min-Heap

Array-backed priority queue with push and pop in O(log n).
"""

class MinHeap:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)
        i = len(self._items) - 1
        while i and self._items[(i - 1) // 2] > self._items[i]:
            parent = (i - 1) // 2
            self._items[i], self._items[parent] = self._items[parent], self._items[i]
            i = parent

    def pop(self):
        items = self._items
        items[0], items[-1] = items[-1], items[0]
        smallest = items.pop()
        i = 0
        while True:
            small, l, r = i, 2 * i + 1, 2 * i + 2
            if l < len(items) and items[l] < items[small]:
                small = l
            if r < len(items) and items[r] < items[small]:
                small = r
            if small == i:
                return smallest
            items[i], items[small] = items[small], items[i]
            i = small

    def __len__(self):
        return len(self._items)


if __name__ == "__main__":
    h = MinHeap()
    for v in (5, 1, 3):
        h.push(v)
    assert [h.pop() for _ in range(3)] == [1, 3, 5]
    print("min-heap: ok")
