import tempfile
import unittest
from pathlib import Path

from patch_arm_word import parse_hex_word


class ParseHexWordTests(unittest.TestCase):
    def test_accepts_four_bytes(self) -> None:
        self.assertEqual(parse_hex_word("f0 00 f0 e7"), b"\xf0\x00\xf0\xe7")

    def test_rejects_wrong_size(self) -> None:
        with self.assertRaises(Exception):
            parse_hex_word("00")


if __name__ == "__main__":
    unittest.main()
