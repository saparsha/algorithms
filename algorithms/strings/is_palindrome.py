"""Palindrome Check

Test whether a string reads the same forwards and backwards, ignoring case and non-alphanumerics.
"""

def is_palindrome(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    assert is_palindrome("A man, a plan, a canal: Panama")
    assert not is_palindrome("hello")
    assert is_palindrome("")
    print("is-palindrome: ok")
