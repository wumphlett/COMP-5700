from unittest import TestCase

from rubik.solve import solve


class SolveTest(TestCase):
    def test_no_cube(self):
        result = solve({"op": "solve"})
        self.assertIn("status", result)
        # Not checking for a specific error msg as that is relegated to check_test
        self.assertNotEqual("ok", result.get("status"))

    def test_improper_cube(self):
        result = solve({"op": "solve", "cube": 6})
        self.assertIn("status", result)
        # Not checking for a specific error msg as that is relegated to check_test
        self.assertNotEqual("ok", result.get("status"))

    def test_int_rotate(self):
        result = solve({"op": "solve", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww", "rotate": 6})
        self.assertIn("status", result)
        self.assertEqual("error: rotate must be given as a string", result.get("status"))

    def test_non_alpha_rotate(self):
        result = solve({"op": "solve", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww", "rotate": "1"})
        self.assertIn("status", result)
        self.assertEqual("error: rotate must be given as a solely alphabetical string", result.get("status"))

    def test_invalid_char_rotate(self):
        result = solve(
            {"op": "solve", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww", "rotate": "xxxx"}
        )
        self.assertIn("status", result)
        self.assertEqual("error: rotate must be comprised of characters in FfRrBbLlUuDd", result.get("status"))

    def test_missing_rotate(self):
        result = solve({"op": "solve", "cube": "gggggggggrrrrrrrrrbbbbbbbbbooooooooowwwwwwwwwyyyyyyyyy"})
        self.assertIn("status", result)
        self.assertEqual("ok", result.get("status"))
        self.assertIn("solution", result)

    def test_empty_rotate(self):
        result = solve({"op": "solve", "cube": "gggggggggrrrrrrrrrbbbbbbbbbooooooooowwwwwwwwwyyyyyyyyy", "rotate": ""})
        self.assertIn("status", result)
        self.assertEqual("ok", result.get("status"))
        self.assertIn("solution", result)

    def test_valid_rotate(self):
        result = solve({"op": "solve", "cube": "gggggggggrrrrrrrrrbbbbbbbbbooooooooowwwwwwwwwyyyyyyyyy", "rotate": "F"})
        self.assertIn("status", result)
        self.assertEqual("ok", result.get("status"))
        self.assertEqual("gggggggggwrrwrrwrrbbbbbbbbbooyooyooywwwwwwooorrryyyyyy", result.get("cube"))

    def test_solve_rotate(self):
        result = solve(
            {
                "op": "solve",
                "cube": "bbrgoywwgbrbgbgrbgobowrwobryyorgobrggowoygywwroyywyyrw",
                "rotate": "DbuFFUUFFrFuBDDRBBULLDRRD",
            }
        )
        self.assertIn("status", result)
        self.assertEqual("ok", result.get("status"))
        self.assertEqual("ooooooooobbbbbbbbbrrrrrrrrrgggggggggyyyyyyyyywwwwwwwww", result.get("cube"))
