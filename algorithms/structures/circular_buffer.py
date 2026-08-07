"""Circular Buffer

Fixed-size ring buffer that overwrites the oldest entry when full.
"""

class CircularBuffer:
    def __init__(self, capacity):
        self._data = [None] * capacity
        self._start = self._size = 0

    def push(self, item):
        end = (self._start + self._size) % len(self._data)
        self._data[end] = item
        if self._size == len(self._data):
            self._start = (self._start + 1) % len(self._data)
        else:
            self._size += 1

    def to_list(self):
        return [self._data[(self._start + i) % len(self._data)] for i in range(self._size)]


if __name__ == "__main__":
    b = CircularBuffer(3)
    for v in (1, 2, 3, 4):
        b.push(v)
    assert b.to_list() == [2, 3, 4]
    print("circular-buffer: ok")
