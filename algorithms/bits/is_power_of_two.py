"""Power of Two

Detect exact powers of two with a single bitwise test.
"""

def is_power_of_two(n):
    return n > 0 and n & (n - 1) == 0


if __name__ == "__main__":
    assert is_power_of_two(16)
    assert not is_power_of_two(0)
    assert not is_power_of_two(6)
    print("is-power-of-two: ok")
