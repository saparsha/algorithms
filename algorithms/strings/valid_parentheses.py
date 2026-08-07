"""Balanced Brackets

Stack-based validation of nested (), [] and {} pairs.
"""

def is_balanced(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


if __name__ == "__main__":
    assert is_balanced("{[()]}")
    assert not is_balanced("(]")
    assert is_balanced("")
    print("valid-parentheses: ok")
