"""Min Stack

Stack that reports its minimum element in constant time.
"""

class MinStack:
    def __init__(self):
        self._items, self._mins = [], []

    def push(self, item):
        self._items.append(item)
        self._mins.append(item if not self._mins else min(item, self._mins[-1]))

    def pop(self):
        self._mins.pop()
        return self._items.pop()

    def minimum(self):
        return self._mins[-1]


if __name__ == "__main__":
    s = MinStack()
    for v in (3, 1, 2):
        s.push(v)
    assert s.minimum() == 1
    s.pop(); s.pop()
    assert s.minimum() == 3
    print("min-stack: ok")
