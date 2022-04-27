from collections import Counter

from rubik.cube import Cube

ADJACENT_PIECES = [
    (0, 29, 42),
    (1, 43),
    (2, 9, 44),
    (3, 32),
    (5, 12),
    (6, 35, 45),
    (7, 46),
    (8, 15, 47),
    (10, 41),
    (11, 18, 38),
    (14, 21),
    (16, 50),
    (17, 24, 53),
    (19, 37),
    (20, 27, 36),
    (23, 30),
    (25, 52),
    (26, 33, 51),
    (28, 39),
    (34, 48),
]

OPPOSITE_FACES = [
    (4, 22),
    (13, 31),
    (40, 49),
]


def _2d_adjacency_check(cube: str) -> bool:
    """Checks if the pieces on each cuboid have valid colors given the opposing faces of the cube.

    Args:
        cube: A validated (but not necessarily solved) rubik's cube.

    Returns:
        If the cube passes the adjacent pieces check. True for pass, False otherwise.
    """
    invalid_colors = {}
    for a, b in OPPOSITE_FACES:
        invalid_colors[cube[a]] = cube[b]
        invalid_colors[cube[b]] = cube[a]
    for adjacent in ADJACENT_PIECES:
        adjacent = tuple(cube[i] for i in adjacent)
        for color in adjacent:
            if invalid_colors[color] in adjacent:
                return False
    return True


def check(params: dict) -> dict:
    result = {}
    encoded_cube = params.get("cube")
    if encoded_cube is None:
        result["status"] = "error: cube must be present"
    elif not isinstance(encoded_cube, str):
        result["status"] = "error: cube must be given as a string"
    elif not encoded_cube.isalnum():
        result["status"] = "error: cube must be given as a solely alphanumeric string"
    elif len(encoded_cube) != 54:
        result["status"] = "error: cube must have exactly 54 pieces"
    elif len((piece_counter := Counter(encoded_cube))) != 6:
        result["status"] = "error: cube must have exactly 6 different colors"
    elif any(count != 9 for count in piece_counter.values()):
        result["status"] = "error: cube must have exactly 9 pieces to each color"
    elif len(set(encoded_cube[i] for i in range(4, 54, 9))) != 6:
        result["status"] = "error: cube must have uniquely colored pieces at the center of each face"
    elif not Cube(encoded_cube).is_adjacency_safe():
        result["status"] = "error: cube adjacent pieces must be valid"
    else:
        result["status"] = "ok"
    return result
