"""Two Sum

Find two indices whose values add to a target, in one pass.
"""

def two_sum(xs, target):
    seen = {}
    for i, x in enumerate(xs):
        if target - x in seen:
            return (seen[target - x], i)
        seen[x] = i
    return None


if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([1, 2], 100) is None
    print("two-sum: ok")
