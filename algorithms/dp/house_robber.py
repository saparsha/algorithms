"""House Robber

Maximum sum of non-adjacent elements.
"""

def rob(values):
    skip = take = 0
    for v in values:
        skip, take = max(skip, take), skip + v
    return max(skip, take)


if __name__ == "__main__":
    assert rob([2, 7, 9, 3, 1]) == 12
    assert rob([]) == 0
    print("house-robber: ok")
