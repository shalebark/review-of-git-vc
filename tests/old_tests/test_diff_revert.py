import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import diff
import diff_revert

class DiffRevertTestCase(unittest.TestCase):

    def test_diff_revert_add(self):
        with open('tests/test_add_from_empty1') as ff, open('tests/test_add_from_empty2') as tf:
            fb = ff.read()
            tb = tf.read()
        deltas = diff.diff(fb, tb)
        result = diff_revert.diff_revert(tb, deltas)
        assert(result == fb)

    def test_diff_revert_remove(self):
        with open('tests/test_empty_from_full1') as ff, open('tests/test_empty_from_full2') as tf:
            fb = ff.read()
            tb = tf.read()
        deltas = diff.diff(fb, tb)
        result = diff_revert.diff_revert(tb, deltas)
        assert(result == fb)

    def test_diff_revert_mixed(self):
        result_buffer = diff_revert.diff_revert_file('tests/test_mixed_changes_2', 'tests/mixed_output_result')
        with open('tests/test_mixed_changes_1') as f:
            expected_result_buffer = f.read()
        assert(result_buffer == expected_result_buffer)

if __name__ == '__main__':
    unittest.main()

