"""Apply one hash- and byte-guarded 32-bit ARM instruction patch.

This is intended for disposable diagnostic APK builds. It refuses to patch an
unexpected input, an out-of-range address, or an instruction whose bytes do
not match the caller's recorded expectation.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def parse_hex_word(value: str) -> bytes:
    compact = value.replace(" ", "").removeprefix("0x")
    result = bytes.fromhex(compact)
    if len(result) != 4:
        raise argparse.ArgumentTypeError("instruction must be exactly 4 bytes")
    return result


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--offset", required=True, type=lambda x: int(x, 0))
    parser.add_argument("--expect", required=True, type=parse_hex_word)
    parser.add_argument("--replace", required=True, type=parse_hex_word)
    parser.add_argument("--sha256", help="optional expected input SHA-256")
    return parser.parse_args()


def main() -> None:
    args = arguments()
    blob = bytearray(args.input.read_bytes())
    digest = hashlib.sha256(blob).hexdigest()
    if args.sha256 and digest.lower() != args.sha256.lower():
        raise SystemExit(f"input SHA-256 mismatch: {digest}")
    if args.offset < 0 or args.offset + 4 > len(blob):
        raise SystemExit("patch offset is outside input")
    actual = bytes(blob[args.offset : args.offset + 4])
    if actual != args.expect:
        raise SystemExit(
            f"instruction mismatch at 0x{args.offset:x}: "
            f"expected {args.expect.hex()}, found {actual.hex()}"
        )
    blob[args.offset : args.offset + 4] = args.replace
    args.output.write_bytes(blob)
    print(f"input_sha256={digest}")
    print(f"output_sha256={hashlib.sha256(blob).hexdigest()}")
    print(f"offset=0x{args.offset:x}")
    print(f"before={actual.hex()}")
    print(f"after={args.replace.hex()}")


if __name__ == "__main__":
    main()
