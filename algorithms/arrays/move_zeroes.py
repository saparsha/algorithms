"""Move Zeroes

Shift all zeroes to the end while preserving relative order.
"""

def move_zeroes(xs):
    xs = list(xs)
    slot = 0
    for i, x in enumerate(xs):
        if x != 0:
            xs[slot], xs[i] = xs[i], xs[slot]
            slot += 1
    return xs


if __name__ == "__main__":
    assert move_zeroes([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]
    print("move-zeroes: ok")
