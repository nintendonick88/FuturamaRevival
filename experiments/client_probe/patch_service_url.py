"""Create a test APK with one native service URL replaced in-place.

The original APK is never edited. The replacement must fit in the existing
NUL-terminated string so no native offsets or section sizes change.
"""

from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path


LIBRARY_PATH = "lib/armeabi-v7a/libclient.so"


def replace_c_string(data: bytes, old: bytes, new: bytes) -> bytes:
    if len(new) > len(old):
        raise ValueError("replacement URL is longer than the original URL")
    occurrences = data.count(old)
    if occurrences != 1:
        raise ValueError(f"expected one original URL, found {occurrences}")
    padded = new + (b"\0" * (len(old) - len(new)))
    return data.replace(old, padded, 1)


def patch_apk(source: Path, output: Path, old: bytes, new: bytes) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix="futurama-url-patch-", suffix=".apk", delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)

    try:
        found_library = False
        with zipfile.ZipFile(source, "r") as original, zipfile.ZipFile(
            temporary_path, "w", allowZip64=True
        ) as patched:
            for entry in original.infolist():
                contents = original.read(entry.filename)
                if entry.filename == LIBRARY_PATH:
                    contents = replace_c_string(contents, old, new)
                    found_library = True
                patched.writestr(entry, contents)
        if not found_library:
            raise ValueError(f"APK does not contain {LIBRARY_PATH}")
        shutil.move(temporary_path, output)
    finally:
        temporary_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--old", required=True)
    parser.add_argument("--new", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.source.resolve() == args.output.resolve():
        raise SystemExit("source and output APK paths must differ")
    patch_apk(args.source, args.output, args.old.encode(), args.new.encode())
    print(f"Patched test APK written to {args.output}")


if __name__ == "__main__":
    main()
