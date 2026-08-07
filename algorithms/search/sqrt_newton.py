"""Integer Square Root

Newton's method for floor(sqrt(n)) using only integer arithmetic.
"""

def isqrt(n):
    if n < 0:
        raise ValueError("negative input")
    if n == 0:
        return 0
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


if __name__ == "__main__":
    assert isqrt(0) == 0
    assert isqrt(15) == 3
    assert isqrt(16) == 4
    assert isqrt(10**12) == 10**6
    print("sqrt-newton: ok")
