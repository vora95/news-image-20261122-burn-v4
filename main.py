#!/usr/bin/env python3
"""THE LATE EDITION - Sunday 22 November 2026.

Copies the pre-rendered front page (entry.png) into the make.fun output
directory and verifies the copy byte-for-byte with SHA-256. The page was
drawn once from that day's verified wires and sealed as a single image;
this entrypoint only moves it, it never redraws it.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "5dd5e584c1c6ae2c5220472a91810d1c73fbb4ebf3d019bc31509d6d4fba45be"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    if sha256_of(SRC) != EXPECTED_SHA256:
        print("entry.png does not match the expected SHA-256", file=sys.stderr)
        return 3
    if os.path.getsize(SRC) >= 1024 * 1024:
        print("entry.png is over the 1 MiB limit", file=sys.stderr)
        return 5
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    if sha256_of(dst) != EXPECTED_SHA256:
        print("copied entry.png failed verification", file=sys.stderr)
        return 4
    print("wrote", dst, EXPECTED_SHA256)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
