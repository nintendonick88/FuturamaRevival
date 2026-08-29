"""Disassemble a bounded ARM range from the Futurama native library."""

from __future__ import annotations

import argparse
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_LITTLE_ENDIAN, Cs


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("start", type=lambda value: int(value, 0))
    parser.add_argument("end", type=lambda value: int(value, 0))
    return parser.parse_args()


def main() -> None:
    args = arguments()
    if args.start < 0 or args.end <= args.start:
        raise SystemExit("range must satisfy 0 <= start < end")
    blob = args.binary.read_bytes()
    if args.end > len(blob):
        raise SystemExit("range extends beyond the input file")

    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM | CS_MODE_LITTLE_ENDIAN)
    for instruction in decoder.disasm(blob[args.start : args.end], args.start):
        raw = instruction.bytes.hex()
        print(
            f"{instruction.address:08x}: {raw:<8} "
            f"{instruction.mnemonic:<8} {instruction.op_str}"
        )


if __name__ == "__main__":
    main()
