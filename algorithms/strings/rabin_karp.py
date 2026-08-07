"""Rabin-Karp

Rolling-hash substring search with verification on hash hits.
"""

def rabin_karp(text, pattern, base=257, mod=(1 << 61) - 1):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1
    high = pow(base, m - 1, mod)
    ph = th = 0
    for i in range(m):
        ph = (ph * base + ord(pattern[i])) % mod
        th = (th * base + ord(text[i])) % mod
    for i in range(n - m + 1):
        if ph == th and text[i:i + m] == pattern:
            return i
        if i < n - m:
            th = ((th - ord(text[i]) * high) * base + ord(text[i + m])) % mod
    return -1


if __name__ == "__main__":
    assert rabin_karp("hello world", "world") == 6
    assert rabin_karp("abc", "d") == -1
    print("rabin-karp: ok")
