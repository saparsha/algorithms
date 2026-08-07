"""Caesar Cipher

Shift alphabetic characters by a fixed offset, preserving case.
"""

def caesar(s, shift):
    out = []
    for ch in s:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


if __name__ == "__main__":
    assert caesar("Hello, World!", 3) == "Khoor, Zruog!"
    assert caesar(caesar("abc", 5), -5) == "abc"
    print("caesar-cipher: ok")
