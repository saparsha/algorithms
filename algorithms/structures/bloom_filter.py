"""Bloom Filter

Probabilistic set membership with no false negatives.
"""

import hashlib


class BloomFilter:
    def __init__(self, size=1024, hashes=3):
        self.size, self.hashes = size, hashes
        self.bits = bytearray(size)

    def _positions(self, item):
        data = str(item).encode()
        for i in range(self.hashes):
            digest = hashlib.sha256(data + bytes([i])).digest()
            yield int.from_bytes(digest[:8], "big") % self.size

    def add(self, item):
        for pos in self._positions(item):
            self.bits[pos] = 1

    def __contains__(self, item):
        return all(self.bits[pos] for pos in self._positions(item))


if __name__ == "__main__":
    bf = BloomFilter()
    bf.add("hello")
    assert "hello" in bf
    assert "definitely-not-present-xyz" not in bf
    print("bloom-filter: ok")
