"""Flatten a Dictionary

Collapse nested mappings into dotted-path keys.
"""

def flatten_dict(d, prefix=""):
    out = {}
    for key, value in d.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict) and value:
            out.update(flatten_dict(value, path))
        else:
            out[path] = value
    return out


if __name__ == "__main__":
    assert flatten_dict({"a": {"b": 1}, "c": 2}) == {"a.b": 1, "c": 2}
    print("flatten-dict: ok")
