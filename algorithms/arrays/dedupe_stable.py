"""Stable Deduplicate

Remove duplicates while keeping the first occurrence's position.
"""

def dedupe(xs):
    seen, out = set(), []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


if __name__ == "__main__":
    assert dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]
    print("dedupe-stable: ok")
