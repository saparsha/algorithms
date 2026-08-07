"""Queue from Two Stacks

FIFO queue with amortised O(1) operations built on two stacks.
"""

class Queue:
    def __init__(self):
        self._front, self._back = [], []

    def enqueue(self, item):
        self._back.append(item)

    def dequeue(self):
        if not self._front:
            while self._back:
                self._front.append(self._back.pop())
        if not self._front:
            raise IndexError("dequeue from empty queue")
        return self._front.pop()

    def __len__(self):
        return len(self._front) + len(self._back)


if __name__ == "__main__":
    q = Queue()
    q.enqueue(1); q.enqueue(2)
    assert q.dequeue() == 1 and q.dequeue() == 2 and len(q) == 0
    print("queue-two-stacks: ok")
