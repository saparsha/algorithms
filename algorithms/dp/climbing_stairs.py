"""Climbing Stairs

Count ways to climb n steps taking one or two at a time.
"""

def climb_stairs(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    assert climb_stairs(3) == 3
    assert climb_stairs(0) == 1
    print("climbing-stairs: ok")
