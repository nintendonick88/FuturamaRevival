"""Find common ARM PIC constructions of selected code/data addresses.

The stripped Futurama 1.6.6 client commonly materializes an address with:

    ldr  rN, [pc, #literal]
    ...
    add  rN, pc, rN

The literal is a signed delta from the second instruction's ARM PC value.
This archaeology helper reports exact matches for requested virtual addresses.
It recognizes only this compiler pattern and therefore cannot prove that no
other references exist.
"""

from __future__ import annotations

import argparse
import bisect
import struct
from pathlib import Path

from elftools.elf.elffile import ELFFile


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf", type=Path)
    parser.add_argument(
        "addresses",
        nargs="+",
        type=lambda value: int(value, 0),
        help="virtual addresses, such as 0xe46d9c",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=64,
        help="maximum bytes between literal load and resolver (default: 64)",
    )
    return parser.parse_args()


def prel31(place: int, word: int) -> int:
    delta = word & 0x7FFFFFFF
    if delta & 0x40000000:
        delta -= 0x80000000
    return place + delta


def main() -> None:
    args = arguments()
    blob = args.elf.read_bytes()

    with args.elf.open("rb") as stream:
        elf = ELFFile(stream)
        text = elf.get_section_by_name(".text")
        exidx = elf.get_section_by_name(".ARM.exidx")
        if text is None or exidx is None:
            raise SystemExit("ELF must contain .text and .ARM.exidx")
        text_address = int(text["sh_addr"])
        text_bytes = text.data()
        exidx_address = int(exidx["sh_addr"])
        exidx_bytes = exidx.data()

    function_starts = sorted(
        {
            prel31(exidx_address + offset, struct.unpack_from("<I", exidx_bytes, offset)[0])
            for offset in range(0, len(exidx_bytes) - 7, 8)
        }
    )

    def containing_function(address: int) -> tuple[int, int | None]:
        index = bisect.bisect_right(function_starts, address) - 1
        if index < 0:
            return (0, None)
        end = function_starts[index + 1] if index + 1 < len(function_starts) else None
        return (function_starts[index], end)

    literal_loads: list[tuple[int, int, int]] = []
    resolvers: dict[int, tuple[str, int]] = {}

    for offset in range(0, len(text_bytes) - 3, 4):
        address = text_address + offset
        word = struct.unpack_from("<I", text_bytes, offset)[0]

        # LDR Rd, [PC, +/-imm12], immediate/pre-indexed/word/no-writeback.
        if word & 0x0F7F0000 == 0x051F0000:
            register = (word >> 12) & 0xF
            displacement = word & 0xFFF
            literal_address = address + 8
            literal_address += displacement if word & (1 << 23) else -displacement
            if 0 <= literal_address <= len(blob) - 4:
                delta = struct.unpack_from("<i", blob, literal_address)[0]
                literal_loads.append((address, register, delta))

        # ADD/SUB Rd, Rn, Rm with no shift, where inputs are PC and Rd.
        if word & 0x0E000FF0 == 0:
            opcode = (word >> 21) & 0xF
            if opcode not in {2, 4}:
                continue
            destination = (word >> 12) & 0xF
            left = (word >> 16) & 0xF
            right = word & 0xF
            if {left, right} == {15, destination}:
                resolvers[address] = ("add" if opcode == 4 else "sub", destination)

    targets = set(args.addresses)
    matches: set[tuple[int, int, int]] = set()
    for load_address, register, delta in literal_loads:
        for distance in range(0, args.window + 1, 4):
            resolve_address = load_address + distance
            resolver = resolvers.get(resolve_address)
            if resolver is None or resolver[1] != register:
                continue
            resolved = resolve_address + 8
            resolved += delta if resolver[0] == "add" else -delta
            if resolved not in targets:
                continue
            if containing_function(load_address) != containing_function(resolve_address):
                continue
            matches.add((load_address, resolve_address, resolved))

    for target in args.addresses:
        print(f"target 0x{target:08x}")
    for load, resolve, target in sorted(matches):
        start, end = containing_function(load)
        end_text = f"0x{end:08x}" if end is not None else "unknown"
        print(
            f"xref load=0x{load:08x} resolve=0x{resolve:08x} "
            f"target=0x{target:08x} function=0x{start:08x}-{end_text}"
        )
    if not matches:
        print("no references matched the recognized ARM PIC pattern")


if __name__ == "__main__":
    main()
