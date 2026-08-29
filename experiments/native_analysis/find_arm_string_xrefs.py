"""Find common ARM position-independent references to selected ELF strings.

The Futurama 1.6.6 native library is largely stripped, and full automatic
analysis is slow. This small archaeology helper recognizes the common ARM
sequence used by this binary:

    ldr  rN, [pc, #literal]
    ...
    add  rN, pc, rN

The literal contains a signed PC-relative delta. The script reports only exact
resolutions to strings supplied on the command line; it does not claim to find
every possible compiler code-generation pattern.
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
    parser.add_argument("strings", nargs="+")
    parser.add_argument(
        "--show-rodata-samples",
        type=int,
        default=0,
        help="show this many PIC resolutions into .rodata for diagnostics",
    )
    return parser.parse_args()


def c_string_offsets(blob: bytes, values: list[str]) -> dict[int, str]:
    results: dict[int, str] = {}
    for value in values:
        needle = value.encode("utf-8") + b"\0"
        start = 0
        while True:
            offset = blob.find(needle, start)
            if offset < 0:
                break
            results[offset] = value
            start = offset + 1
    return results


def main() -> None:
    args = arguments()
    blob = args.elf.read_bytes()
    targets = c_string_offsets(blob, args.strings)
    if not targets:
        raise SystemExit("none of the requested strings were found")

    with args.elf.open("rb") as stream:
        elf = ELFFile(stream)
        text = elf.get_section_by_name(".text")
        if text is None:
            raise SystemExit("ELF has no .text section")
        text_address = int(text["sh_addr"])
        text_bytes = text.data()
        rodata = elf.get_section_by_name(".rodata")
        if rodata is None:
            raise SystemExit("ELF has no .rodata section")
        rodata_start = int(rodata["sh_addr"])
        rodata_end = rodata_start + int(rodata["sh_size"])
        exidx = elf.get_section_by_name(".ARM.exidx")
        if exidx is None:
            raise SystemExit("ELF has no .ARM.exidx section")
        exidx_address = int(exidx["sh_addr"])
        exidx_bytes = exidx.data()

    function_starts: list[int] = []
    for offset in range(0, len(exidx_bytes) - 7, 8):
        word = struct.unpack_from("<I", exidx_bytes, offset)[0]
        signed_delta = word & 0x7FFFFFFF
        if signed_delta & 0x40000000:
            signed_delta -= 0x80000000
        function_starts.append(exidx_address + offset + signed_delta)
    function_starts = sorted(set(function_starts))

    def containing_function(address: int) -> int:
        return bisect.bisect_right(function_starts, address) - 1

    matches: set[tuple[int, int, int, str]] = set()
    rodata_samples: set[tuple[int, int, int]] = set()
    literal_loads: list[tuple[int, int, int]] = []
    resolvers: dict[int, tuple[str, int]] = {}

    # Decode only the two fixed-width ARM instruction families required for
    # this pattern. This is dramatically faster than materializing millions
    # of Capstone instruction objects for the 22 MB text section.
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

        # ADD/SUB Rd, Rn, Rm with no shift. Keep cases where the inputs are PC
        # and Rd; this is the resolver half of the PIC string sequence.
        if word & 0x0E000FF0 == 0:
            opcode = (word >> 21) & 0xF
            if opcode not in {2, 4}:
                continue
            destination = (word >> 12) & 0xF
            left = (word >> 16) & 0xF
            right = word & 0xF
            if {left, right} == {15, destination}:
                resolvers[address] = ("add" if opcode == 4 else "sub", destination)

    for load_address, register, delta in literal_loads:
        for target, value in targets.items():
            for mnemonic, sign in (("add", 1), ("sub", -1)):
                resolve_address = target - sign * delta - 8
                resolver = resolvers.get(resolve_address)
                if (
                    resolver == (mnemonic, register)
                    and 0 <= resolve_address - load_address <= 64
                    and containing_function(load_address)
                    == containing_function(resolve_address)
                ):
                    matches.add((load_address, resolve_address, target, value))

        if len(rodata_samples) < args.show_rodata_samples:
            for distance in range(4, 28, 4):
                resolve_address = load_address + distance
                resolver = resolvers.get(resolve_address)
                if resolver is None or resolver[1] != register:
                    continue
                resolved = resolve_address + 8
                resolved += delta if resolver[0] == "add" else -delta
                if rodata_start <= resolved < rodata_end:
                    rodata_samples.add((load_address, resolve_address, resolved))

    for target, value in sorted(targets.items()):
        print(f"string 0x{target:08x} {value!r}")
    for load, add, target, value in sorted(matches):
        print(
            f"xref load=0x{load:08x} resolve=0x{add:08x} "
            f"target=0x{target:08x} {value!r}"
        )
    for load, add, target in sorted(rodata_samples)[: args.show_rodata_samples]:
        print(
            f"rodata-sample load=0x{load:08x} resolve=0x{add:08x} "
            f"target=0x{target:08x}"
        )
    if not matches:
        print("no references matched the recognized ARM PIC pattern")


if __name__ == "__main__":
    main()
