import rubik.check as check
import rubik.solve as solve
import rubik.info as info

ERROR01 = "error: no op is specified"
ERROR02 = "error: parameter is not a dictionary"
ERROR03 = "error: op is not legal"
STATUS = "status"
OP = "op"
OPS = {
    "check": check._check,
    "solve": solve._solve,
    "info": info._info,
}


def _dispatch(parms=None):

    result = {}

    # Validate parm
    if parms == None:
        result = {STATUS: ERROR01}
    elif not (isinstance(parms, dict)):
        result = {STATUS: ERROR02}
    elif not (OP in parms):
        result = {STATUS: ERROR01}
    elif not (parms[OP] in OPS):
        result[STATUS] = ERROR03
    else:
        result = OPS[parms[OP]](parms)
    return result
