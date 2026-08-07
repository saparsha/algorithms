"""Binary Search Tree

Unbalanced BST supporting insert, membership and in-order traversal.
"""

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        def go(node):
            if node is None:
                return {"value": value, "left": None, "right": None}
            if value < node["value"]:
                node["left"] = go(node["left"])
            elif value > node["value"]:
                node["right"] = go(node["right"])
            return node

        self.root = go(self.root)
        return self

    def __contains__(self, value):
        node = self.root
        while node:
            if value == node["value"]:
                return True
            node = node["left"] if value < node["value"] else node["right"]
        return False

    def in_order(self):
        out = []

        def walk(node):
            if node:
                walk(node["left"])
                out.append(node["value"])
                walk(node["right"])

        walk(self.root)
        return out


if __name__ == "__main__":
    t = BST()
    for v in (5, 3, 8, 1):
        t.insert(v)
    assert t.in_order() == [1, 3, 5, 8]
    assert 3 in t and 9 not in t
    print("binary-search-tree: ok")
