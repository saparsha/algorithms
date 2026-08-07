"""String Permutations

Generate every distinct ordering of a string's characters.
"""

def permutations(s):
    if len(s) <= 1:
        return [s]
    out = set()
    for i, ch in enumerate(s):
        for rest in permutations(s[:i] + s[i + 1:]):
            out.add(ch + rest)
    return sorted(out)


if __name__ == "__main__":
    assert permutations("abc") == ["abc", "acb", "bac", "bca", "cab", "cba"]
    assert permutations("aa") == ["aa"]
    print("string-permutations: ok")
