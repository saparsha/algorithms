"""Ternary Search

Maximise a strictly unimodal function over a real interval.
"""

def ternary_search(f, lo, hi, iters=200):
    for _ in range(iters):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2):
            lo = m1
        else:
            hi = m2
    return (lo + hi) / 2


if __name__ == "__main__":
    x = ternary_search(lambda t: -(t - 2) ** 2, -10, 10)
    assert abs(x - 2) < 1e-6
    print("ternary-search: ok")
