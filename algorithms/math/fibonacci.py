"""Fibonacci (Fast Doubling)

n-th Fibonacci number in O(log n) via the fast-doubling identities.
"""

def fib(n):
    def helper(k):
        if k == 0:
            return (0, 1)
        a, b = helper(k >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        return (d, c + d) if k & 1 else (c, d)

    return helper(n)[0]


if __name__ == "__main__":
    assert fib(0) == 0
    assert fib(10) == 55
    assert fib(50) == 12586269025
    print("fibonacci: ok")
