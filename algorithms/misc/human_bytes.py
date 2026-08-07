"""Human-Readable Byte Sizes

Format a byte count using binary SI prefixes.
"""

UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]


def human_bytes(size):
    value = float(size)
    for unit in UNITS:
        if abs(value) < 1024 or unit == UNITS[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024


if __name__ == "__main__":
    assert human_bytes(512) == "512 B"
    assert human_bytes(2048) == "2.0 KiB"
    assert human_bytes(1536 * 1024) == "1.5 MiB"
    print("human-bytes: ok")
