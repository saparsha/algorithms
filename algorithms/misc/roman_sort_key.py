"""Natural Sort Key

Sort strings so embedded numbers compare numerically.
"""

import re


def natural_key(s):
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", s)]


if __name__ == "__main__":
    assert sorted(["item10", "item2"], key=natural_key) == ["item2", "item10"]
    print("roman-sort-key: ok")
