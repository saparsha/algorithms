"""Similarity Ratio

Normalise edit distance into a 0..1 similarity score.
"""

def similarity(a, b):
    if not a and not b:
        return 1.0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return 1 - prev[-1] / max(len(a), len(b))


if __name__ == "__main__":
    assert similarity("abc", "abc") == 1.0
    assert similarity("", "") == 1.0
    assert 0 < similarity("kitten", "sitting") < 1
    print("levenshtein-ratio: ok")
