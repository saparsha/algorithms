"""Edit Distance with Operations

Levenshtein distance plus the actual edit script.
"""

def edit_script(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1,
                           dp[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    ops, i, j = [], n, m
    while i or j:
        if i and j and dp[i][j] == dp[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            if a[i - 1] != b[j - 1]:
                ops.append(("replace", i - 1, b[j - 1]))
            i, j = i - 1, j - 1
        elif i and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(("delete", i - 1, a[i - 1]))
            i -= 1
        else:
            ops.append(("insert", i, b[j - 1]))
            j -= 1
    return dp[n][m], list(reversed(ops))


if __name__ == "__main__":
    dist, ops = edit_script("kitten", "sitting")
    assert dist == 3 and len(ops) == 3
    print("edit-distance-ops: ok")
