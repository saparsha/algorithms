"""Minimum Window Substring

Smallest slice of a string containing all characters of a pattern.
"""

from collections import Counter


def min_window(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    best = (0, 0)
    start = 0
    for end, ch in enumerate(s, 1):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while need[s[start]] < 0:
                need[s[start]] += 1
                start += 1
            if not best[1] or end - start < best[1] - best[0]:
                best = (start, end)
    return s[best[0]:best[1]]


if __name__ == "__main__":
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "aa") == ""
    print("min-window-substring: ok")
