"""Moving Average

Simple moving average over a fixed-size sliding window.
"""

from collections import deque


def moving_average(values, window):
    if window <= 0:
        raise ValueError("window must be positive")
    buf, total, out = deque(), 0.0, []
    for v in values:
        buf.append(v)
        total += v
        if len(buf) > window:
            total -= buf.popleft()
        out.append(total / len(buf))
    return out


if __name__ == "__main__":
    assert moving_average([1, 2, 3, 4], 2) == [1.0, 1.5, 2.5, 3.5]
    print("chunked-average: ok")
