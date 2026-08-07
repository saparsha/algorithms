"""Word Break

Decide whether a string splits into a sequence of dictionary words.
"""

def word_break(s, words):
    vocab = set(words)
    ok = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        ok[i] = any(ok[j] and s[j:i] in vocab for j in range(i))
    return ok[len(s)]


if __name__ == "__main__":
    assert word_break("leetcode", ["leet", "code"])
    assert not word_break("catsandog", ["cats", "dog", "sand", "and"])
    print("word-break: ok")
