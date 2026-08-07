"""Frequency Counter

Count occurrences and report the n most common values.
"""

class FrequencyCounter:
    def __init__(self, items=()):
        self._counts = {}
        for item in items:
            self.add(item)

    def add(self, item):
        self._counts[item] = self._counts.get(item, 0) + 1

    def most_common(self, n=None):
        ordered = sorted(self._counts.items(), key=lambda kv: (-kv[1], str(kv[0])))
        return ordered if n is None else ordered[:n]


if __name__ == "__main__":
    fc = FrequencyCounter("abracadabra")
    assert fc.most_common(2) == [("a", 5), ("b", 2)]
    print("ordered-dict-lru: ok")
