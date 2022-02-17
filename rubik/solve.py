import rubik.cube as rubik


def _solve(parms):
    result = {}
    encodedCube = parms.get("cube", None)  # get "cube" parameter if present
    result["solution"] = "FfRrBbLlUuDd"  # example rotations
    result["status"] = "ok"
    return result
