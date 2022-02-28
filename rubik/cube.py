from copy import deepcopy
from math import sqrt


"""Given in the form {<rotation char>: (<layer method>, <axis orientation>)}

If one wished to change the mapping of key to layer, that can be done here.
"""
FACES = {
    "f": ("_front", "+y"),
    "r": ("_right", "+x"),
    "b": ("_back", "-y"),
    "l": ("_left", "-x"),
    "u": ("_up", "+z"),
    "d": ("_down", "-z"),
}


class Cubelet:
    """A class representing the cubelets that compose a rubik's cube."""
    def __init__(self):
        self.x_pos, self.x_neg, self.y_pos, self.y_neg, self.z_pos, self.z_neg = "", "", "", "", "", ""

    def rotate(self, normal: str, clockwise: bool) -> "Cubelet":
        """Rotate the individual cubelet.

        Args:
            normal (str): The axis and orientation normal to the plane being rotated.
            clockwise (bool): Whether the rotation being performed is clockwise from the viewer's point of view.

        Returns:
            Itself.
        """
        clockwise = clockwise if normal[0] == "+" else not clockwise
        normal = normal[1]
        if normal == "x":
            if clockwise:
                self.z_pos, self.y_neg, self.z_neg, self.y_pos = self.y_pos, self.z_pos, self.y_neg, self.z_neg
            else:
                self.z_pos, self.y_neg, self.z_neg, self.y_pos = self.y_neg, self.z_neg, self.y_pos, self.z_pos
        elif normal == "y":
            if clockwise:
                self.z_pos, self.x_neg, self.z_neg, self.x_pos = self.x_neg, self.z_neg, self.x_pos, self.z_pos
            else:
                self.z_pos, self.x_neg, self.z_neg, self.x_pos = self.x_pos, self.z_pos, self.x_neg, self.z_neg
        elif normal == "z":
            if clockwise:
                self.y_neg, self.x_pos, self.y_pos, self.x_neg = self.x_neg, self.y_neg, self.x_pos, self.y_pos
            else:
                self.y_neg, self.x_pos, self.y_pos, self.x_neg = self.x_pos, self.y_pos, self.x_neg, self.y_neg
        return self

    def replace(self, other: "Cubelet") -> None:
        """Replace the cubelet's attributes with that of another cubelet.

        Notes:
            This is required to allow for rotations of the cube from any plane perpendicular to the axis.
        """
        for attr in self.__dict__.keys():
            setattr(self, attr, getattr(other, attr))


class Cube:
    """A class representing a rubik's cube.

    Cube can represent any nth rubik's cube, meaning you can have a 3x3 cube, 5x5 cube, etc.
    The degree of the rubik's cube is determined from the input string, where (n^2) * 6 = len(input_string)

    Attributes:
        n (int): Which nth rubik's cube is represented. e.g. if n = 3 then one side of the cube is a 3x3 square.

    Notes:
        The cube is defined along the x, y, and z axis. If you were looking at the corner of the rubik's cube that joins
        the front, right, and top faces, the x-axis would extend normal to the right faces, the y-axis normal to the
        front, and z-axis normal to the top.
    """
    def __init__(self, cube_str: str):
        self.n = int(sqrt(len(cube_str) // 6))
        self._cube = [[[Cubelet() for _ in range(self.n)] for _ in range(self.n)] for _ in range(self.n)]

        # Initialize every cubelet of the cube given the input string
        front, offset = self._front(), 0
        for i in range(self.n ** 2):
            front[i // self.n][i % self.n].y_pos = cube_str[i + offset]
        right, offset = self._right(), self.n ** 2
        for i in range(self.n ** 2):
            right[i // self.n][i % self.n].x_pos = cube_str[i + offset]
        back, offset = self._back(), self.n ** 2 * 2
        for i in range(self.n ** 2):
            back[i // self.n][i % self.n].y_neg = cube_str[i + offset]
        left, offset = self._left(), self.n ** 2 * 3
        for i in range(self.n ** 2):
            left[i // self.n][i % self.n].x_neg = cube_str[i + offset]
        up, offset = self._up(), self.n ** 2 * 4
        for i in range(self.n ** 2):
            up[i // self.n][i % self.n].z_pos = cube_str[i + offset]
        down, offset = self._down(), self.n ** 2 * 5
        for i in range(self.n ** 2):
            down[i // self.n][i % self.n].z_neg = cube_str[i + offset]

    def __str__(self) -> str:
        return (
            "".join(str(cuboid.y_pos) for row in self._front() for cuboid in row)
            + "".join(str(cuboid.x_pos) for row in self._right() for cuboid in row)
            + "".join(str(cuboid.y_neg) for row in self._back() for cuboid in row)
            + "".join(str(cuboid.x_neg) for row in self._left() for cuboid in row)
            + "".join(str(cuboid.z_pos) for row in self._up() for cuboid in row)
            + "".join(str(cuboid.z_neg) for row in self._down() for cuboid in row)
        )

    def rotate(self, face: str, offset: int = 0, rotations: int = 1) -> None:
        """Rotate a layer in the cube.

        First select the face representing your point of view of the cube. Valid choices are defined in FACES.
        Next, you may specify an offset from the top-most face of your viewpoint. If you are looking at the front face
        and specify an offset of 1, you would be rotating the face directly under the one you're looking at. Lastly,
        you may specify the number of rotations. By default, this is 1 and represents a 90-degree turn, however this can
        be any positive integer representing a number of 90-degree turns.

        Args:
            face (str): The face to rotate based on (uppercase means rotate clock-wise).
            offset (int): The zero-indexed offset to determine the layer to rotate from the face.
            rotations (int): The number of rotations to perform.
        """
        if not FACES.get(face.lower()):
            raise ValueError("The face specified for rotation is not present in " + str(list(FACES.keys())))
        if offset < 0 or offset >= self.n:
            raise ValueError(f"The offset specified must be between 0 <= offset < {self.n}")
        if rotations < 0:
            raise ValueError("The rotation specified must be greater than 0")

        normal = FACES.get(face.lower())[1]
        layer = getattr(self, FACES.get(face.lower())[0])(offset)
        clockwise = face.isupper()

        for _ in range(rotations):
            for x in range(0, self.n // 2):
                for y in range(x, self.n-x-1):
                    temp = deepcopy(layer[x][y].rotate(normal, clockwise))
                    if clockwise:
                        layer[x][y].replace(layer[self.n-y-1][x].rotate(normal, clockwise))
                        layer[self.n-y-1][x].replace(layer[self.n-x-1][self.n-y-1].rotate(normal, clockwise))
                        layer[self.n-x-1][self.n-y-1].replace(layer[y][self.n-x-1].rotate(normal, clockwise))
                        layer[y][self.n-x-1].replace(temp)
                    else:
                        layer[x][y].replace(layer[y][self.n-x-1].rotate(normal, clockwise))
                        layer[y][self.n-x-1].replace(layer[self.n-x-1][self.n-y-1].rotate(normal, clockwise))
                        layer[self.n-x-1][self.n-y-1].replace(layer[self.n-y-1][x].rotate(normal, clockwise))
                        layer[self.n-y-1][x].replace(temp)

    def is_solved(self) -> bool:
        """Check if every face of the cube consists of the same character and return the result.

        Returns:
            If the cube is solved. True if so, false otherwise.
        """
        return (
            len(set(str(cuboid.y_pos) for row in self._front() for cuboid in row))
            + len(set(str(cuboid.x_pos) for row in self._right() for cuboid in row))
            + len(set(str(cuboid.y_neg) for row in self._back() for cuboid in row))
            + len(set(str(cuboid.x_neg) for row in self._left() for cuboid in row))
            + len(set(str(cuboid.z_pos) for row in self._up() for cuboid in row))
            + len(set(str(cuboid.z_neg) for row in self._down() for cuboid in row))
        ) == 6

    def is_adjacency_safe(self) -> bool:
        if self.n % 2 != 1:
            raise ValueError("The parity of the cube's nth degree must be odd to perform an adjacency check")

        mid = self.n // 2
        invalid_colors = {}

        front, back = self._cube[mid][self.n-1][mid].y_pos, self._cube[mid][0][mid].y_neg
        invalid_colors[front], invalid_colors[back] = back, front
        left, right = self._cube[mid][mid][0].x_neg, self._cube[mid][mid][self.n-1].x_pos
        invalid_colors[left], invalid_colors[right] = right, left
        up, down = self._cube[self.n-1][mid][mid].z_pos, self._cube[0][mid][mid].z_neg
        invalid_colors[up], invalid_colors[down] = down, up

        for plane in self._cube:
            for row in plane:
                for cubelet in row:
                    cubelet = set(cubelet.__dict__.values())
                    for color in cubelet:
                        if color and invalid_colors.get(color, None) in cubelet:
                            return False
        return True

    def _front(self, offset: int = 0):
        """Obtain a layer respective to the front of the cube."""
        return self._xz_plane(self.n - 1 - offset)[::-1]

    def _right(self, offset: int = 0):
        """Obtain a layer respective to the right of the cube."""
        return [row[::-1] for row in self._yz_plane(self.n - 1 - offset)[::-1]]

    def _back(self, offset: int = 0):
        """Obtain a layer respective to the back of the cube."""
        return [row[::-1] for row in self._xz_plane(0 + offset)[::-1]]

    def _left(self, offset: int = 0):
        """Obtain a layer respective to the left of the cube."""
        return self._yz_plane(0 + offset)[::-1]

    def _up(self, offset: int = 0):
        """Obtain a layer respective to the top of the cube."""
        return self._xy_plane(self.n - 1 - offset)

    def _down(self, offset: int = 0):
        """Obtain a layer respective to the bottom of the cube."""
        return self._xy_plane(0 + offset)[::-1]

    def _xy_plane(self, z):
        """Obtain a plane parallel to the x and y axis."""
        return self._cube[z]

    def _yz_plane(self, x):
        """Obtain a plane parallel to the y and z axis."""
        return [[row[x] for row in plane] for plane in self._cube]

    def _xz_plane(self, y):
        """Obtain a plane parallel to the x and z axis."""
        return [plane[y] for plane in self._cube]


"""
BELOW IS THE IMPLEMENTATION OF RUBIK'S CUBE USING 2D ARRAYS FOR EACH FACE. THIS IS NO LONGER WHAT I'M USING FOR THE
PROJECT BUT HAS BEEN KEPT BELOW FOR RECORD KEEPING.
"""
FACE_NAMES = ("front", "right", "back", "left", "up", "down")
OPERATIONS = {name[0]: name for name in FACE_NAMES}
ADJACENT_EDGES = {
    FACE_NAMES[0]: ((42, 43, 44), (9, 12, 15), (47, 46, 45), (35, 32, 29)),
    FACE_NAMES[1]: ((44, 41, 38), (18, 21, 24), (53, 50, 47), (8, 5, 2)),
    FACE_NAMES[2]: ((38, 37, 36), (27, 30, 33), (51, 52, 53), (17, 14, 11)),
    FACE_NAMES[3]: ((36, 39, 42), (0, 3, 6), (45, 48, 51), (26, 23, 20)),
    FACE_NAMES[4]: ((20, 19, 18), (11, 10, 9), (2, 1, 0), (29, 28, 27)),
    FACE_NAMES[5]: ((6, 7, 8), (15, 16, 17), (24, 25, 26), (33, 34, 35)),
}


class Cube2D:
    def __init__(self, cube_str: str):
        self.faces = {
            face: [
                [cube_str[offset + 0], cube_str[offset + 1], cube_str[offset + 2]],
                [cube_str[offset + 3], cube_str[offset + 4], cube_str[offset + 5]],
                [cube_str[offset + 6], cube_str[offset + 7], cube_str[offset + 8]],
            ]
            for face, offset in zip(FACE_NAMES, (0, 9, 18, 27, 36, 45))
        }

    def __getitem__(self, item: int) -> str:
        return self.faces[FACE_NAMES[item // 9]][item % 9 // 3][item % 3]

    def __setitem__(self, key: int, value: str) -> None:
        self.faces[FACE_NAMES[key // 9]][key % 9 // 3][key % 3] = value

    def __repr__(self) -> str:
        result = "".join(
            f"{f[0][0]}{f[0][1]}{f[0][2]}{f[1][0]}{f[1][1]}{f[1][2]}{f[2][0]}{f[2][1]}{f[2][2]}"
            for f in (self.faces[face] for face in FACE_NAMES)
        )
        return result

    def __str__(self) -> str:
        result = "\n".join(
            face + "\n" + "\n".join(", ".join(row) for row in self.faces[face]) + "\n" for face in FACE_NAMES
        )
        return result

    def is_solved(self) -> bool:
        return all(all(self[offset] == self[offset + i] for i in range(1, 9)) for offset in (0, 9, 18, 27, 36, 45))

    def rotate(self, rotation: str) -> None:
        clockwise = rotation.isupper()
        self._rotate_face(OPERATIONS[rotation.lower()], clockwise)
        self._rotate_edges(OPERATIONS[rotation.lower()], clockwise)

    def _rotate_face(self, face_name: str, clockwise: bool):
        offset = FACE_NAMES.index(face_name) * 9
        for x in range(0, 1):
            for y in range(x, 2 - x):
                temp = self[offset + (x * 3 + y)]
                if clockwise:
                    self[offset + (x * 3 + y)] = self[offset + ((2 - y) * 3 + x)]
                    self[offset + ((2 - y) * 3 + x)] = self[offset + ((2 - x) * 3 + (2 - y))]
                    self[offset + ((2 - x) * 3 + (2 - y))] = self[offset + (y * 3 + (2 - x))]
                    self[offset + (y * 3 + (2 - x))] = temp
                else:
                    self[offset + (x * 3 + y)] = self[offset + (y * 3 + (2 - x))]
                    self[offset + (y * 3 + (2 - x))] = self[offset + ((2 - x) * 3 + (2 - y))]
                    self[offset + ((2 - x) * 3 + (2 - y))] = self[offset + ((2 - y) * 3 + x)]
                    self[offset + ((2 - y) * 3 + x)] = temp

    def _rotate_edges(self, face_name: str, clockwise: bool):
        for a, b, c, d in zip(*ADJACENT_EDGES[face_name]):
            temp = self[a]
            if clockwise:
                self[a] = self[d]
                self[d] = self[c]
                self[c] = self[b]
                self[b] = temp
            else:
                self[a] = self[b]
                self[b] = self[c]
                self[c] = self[d]
                self[d] = temp
