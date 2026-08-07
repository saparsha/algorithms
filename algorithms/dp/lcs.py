"""Longest Common Subsequence

Length of the longest subsequence common to two sequences.
"""

def lcs_length(a, b):
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0]
        for j, cb in enumerate(b):
            cur.append(prev[j] + 1 if ca == cb else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


if __name__ == "__main__":
    assert lcs_length("abcde", "ace") == 3
    assert lcs_length("abc", "def") == 0
    print("lcs: ok")
