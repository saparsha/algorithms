"""Subsets via Bitmask

Enumerate the power set by iterating over bit patterns.
"""

def subsets(items):
    items = list(items)
    out = []
    for mask in range(1 << len(items)):
        out.append([items[i] for i in range(len(items)) if mask >> i & 1])
    return out


if __name__ == "__main__":
    assert subsets([1, 2]) == [[], [1], [2], [1, 2]]
    assert subsets([]) == [[]]
    print("subsets-bitmask: ok")
