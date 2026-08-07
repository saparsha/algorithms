"""Find the Unpaired Number

XOR every element so that pairs cancel and the loner remains.
"""

def single_number(xs):
    result = 0
    for x in xs:
        result ^= x
    return result


if __name__ == "__main__":
    assert single_number([4, 1, 2, 1, 2]) == 4
    print("single-number: ok")
