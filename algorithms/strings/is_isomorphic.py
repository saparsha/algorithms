"""Isomorphic Strings

Check for a consistent one-to-one character mapping between strings.
"""

def is_isomorphic(a, b):
    if len(a) != len(b):
        return False
    fwd, rev = {}, {}
    for x, y in zip(a, b):
        if fwd.setdefault(x, y) != y or rev.setdefault(y, x) != x:
            return False
    return True


if __name__ == "__main__":
    assert is_isomorphic("egg", "add")
    assert not is_isomorphic("foo", "bar")
    print("is-isomorphic: ok")
