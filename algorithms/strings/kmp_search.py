"""Knuth-Morris-Pratt

Linear-time substring search using a prefix-function failure table.
"""

def kmp_search(text, pattern):
    if not pattern:
        return 0
    fail = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k and pattern[k] != pattern[i]:
            k = fail[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        fail[i] = k
    k = 0
    for i, ch in enumerate(text):
        while k and pattern[k] != ch:
            k = fail[k - 1]
        if pattern[k] == ch:
            k += 1
        if k == len(pattern):
            return i - k + 1
    return -1


if __name__ == "__main__":
    assert kmp_search("abxabcabcaby", "abcaby") == 6
    assert kmp_search("aaa", "b") == -1
    print("kmp-search: ok")
