"""Longest Common Prefix

Longest prefix shared by every string in a list.
"""

def longest_common_prefix(words):
    if not words:
        return ""
    first, last = min(words), max(words)
    for i, ch in enumerate(first):
        if i >= len(last) or last[i] != ch:
            return first[:i]
    return first


if __name__ == "__main__":
    assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"
    assert longest_common_prefix(["dog", "car"]) == ""
    print("longest-common-prefix: ok")
