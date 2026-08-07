"""0/1 Knapsack

Maximise value under a weight limit, each item used at most once.
"""

def knapsack(items, capacity):
    best = [0] * (capacity + 1)
    for weight, value in items:
        for c in range(capacity, weight - 1, -1):
            best[c] = max(best[c], best[c - weight] + value)
    return best[capacity]


if __name__ == "__main__":
    assert knapsack([(1, 1), (3, 4), (4, 5), (5, 7)], 7) == 9
    assert knapsack([], 5) == 0
    print("knapsack: ok")
