"""Matrix Chain Order

Cheapest parenthesisation cost for a chain of matrix products.
"""

def matrix_chain(dims):
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = min(
                dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                for k in range(i, j)
            )
    return dp[0][n - 1] if n else 0


if __name__ == "__main__":
    assert matrix_chain([10, 30, 5, 60]) == 4500
    print("matrix-chain: ok")
