"""Collatz Sequence

Generate the hailstone sequence from n down to 1.
"""

def collatz(n):
    if n < 1:
        raise ValueError("n must be positive")
    seq = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        seq.append(n)
    return seq


if __name__ == "__main__":
    assert collatz(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]
    assert collatz(1) == [1]
    print("collatz: ok")
