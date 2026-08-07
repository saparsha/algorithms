"""Weighted Selection

Deterministically select from weighted options given a 0..1 value.
"""

def weighted_choice(options, position):
    total = sum(w for _, w in options)
    target = position * total
    acc = 0.0
    for item, weight in options:
        acc += weight
        if target < acc:
            return item
    return options[-1][0]


if __name__ == "__main__":
    opts = [("a", 1), ("b", 3)]
    assert weighted_choice(opts, 0.1) == "a"
    assert weighted_choice(opts, 0.9) == "b"
    print("weighted-choice: ok")
