"""Reverse Words

Reverse word order while collapsing runs of whitespace.
"""

def reverse_words(s):
    return " ".join(reversed(s.split()))


if __name__ == "__main__":
    assert reverse_words("  the sky  is blue ") == "blue is sky the"
    assert reverse_words("") == ""
    print("reverse-words: ok")
