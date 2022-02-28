from unittest import TestCase
from rubik.cube import Cube


class CubeTest(TestCase):
    def test_cube_01_test_str(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        self.assertEqual(cube_str, str(cube))

    def test_cube_02_simple_rotate(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        cube.rotate("F")
        self.assertEqual("bbbbbbbbbyrryrryrrgggggggggoowoowoowyyyyyyooorrrwwwwww", str(cube))

    def test_cube_03_every_rotate(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        for rotation in "FRBLUDfrblud":
            cube.rotate(rotation)
        self.assertEqual("rbbobrbbrrwgyrggrgowoygoogwbwybogbyoygyoyrgyywwwowbrrw", str(cube))

    def test_cube_04_complete_solve(self):
        cube_str = "bbrgoywwgbrbgbgrbgobowrwobryyorgobrggowoygywwroyywyyrw"
        cube = Cube(cube_str)
        for rotation in "DbuFFUUFFrFuBDDRBBULLDRRD":
            cube.rotate(rotation)
        self.assertEqual("ooooooooobbbbbbbbbrrrrrrrrrgggggggggyyyyyyyyywwwwwwwww", str(cube))

    def test_cube_05_solve_check(self):
        cube_str = "bbrgoywwgbrbgbgrbgobowrwobryyorgobrggowoygywwroyywyyrw"
        cube = Cube(cube_str)
        self.assertFalse(cube.is_solved())
        for rotation in "DbuFFUUFFrFuBDDRBBULLDRRD":
            cube.rotate(rotation)
        self.assertTrue(cube.is_solved())
