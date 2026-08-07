"""Longest Binary Gap

Longest run of zeroes bounded by ones in a number's binary form.
"""

def binary_gap(n):
    best = cur = 0
    started = False
    for bit in bin(n)[2:]:
        if bit == "1":
            if started:
                best = max(best, cur)
            started, cur = True, 0
        elif started:
            cur += 1
    return best


if __name__ == "__main__":
    assert binary_gap(529) == 4
    assert binary_gap(15) == 0
    print("binary-gap: ok")
