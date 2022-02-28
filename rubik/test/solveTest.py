from unittest import TestCase
import rubik.solve as solve


class SolveTest(TestCase):
    def test_solve_01_no_cube(self):
        parm = {"op": "solve"}
        result = solve._solve(parm)
        self.assertIn("status", result)
        status = result.get("status")
        # Not checking for a specific error msg as that is relegated to checkTest
        self.assertNotEqual("ok", status)

    def test_solve_02_improper_cube(self):
        parm = {"op": "solve", "cube": 6}
        result = solve._solve(parm)
        self.assertIn("status", result)
        status = result.get("status")
        # Not checking for a specific error msg as that is relegated to checkTest
        self.assertNotEqual("ok", status)

    def test_solve_03_int_rotate(self):
        parm = {"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww", "rotate": 6}
        result = solve._solve(parm)
        self.assertIn("status", result)
        status = result.get("status")
        self.assertEqual("error: rotate must be given as a string", status)

    def test_solve_04_non_alpha_rotate(self):
        parm = {"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww", "rotate": "1"}
        result = solve._solve(parm)
        self.assertIn("status", result)
        status = result.get("status")
        self.assertEqual("error: rotate must be given as a solely alphabetical string", status)

    def test_solve_05_invalid_char_rotate(self):
        parm = {"op": "check", "cube": "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww", "rotate": "xxxx"}
        result = solve._solve(parm)
        self.assertIn("status", result)
        status = result.get("status")
        self.assertEqual("error: rotate must be comprised of characters in FfRrBbLlUuDd", status)

    def test_solve_06_missing_rotate(self):
        parm = {"op": "check", "cube": "gggggggggrrrrrrrrrbbbbbbbbbooooooooowwwwwwwwwyyyyyyyyy"}
        result = solve._solve(parm)
        self.assertIn("status", result)
        status = result.get("status")
        self.assertEqual("ok", status)
        cube = result.get("cube")
        self.assertEqual("gggggggggwrrwrrwrrbbbbbbbbbooyooyooywwwwwwooorrryyyyyy", cube)

    def test_solve_07_empty_rotate(self):
        parm = {"op": "check", "cube": "gggggggggrrrrrrrrrbbbbbbbbbooooooooowwwwwwwwwyyyyyyyyy", "rotate": ""}
        result = solve._solve(parm)
        self.assertIn("status", result)
        status = result.get("status")
        self.assertEqual("ok", status)
        cube = result.get("cube")
        self.assertEqual("gggggggggwrrwrrwrrbbbbbbbbbooyooyooywwwwwwooorrryyyyyy", cube)

    def test_solve_08_valid_rotate(self):
        parm = {"op": "check", "cube": "gggggggggrrrrrrrrrbbbbbbbbbooooooooowwwwwwwwwyyyyyyyyy", "rotate": "F"}
        result = solve._solve(parm)
        self.assertIn("status", result)
        status = result.get("status")
        self.assertEqual("ok", status)
        cube = result.get("cube")
        self.assertEqual("gggggggggwrrwrrwrrbbbbbbbbbooyooyooywwwwwwooorrryyyyyy", cube)

    def test_solve_09_solve_rotate(self):
        parm = {
            "op": "check",
            "cube": "bbrgoywwgbrbgbgrbgobowrwobryyorgobrggowoygywwroyywyyrw",
            "rotate": "DbuFFUUFFrFuBDDRBBULLDRRD",
        }
        result = solve._solve(parm)
        self.assertIn("status", result)
        status = result.get("status")
        self.assertEqual("ok", status)
        cube = result.get("cube")
        self.assertEqual("ooooooooobbbbbbbbbrrrrrrrrrgggggggggyyyyyyyyywwwwwwwww", cube)
