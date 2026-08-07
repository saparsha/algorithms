"""Levenshtein Distance

Minimum single-character edits to turn one string into another.
"""

def levenshtein(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


if __name__ == "__main__":
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("", "abc") == 3
    print("levenshtein: ok")
