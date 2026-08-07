"""Run-Length Encoding

Compress and expand runs of repeated characters.
"""

from itertools import groupby


def rle_encode(s):
    return "".join(f"{ch}{len(list(g))}" for ch, g in groupby(s))


def rle_decode(s):
    out, i = [], 0
    while i < len(s):
        ch, i = s[i], i + 1
        n = ""
        while i < len(s) and s[i].isdigit():
            n += s[i]
            i += 1
        out.append(ch * int(n))
    return "".join(out)


if __name__ == "__main__":
    assert rle_encode("aaabbc") == "a3b2c1"
    assert rle_decode("a3b2c1") == "aaabbc"
    assert rle_decode(rle_encode("zzzz")) == "zzzz"
    print("run-length-encoding: ok")
