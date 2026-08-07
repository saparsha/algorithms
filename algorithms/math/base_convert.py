"""Arbitrary Base Conversion

Convert a non-negative integer to any base from 2 to 36.
"""

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n, base):
    if not 2 <= base <= 36:
        raise ValueError("base out of range")
    if n == 0:
        return "0"
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(DIGITS[r])
    return "".join(reversed(out))


if __name__ == "__main__":
    assert to_base(255, 16) == "ff"
    assert to_base(0, 2) == "0"
    assert to_base(10, 2) == "1010"
    print("base-convert: ok")
