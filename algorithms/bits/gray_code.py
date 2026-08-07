"""Gray Code

Generate the reflected binary code sequence of n bits.
"""

def gray_code(n):
    return [i ^ (i >> 1) for i in range(1 << n)]


if __name__ == "__main__":
    assert gray_code(2) == [0, 1, 3, 2]
    assert gray_code(0) == [0]
    print("gray-code: ok")
