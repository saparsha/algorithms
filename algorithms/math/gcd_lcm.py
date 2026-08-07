"""GCD and LCM

Euclid's algorithm for the greatest common divisor, and LCM from it.
"""

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


if __name__ == "__main__":
    assert gcd(48, 18) == 6
    assert lcm(4, 6) == 12
    assert gcd(0, 5) == 5
    print("gcd-lcm: ok")
