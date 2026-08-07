"""Retry with Backoff

Re-run a callable on failure with exponentially growing delays.
"""

import time


def retry(fn, attempts=3, delay=0.01, factor=2.0, exceptions=(Exception,)):
    for attempt in range(attempts):
        try:
            return fn()
        except exceptions:
            if attempt == attempts - 1:
                raise
            time.sleep(delay * factor ** attempt)


if __name__ == "__main__":
    state = {"n": 0}


    def flaky():
        state["n"] += 1
        if state["n"] < 3:
            raise ValueError("not yet")
        return "ok"


    assert retry(flaky) == "ok"
    assert state["n"] == 3
    print("retry-backoff: ok")
