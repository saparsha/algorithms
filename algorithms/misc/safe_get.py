"""Safe Nested Lookup

Traverse nested containers by path, returning a default on any miss.
"""

def safe_get(data, path, default=None):
    cur = data
    for key in path:
        try:
            cur = cur[key]
        except (KeyError, IndexError, TypeError):
            return default
    return cur


if __name__ == "__main__":
    d = {"a": {"b": [10, 20]}}
    assert safe_get(d, ["a", "b", 1]) == 20
    assert safe_get(d, ["a", "x"], "none") == "none"
    print("safe-get: ok")
