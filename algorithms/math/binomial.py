"""Binomial Coefficient

n choose k computed iteratively without large intermediate factorials.
"""

def binomial(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


if __name__ == "__main__":
    assert binomial(5, 2) == 10
    assert binomial(5, 6) == 0
    assert binomial(50, 25) == 126410606437752
    print("binomial: ok")
