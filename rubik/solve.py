from rubik.check import _check
from rubik.cube import Cube


ALLOWED_ROTATIONS = set("FfRrBbLlUuDd")


def _solve(parms):
    if (cube_result := _check(parms)).get("status") != "ok":
        return cube_result

    result = {}
    rotations = parms.get("rotate")
    if not rotations:
        rotations = "F"

    if not isinstance(rotations, str):
        result["status"] = "error: rotate must be given as a string"
    elif not rotations.isalpha():
        result["status"] = "error: rotate must be given as a solely alphabetical string"
    elif not all(rotation in ALLOWED_ROTATIONS for rotation in rotations):
        result["status"] = "error: rotate must be comprised of characters in FfRrBbLlUuDd"
    else:
        cube = Cube(parms.get("cube"))
        for rotation in rotations:
            cube.rotate(rotation)
        result["status"] = "ok"
        result["cube"] = str(cube)
    return result
