#!/usr/bin/env python3
"""Run every algorithm module and report the ones that fail.

Each module under algorithms/ checks itself with assertions guarded by a
`if __name__ == "__main__"` block, so running the file *is* running its tests.
This runner just executes them all as subprocesses and summarises the result.
"""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SOURCES = sorted(ROOT.glob("algorithms/*/*.py"))


def main():
    if not SOURCES:
        print("no modules found under algorithms/")
        return 0

    failures = []
    for path in SOURCES:
        result = subprocess.run(
            [sys.executable, str(path)], capture_output=True, text=True
        )
        if result.returncode != 0:
            failures.append((path, result.stderr.strip()))
            print(f"FAIL {path.relative_to(ROOT)}")
        else:
            print(f"ok   {path.relative_to(ROOT)}")

    print(f"\n{len(SOURCES) - len(failures)}/{len(SOURCES)} passed")
    for path, err in failures:
        last_line = err.splitlines()[-1] if err else "no output"
        print(f"\n{path.relative_to(ROOT)}:\n  {last_line}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
