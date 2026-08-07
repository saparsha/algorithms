"""Modular Exponentiation

Square-and-multiply computation of (base ** exp) % mod.
"""

def power_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


if __name__ == "__main__":
    assert power_mod(2, 10, 1000) == 24
    assert power_mod(3, 0, 7) == 1
    print("power-mod: ok")
