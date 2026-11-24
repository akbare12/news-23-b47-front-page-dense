#!/usr/bin/env python3
"""news-23 b47 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is empty", file=sys.stderr)
        return 1
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        print("MAKEFUN_OUTPUT_DIR must not be inside the repo", file=sys.stderr)
        return 1
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > 1024 * 1024:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("not a PNG file", file=sys.stderr)
        return 1
    # IHDR: width, height, bit depth, colour type (manual parse, no PIL).
    width, height, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        print(f"wrong size: {width}x{height}", file=sys.stderr)
        return 1
    if depth != 8 or ctype not in (2, 6):
        print(f"unexpected PNG type: depth {depth}, colour {ctype}", file=sys.stderr)
        return 1
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        print("PNG trailer (IEND) is not well-formed", file=sys.stderr)
        return 1
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        check = f.read()
    if check != data:
        print("output does not match source", file=sys.stderr)
        return 1
    print(f"source {src} ({len(data)} bytes, {width}x{height})")
    print(f"wrote {dst} ({len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
