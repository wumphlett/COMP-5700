from unittest import TestCase
import rubik.check as check


class CheckTest(TestCase):
    def test_check_01_no_cube(self):
        parm = {"op": "check"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube must be provided for validation", status)

    def test_check_02_int_cube(self):
        parm = {"op": "check", "cube": 54}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube must be given as a string", status)

    def test_check_03_non_alphanum_cube(self):
        parm = {"op": "check", "cube": "******"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube must be given as a solely alphanumeric string", status)

    def test_check_04_short_cube(self):
        parm = {"op": "check", "cube": "a"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube must have exactly 54 pieces", status)

    def test_check_04_long_cube(self):
        parm = {"op": "check", "cube": "a"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube must have exactly 54 pieces", status)

    def test_check_05_too_few_colors(self):
        parm = {"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwwwwwwwwwwww"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube must have exactly 6 different colors", status)

    def test_check_05_too_many_colors(self):
        parm = {"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwwl"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube must have exactly 6 different colors", status)

    def test_check_06_improper_piece_number(self):
        parm = {"op": "check", "cube": "bbbbrrrrrrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube must have exactly 9 pieces to each color", status)

    def test_check_07_improper_centers(self):
        parm = {"op": "check", "cube": "bbbbbbbbrrrrrbrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube must have uniquely colored pieces at the center of each face", status)

    def test_check_08_failed_adjacency_check(self):
        parm = {"op": "check", "cube": "bbbbbbbbbrrrrrrgrrggggggggroooooooooyyyyyyyyywwwwwwwww"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("error: cube adjacent pieces must be valid", status)

    def test_check_09_valid_cube(self):
        parm = {"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"}
        result = check._check(parm)
        self.assertIn("status", result)
        status = result.get("status", None)
        self.assertEqual("ok", status)
