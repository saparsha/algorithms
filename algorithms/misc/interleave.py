"""Interleave Sequences

Round-robin merge of several iterables of differing lengths.
"""

def interleave(*iterables):
    iters = [iter(it) for it in iterables]
    out = []
    while iters:
        alive = []
        for it in iters:
            item = next(it, _MISSING)
            if item is not _MISSING:
                out.append(item)
                alive.append(it)
        iters = alive
    return out


_MISSING = object()


if __name__ == "__main__":
    assert interleave([1, 2, 3], "ab") == [1, "a", 2, "b", 3]
    assert interleave() == []
    print("interleave: ok")
