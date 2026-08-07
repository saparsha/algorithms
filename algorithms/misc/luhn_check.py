"""Luhn Checksum

Validate card-style identifiers with the Luhn mod-10 algorithm.
"""

def luhn_valid(number):
    digits = [int(c) for c in str(number) if c.isdigit()]
    if not digits:
        return False
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


if __name__ == "__main__":
    assert luhn_valid("4539578763621486")
    assert not luhn_valid("1234567812345678")
    print("luhn-check: ok")
