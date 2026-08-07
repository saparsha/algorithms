"""Singly Linked List

Linked list with push, iteration and in-place reversal.
"""

class Node:
    def __init__(self, value, nxt=None):
        self.value, self.next = value, nxt


class LinkedList:
    def __init__(self, values=()):
        self.head = None
        for v in reversed(list(values)):
            self.head = Node(v, self.head)

    def __iter__(self):
        node = self.head
        while node:
            yield node.value
            node = node.next

    def reverse(self):
        prev, node = None, self.head
        while node:
            node.next, prev, node = prev, node, node.next
        self.head = prev
        return self


if __name__ == "__main__":
    ll = LinkedList([1, 2, 3])
    assert list(ll) == [1, 2, 3]
    assert list(ll.reverse()) == [3, 2, 1]
    print("linked-list: ok")
