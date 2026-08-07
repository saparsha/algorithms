"""Extended Euclidean Algorithm

Solve ax + by = gcd(a, b) for the Bezout coefficients.
"""

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x, y = extended_gcd(b, a % b)
    return (g, y, x - (a // b) * y)


if __name__ == "__main__":
    g, x, y = extended_gcd(240, 46)
    assert g == 2 and 240 * x + 46 * y == 2
    print("extended-gcd: ok")
