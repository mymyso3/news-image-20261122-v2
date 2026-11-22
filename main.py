#!/usr/bin/env python3
"""Entry for make.fun news-image-20261122.

Writes entry.png (1024x1024, the front page for Sunday 22 November 2026)
to /output/entry.png. Standard library only, no network, deterministic:
the same bytes are written on every run, because the image is a fixed
file shipped in this repository (rendered at build time by render.py).

The output directory defaults to /output and can be overridden with
MAKEFUN_OUTPUT_DIR for local testing.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEFAULT_OUT = "/output"
TARGET_NAME = "entry.png"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUT
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, TARGET_NAME)
    with open(SOURCE, "rb") as src:
        digest = hashlib.sha256(src.read()).hexdigest()
    shutil.copyfile(SOURCE, target)
    with open(target, "rb") as done:
        written = hashlib.sha256(done.read()).hexdigest()
    if written != digest:
        print("mismatch: copied bytes differ from entry.png", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256=%s)"
          % (target, os.path.getsize(target), written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
