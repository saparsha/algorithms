"""Stack

Last-in-first-out container with explicit underflow errors.
"""

class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def __len__(self):
        return len(self._items)


if __name__ == "__main__":
    s = Stack()
    s.push(1); s.push(2)
    assert s.pop() == 2 and s.peek() == 1 and len(s) == 1
    print("stack: ok")
