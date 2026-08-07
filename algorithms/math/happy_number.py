"""Happy Numbers

Detect whether repeated digit-square sums reach 1.
"""

def is_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1


if __name__ == "__main__":
    assert is_happy(19)
    assert not is_happy(2)
    print("happy-number: ok")
