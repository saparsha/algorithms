"""Sieve of Eratosthenes

All primes below n via the classical sieve.
"""

def primes_below(n):
    if n < 3:
        return []
    sieve = bytearray([1]) * n
    sieve[0] = sieve[1] = 0
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(sieve[p * p::p]))
    return [i for i, ok in enumerate(sieve) if ok]


if __name__ == "__main__":
    assert primes_below(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    assert primes_below(2) == []
    print("sieve-eratosthenes: ok")
