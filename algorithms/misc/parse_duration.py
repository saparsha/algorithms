"""Parse Duration Strings

Turn strings like '1h30m' into a number of seconds.
"""

import re

MULTIPLIERS = {"s": 1, "m": 60, "h": 3600, "d": 86400}


def parse_duration(text):
    parts = re.findall(r"(\d+)([smhd])", text.strip().lower())
    if not parts:
        raise ValueError(f"cannot parse duration: {text!r}")
    return sum(int(n) * MULTIPLIERS[unit] for n, unit in parts)


if __name__ == "__main__":
    assert parse_duration("1h30m") == 5400
    assert parse_duration("45s") == 45
    print("parse-duration: ok")
