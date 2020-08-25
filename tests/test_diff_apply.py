import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import diff_apply

class DiffApplyTestCase(unittest.TestCase):

    def test_diff_apply(self):
        result_buffer = diff_apply.diff_apply_file('tests/test_mixed_changes_1', 'tests/mixed_output_result')
        with open('tests/test_mixed_changes_2') as f:
            expected_result_buffer = f.read()
        assert(result_buffer == expected_result_buffer)

if __name__ == '__main__':
    unittest.main()

