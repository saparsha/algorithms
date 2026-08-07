"""Longest Palindromic Subsequence

Longest subsequence of a string that is itself a palindrome.
"""

def lps_length(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1] if n else 0


if __name__ == "__main__":
    assert lps_length("bbbab") == 4
    assert lps_length("") == 0
    print("longest-palindromic-subseq: ok")
