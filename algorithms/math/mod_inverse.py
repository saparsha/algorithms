"""Modular Inverse

Multiplicative inverse modulo m, when one exists.
"""

def mod_inverse(a, m):
    g, x = m, 0
    a0, x0 = a % m, 1
    while a0:
        q = g // a0
        g, a0 = a0, g - q * a0
        x, x0 = x0, x - q * x0
    if g != 1:
        raise ValueError("no inverse exists")
    return x % m


if __name__ == "__main__":
    assert mod_inverse(3, 11) == 4
    assert (3 * mod_inverse(3, 11)) % 11 == 1
    print("mod-inverse: ok")
