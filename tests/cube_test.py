from unittest import TestCase

from rubik.cube import Cube


class CubeTest(TestCase):
    def test_str(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        self.assertEqual(cube_str, str(cube))

    def test_simple_rotate(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        cube.rotate("F")
        self.assertEqual("bbbbbbbbbyrryrryrrgggggggggoowoowoowyyyyyyooorrrwwwwww", str(cube))

    def test_every_rotate(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        for rotation in "FRBLUDfrblud":
            cube.rotate(rotation)
        self.assertEqual("rbbobrbbrrwgyrggrgowoygoogwbwybogbyoygyoyrgyywwwowbrrw", str(cube))

    def test_complete_solve(self):
        cube_str = "bbrgoywwgbrbgbgrbgobowrwobryyorgobrggowoygywwroyywyyrw"
        cube = Cube(cube_str)
        for rotation in "DbuFFUUFFrFuBDDRBBULLDRRD":
            cube.rotate(rotation)
        self.assertEqual("ooooooooobbbbbbbbbrrrrrrrrrgggggggggyyyyyyyyywwwwwwwww", str(cube))

    def test_rotations_to_solve(self):
        cube_str = "bbrgoywwgbrbgbgrbgobowrwobryyorgobrggowoygywwroyywyyrw"
        cube = Cube(cube_str)
        self.assertFalse(cube.is_solved())
        for rotation in "DbuFFUUFFrFuBDDRBBULLDRRD":
            cube.rotate(rotation)
        self.assertTrue(cube.is_solved())

    def test_scramble(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        cube.scramble()
        self.assertNotEqual(cube_str, str(cube))
        self.assertTrue(cube.is_adjacency_safe())
        self.assertFalse(cube.is_solved())

    def test_bottom_cross(self):
        scrambled_cube = "gwbbbwgwboryorgrrrbbyogggbygyoyoybgyorroygwrwrbwwwyoow"
        cube = Cube(scrambled_cube)
        cube._bottom_cross()
        self.assertTrue(cube.is_bottom_crossed())
        daisyed_cube = "yowgbobygggogrgybywrbygybbwrbgborgrwywbwywrwrrooywrooo"
        cube = Cube(daisyed_cube)
        cube._bottom_cross()
        self.assertTrue(cube.is_bottom_crossed())
        bottom_crossed_cube = "gboobybbgwbbbrgyryrygyggbgwyrwroggowroyyyrrobrwowwwowo"
        cube = Cube(bottom_crossed_cube)
        self.assertEqual("", cube._bottom_cross())
        self.assertTrue(cube.is_bottom_crossed())

    def test_bottom_layer(self):
        scrambled_cube = "ygwybrowbbrwyrboggrborgowoyywgyobroggobrygryowbygwwbwr"
        cube = Cube(scrambled_cube)
        cube._bottom_layer()
        self.assertTrue(cube.is_bottom_layered())
        bottom_crossed_cube = "bbbgbyobwwybgrrrryyyybgboggroyyoroowgrogyororbwgwwwwwg"
        cube = Cube(bottom_crossed_cube)
        cube._bottom_layer()
        self.assertTrue(cube.is_bottom_layered())
        solved_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(solved_cube)
        self.assertEqual("", cube._bottom_layer())
        self.assertTrue(cube.is_bottom_layered())

    def test_middle_layer(self):
        scrambled_cube = "ygwybrowbbrwyrboggrborgowoyywgyobroggobrygryowbygwwbwr"
        cube = Cube(scrambled_cube)
        cube._middle_layer()
        self.assertTrue(cube.is_middle_layered())
        bottom_layered_cube = "bgrrbobbbyyrgrrrrrgyyggbggggroooboooobyyyoyybwwwwwwwww"
        cube = Cube(bottom_layered_cube)
        cube._middle_layer()
        self.assertTrue(cube.is_middle_layered())
        solved_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(solved_cube)
        self.assertEqual("", cube._middle_layer())
        self.assertTrue(cube.is_middle_layered())

    def test_top_cross(self):
        scrambled_cube = "ygwybrowbbrwyrboggrborgowoyywgyobroggobrygryowbygwwbwr"
        cube = Cube(scrambled_cube)
        cube._top_cross()
        self.assertTrue(cube.is_top_crossed())
        middle_layered_cube = "bbgbbbbbbyorrrrrrrygoggggggyrooooooogybyyyyyrwwwwwwwww"
        cube = Cube(middle_layered_cube)
        cube._top_cross()
        self.assertTrue(cube.is_top_crossed())
        solved_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(solved_cube)
        self.assertEqual("", cube._top_cross())
        self.assertTrue(cube.is_top_crossed())

    def test_top_surface(self):
        scrambled_cube = "ygwybrowbbrwyrboggrborgowoyywgyobroggobrygryowbygwwbwr"
        cube = Cube(scrambled_cube)
        cube._top_surface()
        self.assertTrue(cube.is_top_surfaced())
        top_crossed_cube = "bgrbbbbbbgogrrrrrrobbggggggrroooooooyyyyyyyyywwwwwwwww"
        cube = Cube(top_crossed_cube)
        cube._top_surface()
        self.assertTrue(cube.is_top_surfaced())
        solved_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(solved_cube)
        self.assertEqual("", cube._top_surface())
        self.assertTrue(cube.is_top_surfaced())

    def test_top_corners(self):
        scrambled_cube = "ygwybrowbbrwyrboggrborgowoyywgyobroggobrygryowbygwwbwr"
        cube = Cube(scrambled_cube)
        cube._top_corners()
        self.assertTrue(cube.is_top_cornered())
        top_surfaced_cube = "bbbbbbbbbrorrrrrrrgrgggggggogoooooooyyyyyyyyywwwwwwwww"
        cube = Cube(top_surfaced_cube)
        cube._top_corners()
        self.assertTrue(cube.is_top_cornered())
        solved_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(solved_cube)
        self.assertEqual("", cube._top_corners())
        self.assertTrue(cube.is_top_cornered())

    def test_top_layer(self):
        scrambled_cube = "ygwybrowbbrwyrboggrborgowoyywgyobroggobrygryowbygwwbwr"
        cube = Cube(scrambled_cube)
        cube._top_layer()
        self.assertTrue(cube.is_solved())
        top_cornered_cube = "bobbbbbbbrrrrrrrrrgbgggggggogoooooooyyyyyyyyywwwwwwwww"
        cube = Cube(top_cornered_cube)
        cube._top_layer()
        self.assertTrue(cube.is_solved())
        solved_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(solved_cube)
        self.assertEqual("", cube._top_layer())
        self.assertTrue(cube.is_solved())

    def test_solve(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        cube.scramble()
        scrambled_cube = str(cube)
        solution = cube.solve()
        self.assertTrue(isinstance(solution, str))
        cube_str = str(cube)
        self.assertTrue(cube.is_solved())
        scrambled_cube = Cube(scrambled_cube)
        for rotation in solution:
            scrambled_cube.rotate(rotation)
        self.assertEqual(cube_str, str(scrambled_cube))

    def test_solve_stress_test(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        for _ in range(1000):
            cube = Cube(cube_str)
            cube.scramble(50)
            scrambled_cube = str(cube)
            self.assertFalse(cube.is_solved())
            solution = cube.solve()
            self.assertTrue(cube.is_solved())
            cube_str = str(cube)
            scrambled_cube = Cube(scrambled_cube)
            for rotation in solution:
                scrambled_cube.rotate(rotation)
            self.assertEqual(cube_str, str(scrambled_cube))

    def test_already_solved(self):
        cube_str = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        solution = cube.solve()
        self.assertEqual("", solution)

    def test_is_adjacency_safe(self):
        cube_str = "bbbbbbbbbrrrrrrgrrggggggggroooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(cube_str)
        self.assertFalse(cube.is_adjacency_safe())
        cube_str = "bbrgoywwgbrbgbgrbgobowrwobryyorgobrggowoygywwroyywyyrw"
        cube = Cube(cube_str)
        self.assertTrue(cube.is_adjacency_safe())

    def test_is_bottom_crossed(self):
        scrambled_cube = "gwbbbwgwboryorgrrrbbyogggbygyoyoybgyorroygwrwrbwwwyoow"
        cube = Cube(scrambled_cube)
        self.assertFalse(cube.is_bottom_crossed())
        only_bottom_face_cube = "gboobybrgwbbbrgygyrygyggbowyrwroggbwroyyyrrobrwowwwowo"
        cube = Cube(only_bottom_face_cube)
        self.assertFalse(cube.is_bottom_crossed())
        only_edges_cube = "gboobybbgwbbbrgyryrygyggbgwyrwroggowroyyyrrobrXoXwXoXo"
        cube = Cube(only_edges_cube)
        self.assertFalse(cube.is_bottom_crossed())
        bottom_crossed_cube = "gboobybbgwbbbrgyryrygyggbgwyrwroggowroyyyrrobrwowwwowo"
        cube = Cube(bottom_crossed_cube)
        self.assertTrue(cube.is_bottom_crossed())

    def test_is_bottom_layered(self):
        scrambled_cube = "gwbbbwgwboryorgrrrbbyogggbygyoyoybgyorroygwrwrbwwwyoow"
        cube = Cube(scrambled_cube)
        self.assertFalse(cube.is_bottom_layered())
        only_bottom_face_cube = "bbbbbbbXbrrrrrrrXrgggggggXgoooooooXoyyyyyyyyywwwwwwwww"
        cube = Cube(only_bottom_face_cube)
        self.assertFalse(cube.is_bottom_layered())
        only_edges_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyyXwwwwwwww"
        cube = Cube(only_edges_cube)
        self.assertFalse(cube.is_bottom_layered())
        bottom_layered_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(bottom_layered_cube)
        self.assertTrue(cube.is_bottom_layered())

    def test_is_middle_layered(self):
        scrambled_cube = "gwbbbwgwboryorgrrrbbyogggbygyoyoybgyorroygwrwrbwwwyoow"
        cube = Cube(scrambled_cube)
        self.assertFalse(cube.is_middle_layered())
        only_bottom_face_cube = "bbbbbbbXbrrrrrrrXrgggggggXgoooooooXoyyyyyyyyywwwwwwwww"
        cube = Cube(only_bottom_face_cube)
        self.assertFalse(cube.is_middle_layered())
        only_edges_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyyXwwwwwwww"
        cube = Cube(only_edges_cube)
        self.assertFalse(cube.is_middle_layered())
        bottom_layered_cube = "bgrrbobbbyyrgrrrrrgyyggbggggroooboooobyyyoyybwwwwwwwww"
        cube = Cube(bottom_layered_cube)
        self.assertFalse(cube.is_middle_layered())
        middle_layered_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(middle_layered_cube)
        self.assertTrue(cube.is_middle_layered())

    def test_is_top_crossed(self):
        scrambled_cube = "gwbbbwgwboryorgrrrbbyogggbygyoyoybgyorroygwrwrbwwwyoow"
        cube = Cube(scrambled_cube)
        self.assertFalse(cube.is_top_crossed())
        only_bottom_face_cube = "bbbbbbbXbrrrrrrrXrgggggggXgoooooooXoyyyyyyyyywwwwwwwww"
        cube = Cube(only_bottom_face_cube)
        self.assertFalse(cube.is_top_crossed())
        only_edges_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyyXwwwwwwww"
        cube = Cube(only_edges_cube)
        self.assertFalse(cube.is_top_crossed())
        bottom_layered_cube = "bgrrbobbbyyrgrrrrrgyyggbggggroooboooobyyyoyybwwwwwwwww"
        cube = Cube(bottom_layered_cube)
        self.assertFalse(cube.is_top_crossed())
        middle_layered_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyXyXyXyXywwwwwwwww"
        cube = Cube(middle_layered_cube)
        self.assertFalse(cube.is_top_crossed())
        top_crossed_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(top_crossed_cube)
        self.assertTrue(cube.is_top_crossed())

    def test_is_top_surfaced(self):
        scrambled_cube = "gwbbbwgwboryorgrrrbbyogggbygyoyoybgyorroygwrwrbwwwyoow"
        cube = Cube(scrambled_cube)
        self.assertFalse(cube.is_top_surfaced())
        only_bottom_face_cube = "bbbbbbbXbrrrrrrrXrgggggggXgoooooooXoyyyyyyyyywwwwwwwww"
        cube = Cube(only_bottom_face_cube)
        self.assertFalse(cube.is_top_surfaced())
        only_edges_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyyXwwwwwwww"
        cube = Cube(only_edges_cube)
        self.assertFalse(cube.is_top_surfaced())
        bottom_layered_cube = "bgrrbobbbyyrgrrrrrgyyggbggggroooboooobyyyoyybwwwwwwwww"
        cube = Cube(bottom_layered_cube)
        self.assertFalse(cube.is_top_surfaced())
        middle_layered_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyXyXyXyXywwwwwwwww"
        cube = Cube(middle_layered_cube)
        self.assertFalse(cube.is_top_surfaced())
        top_crossed_cube = "bbbbbbbbbrrrrrrrrrgggggggggooooooooooXyXyyyyywwwwwwwww"
        cube = Cube(top_crossed_cube)
        self.assertFalse(cube.is_top_surfaced())
        top_surfaced_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(top_surfaced_cube)
        self.assertTrue(cube.is_top_surfaced())

    def test_is_top_cornered(self):
        scrambled_cube = "gwbbbwgwboryorgrrrbbyogggbygyoyoybgyorroygwrwrbwwwyoow"
        cube = Cube(scrambled_cube)
        self.assertFalse(cube.is_top_cornered())
        only_bottom_face_cube = "bbbbbbbXbrrrrrrrXrgggggggXgoooooooXoyyyyyyyyywwwwwwwww"
        cube = Cube(only_bottom_face_cube)
        self.assertFalse(cube.is_top_cornered())
        only_edges_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyyXwwwwwwww"
        cube = Cube(only_edges_cube)
        self.assertFalse(cube.is_top_cornered())
        bottom_layered_cube = "bgrrbobbbyyrgrrrrrgyyggbggggroooboooobyyyoyybwwwwwwwww"
        cube = Cube(bottom_layered_cube)
        self.assertFalse(cube.is_top_cornered())
        middle_layered_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyXyXyXyXywwwwwwwww"
        cube = Cube(middle_layered_cube)
        self.assertFalse(cube.is_top_cornered())
        top_crossed_cube = "bbbbbbbbbrrrrrrrrrgggggggggooooooooooXyXyyyyywwwwwwwww"
        cube = Cube(top_crossed_cube)
        self.assertFalse(cube.is_top_cornered())
        top_surfaced_cube = "Xbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(top_surfaced_cube)
        self.assertFalse(cube.is_top_cornered())
        top_surfaced_cube = "bbbbbbbbbrrrrrrrrrgggggggggoooooooooyyyyyyyyywwwwwwwww"
        cube = Cube(top_surfaced_cube)
        self.assertTrue(cube.is_top_cornered())

    def test_is_solved(self):
        pass
