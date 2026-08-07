"""Digital Root

Repeatedly sum digits until a single digit remains.
"""

def digital_root(n):
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9


if __name__ == "__main__":
    assert digital_root(9875) == 2
    assert digital_root(0) == 0
    print("digits-sum: ok")
