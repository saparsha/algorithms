"""Trie

Prefix tree for word insertion, lookup and prefix queries.
"""

class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True
        return self

    def __contains__(self, word):
        node = self._walk(word)
        return node is not None and "$" in node

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node


if __name__ == "__main__":
    t = Trie()
    t.insert("apple")
    assert "apple" in t and "app" not in t
    assert t.starts_with("app")
    print("trie: ok")
