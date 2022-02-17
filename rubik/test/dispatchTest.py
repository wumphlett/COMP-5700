from unittest import TestCase
import rubik.dispatch as dispatch


class DispatchTest(TestCase):

    # Happy path
    #    Test that each dispatched operation returns a status element
    def test100_020ShouldVerifyInstallOfCheck(self):
        parms = {}
        parms["op"] = "check"
        result = dispatch._dispatch(parms)
        self.assertIn("status", result)

    def test100_030ShouldVerifyInstallOfSolve(self):
        parms = {}
        parms["op"] = "solve"
        result = dispatch._dispatch(parms)
        self.assertIn("status", result)

    def test100_040ShouldVerifyInstallOfInfo(self):
        parms = {}
        parms["op"] = "info"
        result = dispatch._dispatch(parms)
        self.assertIn("status", result)

    # Sad path
    #    Verify status of
    #        1) missing parm
    #        2) non-dict parm
    #        3) missing "op" keyword
    #        4) empty "op" keyword
    #        5) invalid op name

    def test100_910ShouldErrOnMissingParm(self):
        result = dispatch._dispatch()
        self.assertIn("status", result)
        self.assertEquals(result["status"], dispatch.ERROR01)

    def test100_920ShouldErrOnNoOp(self):
        parms = {}
        parms["level"] = 3
        result = dispatch._dispatch(parms)
        self.assertIn("status", result)
        self.assertEquals(result["status"], dispatch.ERROR01)

    def test100_930ShouldErrOnEmptyOp(self):
        parms = {}
        parms["op"] = ""
        result = dispatch._dispatch(parms)
        self.assertIn("status", result)
        self.assertEquals(result["status"], dispatch.ERROR03)

    def test100_940ShouldErrOnUnknownOp(self):
        parms = {}
        parms["op"] = "nop"
        result = dispatch._dispatch(parms)
        self.assertIn("status", result)
        self.assertEquals(result["status"], dispatch.ERROR03)
