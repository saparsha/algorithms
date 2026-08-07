"""Longest Substring Without Repeats

Sliding window over the last-seen index of each character.
"""

def longest_unique(s):
    seen, start, best = {}, 0, 0
    for i, ch in enumerate(s):
        if ch in seen and seen[ch] >= start:
            start = seen[ch] + 1
        seen[ch] = i
        best = max(best, i - start + 1)
    return best


if __name__ == "__main__":
    assert longest_unique("abcabcbb") == 3
    assert longest_unique("bbbbb") == 1
    assert longest_unique("") == 0
    print("longest-unique-substring: ok")
