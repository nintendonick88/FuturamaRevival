"""Find direct ARM B/BL references to selected virtual addresses."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path

from elftools.elf.elffile import ELFFile


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf", type=Path)
    parser.add_argument("addresses", nargs="+", type=lambda value: int(value, 0))
    args = parser.parse_args()

    with args.elf.open("rb") as stream:
        text = ELFFile(stream).get_section_by_name(".text")
        if text is None:
            raise SystemExit("ELF has no .text section")
        base = int(text["sh_addr"])
        data = text.data()

    targets = set(args.addresses)
    matches: list[tuple[int, str, int]] = []
    for offset in range(0, len(data) - 3, 4):
        word = struct.unpack_from("<I", data, offset)[0]
        # ARM B/BL immediate. Exclude cond=1111, whose encoding is BLX.
        if word & 0x0E000000 != 0x0A000000 or word >> 28 == 0xF:
            continue
        delta = (word & 0x00FFFFFF) << 2
        if delta & 0x02000000:
            delta -= 0x04000000
        source = base + offset
        target = source + 8 + delta
        if target in targets:
            matches.append((source, "bl" if word & 0x01000000 else "b", target))

    for target in args.addresses:
        print(f"target 0x{target:08x}")
    for source, mnemonic, target in matches:
        print(f"xref source=0x{source:08x} mnemonic={mnemonic} target=0x{target:08x}")
    if not matches:
        print("no direct ARM B/BL references matched")


if __name__ == "__main__":
    main()
