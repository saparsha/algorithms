"""Longest Palindromic Substring

Expand around every centre to find the longest palindrome.
"""

def longest_palindrome(s):
    best = ""
    for i in range(len(s)):
        for lo, hi in ((i, i), (i, i + 1)):
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo -= 1
                hi += 1
            if hi - lo - 1 > len(best):
                best = s[lo + 1:hi]
    return best


if __name__ == "__main__":
    assert longest_palindrome("babad") in ("bab", "aba")
    assert longest_palindrome("cbbd") == "bb"
    print("longest-palindromic-substring: ok")
