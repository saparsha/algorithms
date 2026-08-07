"""Deep Merge Dictionaries

Recursively merge nested mappings without mutating the inputs.
"""

def deep_merge(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(out.get(key), dict) and isinstance(value, dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out


if __name__ == "__main__":
    a = {"x": {"y": 1, "z": 2}}
    b = {"x": {"z": 9}, "w": 3}
    assert deep_merge(a, b) == {"x": {"y": 1, "z": 9}, "w": 3}
    assert a == {"x": {"y": 1, "z": 2}}
    print("deep-merge: ok")
