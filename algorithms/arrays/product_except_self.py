"""Product Except Self

Product of all other elements, without division.
"""

def product_except_self(xs):
    n = len(xs)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= xs[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= xs[i]
    return out


if __name__ == "__main__":
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([0, 1]) == [1, 0]
    print("product-except-self: ok")
