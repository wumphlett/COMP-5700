from unittest import TestCase

from rubik.check import check


class CheckTest(TestCase):
    def test_no_cube(self):
        result = check({"op": "check"})
        self.assertIn("status", result)
        self.assertEqual("error: cube must be present", result.get("status"))

    def test_int_cube(self):
        result = check({"op": "check", "cube": 54})
        self.assertIn("status", result)
        self.assertEqual("error: cube must be given as a string", result.get("status"))

    def test_non_alphanum_cube(self):
        result = check({"op": "check", "cube": "******"})
        self.assertIn("status", result)
        self.assertEqual("error: cube must be given as a solely alphanumeric string", result.get("status"))

    def test_short_cube(self):
        result = check({"op": "check", "cube": "a"})
        self.assertIn("status", result)
        self.assertEqual("error: cube must have exactly 54 pieces", result.get("status"))

    def test_long_cube(self):
        result = check({"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwwwaaaaaaaaa"})
        self.assertIn("status", result)
        self.assertEqual("error: cube must have exactly 54 pieces", result.get("status"))

    def test_too_few_colors_cube(self):
        result = check({"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwwwwwwwwwwww"})
        self.assertIn("status", result)
        self.assertEqual("error: cube must have exactly 6 different colors", result.get("status"))

    def test_too_many_colors_cube(self):
        result = check({"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwwl"})
        self.assertIn("status", result)
        self.assertEqual("error: cube must have exactly 6 different colors", result.get("status"))

    def test_improper_piece_number_cube(self):
        result = check({"op": "check", "cube": "bbbbrrrrrrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"})
        self.assertIn("status", result)
        self.assertEqual("error: cube must have exactly 9 pieces to each color", result.get("status"))

    def test_improper_centers_cube(self):
        result = check({"op": "check", "cube": "bbbbbbbbrrrrrbrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"})
        self.assertIn("status", result)
        self.assertEqual(
            "error: cube must have uniquely colored pieces at the center of each face", result.get("status")
        )

    def test_adjacency_unsafe_cube(self):
        result = check({"op": "check", "cube": "bbbbbbbbbrrrrrrgrrggggggggroooooooooyyyyyyyyywwwwwwwww"})
        self.assertIn("status", result)
        self.assertEqual("error: cube adjacent pieces must be valid", result.get("status"))

    def test_valid_cube(self):
        result = check({"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"})
        self.assertIn("status", result)
        self.assertEqual("ok", result.get("status"))
