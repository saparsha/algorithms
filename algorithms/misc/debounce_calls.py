"""Throttle

Allow a callable to run at most once per time window.
"""

import time


def throttle(fn, interval):
    state = {"last": None, "value": None}

    def wrapper(*args, **kwargs):
        now = time.monotonic()
        if state["last"] is None or now - state["last"] >= interval:
            state["last"] = now
            state["value"] = fn(*args, **kwargs)
        return state["value"]

    return wrapper


if __name__ == "__main__":
    calls = []
    f = throttle(lambda: calls.append(1) or len(calls), 60)
    assert f() == 1 and f() == 1
    assert len(calls) == 1
    print("debounce-calls: ok")
