"""Perfect Numbers

A number equal to the sum of its proper divisors.
"""

def is_perfect(n):
    if n < 2:
        return False
    total = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            total += d
            if d != n // d:
                total += n // d
        d += 1
    return total == n


if __name__ == "__main__":
    assert is_perfect(28)
    assert not is_perfect(12)
    print("is-perfect-number: ok")
