"""Population Count

Count set bits using Brian Kernighan's clear-lowest-bit trick.
"""

def popcount(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


if __name__ == "__main__":
    assert popcount(0) == 0
    assert popcount(255) == 8
    assert popcount(1 << 40) == 1
    print("count-bits: ok")
