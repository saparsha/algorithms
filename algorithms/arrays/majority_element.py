"""Boyer-Moore Majority Vote

Find an element occurring more than n/2 times in O(1) space.
"""

def majority(xs):
    candidate, count = None, 0
    for x in xs:
        if count == 0:
            candidate = x
        count += 1 if x == candidate else -1
    return candidate if xs.count(candidate) * 2 > len(xs) else None


if __name__ == "__main__":
    assert majority([2, 2, 1, 1, 2]) == 2
    assert majority([1, 2]) is None
    print("majority-element: ok")
