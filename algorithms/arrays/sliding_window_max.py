"""Sliding Window Maximum

Maximum of every k-length window using a monotonic deque.
"""

from collections import deque


def window_max(xs, k):
    dq, out = deque(), []
    for i, x in enumerate(xs):
        while dq and xs[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(xs[dq[0]])
    return out


if __name__ == "__main__":
    assert window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    print("sliding-window-max: ok")
