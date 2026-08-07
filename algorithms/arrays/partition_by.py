"""Partition by Predicate

Split a sequence into matching and non-matching halves in one pass.
"""

def partition(xs, pred):
    yes, no = [], []
    for x in xs:
        (yes if pred(x) else no).append(x)
    return yes, no


if __name__ == "__main__":
    assert partition(range(6), lambda n: n % 2 == 0) == ([0, 2, 4], [1, 3, 5])
    print("partition-by: ok")
