"""Regression checks that invalid descent claims cannot pass offline inspection."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

from check import ROOT, verify


class RejectionChecks(unittest.TestCase):
    def test_wrong_exact_valuation(self):
        with self.assertRaisesRegex(ValueError, 'valuation mismatch'):
            verify((4, 9, (3,)))

    def test_valuation_pattern_not_stable_on_class(self):
        with self.assertRaisesRegex(ValueError, 'unstable valuation pattern'):
            verify((3, 5, (4,)))

    def test_noncontractive_affine_map(self):
        with self.assertRaisesRegex(ValueError, 'noncontractive'):
            verify((3, 3, (1,)))

    def test_contraction_alone_does_not_imply_strict_descent(self):
        # The orbit 1 -> 1 has coefficient 3/4 but positive constant 1/4.
        with self.assertRaisesRegex(ValueError, 'no descent'):
            verify((3, 1, (2,)))

    def test_duplicate_json_keys_rejected(self):
        spec = importlib.util.spec_from_file_location('public_eval_test', ROOT/'public-hill/eval.py')
        evaluator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator)
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp)/'solution.json').write_text('{"rules":[],"rules":[]}')
            with self.assertRaisesRegex(ValueError, 'duplicate JSON object key'):
                evaluator._load_rules(Path(tmp))


if __name__ == '__main__':
    unittest.main()
