"""Validate IPv4

Strict dotted-quad validation rejecting leading zeroes.
"""

def is_ipv4(s):
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit() or (len(p) > 1 and p[0] == "0"):
            return False
        if not 0 <= int(p) <= 255:
            return False
    return True


if __name__ == "__main__":
    assert is_ipv4("192.168.0.1")
    assert not is_ipv4("192.168.01.1")
    assert not is_ipv4("256.0.0.1")
    print("validate-ipv4: ok")
