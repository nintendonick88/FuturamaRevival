import unittest

from patch_service_url import replace_c_string


class ReplaceCStringTests(unittest.TestCase):
    def test_replaces_once_and_preserves_length(self) -> None:
        old = b"https://retired.example/service/"
        new = b"http://10.0.2.2:8302/service/"
        original = b"before\0" + old + b"\0after"

        patched = replace_c_string(original, old, new)

        self.assertEqual(len(patched), len(original))
        self.assertNotIn(old, patched)
        self.assertIn(new + (b"\0" * (len(old) - len(new))), patched)

    def test_rejects_ambiguous_match(self) -> None:
        with self.assertRaisesRegex(ValueError, "expected one"):
            replace_c_string(b"same same", b"same", b"new")

    def test_rejects_longer_replacement(self) -> None:
        with self.assertRaisesRegex(ValueError, "longer"):
            replace_c_string(b"old", b"old", b"too-long")


if __name__ == "__main__":
    unittest.main()
