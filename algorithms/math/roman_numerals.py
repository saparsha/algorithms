"""Roman Numerals

Convert between integers and Roman numeral strings.
"""

VALUES = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
          (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def to_roman(n):
    out = []
    for value, sym in VALUES:
        count, n = divmod(n, value)
        out.append(sym * count)
    return "".join(out)


def from_roman(s):
    lookup = {sym: v for v, sym in VALUES}
    total, i = 0, 0
    while i < len(s):
        if s[i:i + 2] in lookup:
            total += lookup[s[i:i + 2]]
            i += 2
        else:
            total += lookup[s[i]]
            i += 1
    return total


if __name__ == "__main__":
    assert to_roman(1994) == "MCMXCIV"
    assert from_roman("MCMXCIV") == 1994
    print("roman-numerals: ok")
