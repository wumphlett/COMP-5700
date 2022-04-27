from rubik.check import check
from rubik.cube import Cube


ALLOWED_ROTATIONS = "FfRrBbLlUuDd"
ROTATIONS_SET = set(ALLOWED_ROTATIONS)


def solve(params):
    cube_check = check(params)
    if cube_check.get("status", "") != "ok":
        return cube_check

    rotations = params.get("rotate")
    if not rotations:
        result = {"status": "ok", "solution": Cube(params["cube"]).solve()}
    else:
        if not isinstance(rotations, str):
            result = {"status": "error: rotate must be given as a string"}
        elif not rotations.isalpha():
            result = {"status": "error: rotate must be given as a solely alphabetical string"}
        elif not all(rotation in ROTATIONS_SET for rotation in rotations):
            result = {"status": f"error: rotate must be comprised of characters in {ALLOWED_ROTATIONS}"}
        else:
            cube = Cube(params["cube"])
            for rotation in rotations:
                cube.rotate(rotation)
            result = {"status": "ok", "cube": str(cube)}
    return result
