"""Flatten Nested Lists

Recursively flatten arbitrarily nested iterables into one list.
"""

def flatten(xs):
    out = []
    for x in xs:
        if isinstance(x, (list, tuple)):
            out.extend(flatten(x))
        else:
            out.append(x)
    return out


if __name__ == "__main__":
    assert flatten([1, [2, [3, [4]]], 5]) == [1, 2, 3, 4, 5]
    assert flatten([]) == []
    print("flatten-nested: ok")
