"""Catalan Numbers

The n-th Catalan number, counting balanced bracket strings.
"""

def catalan(n):
    dp = [1] + [0] * n
    for i in range(1, n + 1):
        dp[i] = sum(dp[j] * dp[i - 1 - j] for j in range(i))
    return dp[n]


if __name__ == "__main__":
    assert catalan(0) == 1
    assert catalan(5) == 42
    print("catalan: ok")
