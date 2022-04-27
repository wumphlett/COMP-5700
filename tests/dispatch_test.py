from unittest import TestCase

from rubik.dispatch import dispatch


class DispatchTest(TestCase):
    def test_check_present(self):
        params = {"op": "check"}
        result = dispatch(params)
        self.assertIn("status", result)

    def test_solve_present(self):
        params = {"op": "solve"}
        result = dispatch(params)
        self.assertIn("status", result)

    def test_info_present(self):
        params = {"op": "info"}
        result = dispatch(params)
        self.assertIn("status", result)

    def test_missing_param(self):
        result = dispatch()
        self.assertIn("status", result)
        self.assertEqual(result["status"], "error: no parameters are given")

    def test_missing_op(self):
        params = {"level": 3}
        result = dispatch(params)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "error: no op is specified")

    def test_empty_op(self):
        params = {"op": ""}
        result = dispatch(params)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "error: no op is specified")

    def test_unknown_op(self):
        params = {"op": "nop"}
        result = dispatch(params)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "error: op is not legal")
