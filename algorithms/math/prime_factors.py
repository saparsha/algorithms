"""Prime Factorisation

Trial division into a sorted list of prime factors with multiplicity.
"""

def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


if __name__ == "__main__":
    assert prime_factors(360) == [2, 2, 2, 3, 3, 5]
    assert prime_factors(13) == [13]
    print("prime-factors: ok")
