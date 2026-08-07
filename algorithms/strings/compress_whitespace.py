"""Normalise Whitespace

Collapse runs of whitespace and trim the result.
"""

import re


def normalise_whitespace(s):
    return re.sub(r"\s+", " ", s).strip()


if __name__ == "__main__":
    assert normalise_whitespace("  a\t\tb\n c ") == "a b c"
    assert normalise_whitespace("   ") == ""
    print("compress-whitespace: ok")
