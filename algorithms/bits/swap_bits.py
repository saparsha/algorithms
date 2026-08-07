"""Reverse Bits

Reverse the bit order of a fixed-width unsigned integer.
"""

def reverse_bits(n, width=32):
    result = 0
    for _ in range(width):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


if __name__ == "__main__":
    assert reverse_bits(1, 8) == 128
    assert reverse_bits(reverse_bits(12345, 32), 32) == 12345
    print("swap-bits: ok")
