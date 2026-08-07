"""Group Anagrams

Bucket words by their sorted-letter signature.
"""

from collections import defaultdict


def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return sorted(groups.values())


if __name__ == "__main__":
    assert group_anagrams(["eat", "tea", "tan"]) == [["eat", "tea"], ["tan"]]
    print("group-anagrams: ok")
