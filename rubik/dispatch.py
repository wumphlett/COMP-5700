from rubik.check import check
from rubik.info import info
from rubik.solve import solve


OPS = {
    "check": check,
    "info": info,
    "solve": solve,
}


def dispatch(params: dict = None):
    if params is None:
        result = {"status": "error: no parameters are given"}
    elif not isinstance(params, dict):
        result = {"status": "error: parameter is not a dictionary"}
    elif not params.get("op"):
        result = {"status": "error: no op is specified"}
    elif params["op"] not in OPS:
        result = {"status": "error: op is not legal"}
    else:
        result = OPS[params["op"]](params)
    return result
