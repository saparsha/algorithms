"""Floyd's Cycle Detection

Tortoise-and-hare detection of a loop in a linked structure.
"""

def has_cycle(head, next_of):
    slow = fast = head
    while fast is not None and next_of(fast) is not None:
        slow = next_of(slow)
        fast = next_of(next_of(fast))
        if slow is fast:
            return True
    return False


if __name__ == "__main__":
    chain = {1: 2, 2: 3, 3: None}
    assert not has_cycle(1, lambda n: chain[n])
    loop = {1: 2, 2: 3, 3: 2}
    assert has_cycle(1, lambda n: loop[n])
    print("detect-list-cycle: ok")
