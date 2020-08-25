import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import diff

class Bin2DecTestCase(unittest.TestCase):

    def test_add_from_empty(self):
        deltas = diff.diff_files('tests/test_add_from_empty1', 'tests/test_add_from_empty2')
        assert(len(deltas) == 5)
        assert('+1,4' in deltas[0])
        assert(deltas[1] == '+a')
        assert(deltas[2] == '+b')
        assert(deltas[3] == '+c')
        assert(deltas[4] == '+d')

    def test_empty_from_full(self):
        deltas = diff.diff_files('tests/test_empty_from_full1', 'tests/test_empty_from_full2')
        assert(len(deltas) == 5)
        assert('-1,4' in deltas[0])
        assert(deltas[1] == '-a')
        assert(deltas[2] == '-b')
        assert(deltas[3] == '-c')
        assert(deltas[4] == '-d')

    def test_mixed_changes(self):
        deltas = diff.diff_files('tests/test_mixed_changes_1', 'tests/test_mixed_changes_2')
        assert(len(deltas) == 11)
        assert('+2,2' in deltas[0])
        assert(deltas[1] == '-b')
        assert(deltas[2] == '+added line')
        assert(deltas[3] == '+heres another')
        assert('+6' in deltas[4])
        assert(deltas[5] == '+going to add another')
        assert('+8,2' in deltas[6])
        assert(deltas[7] == '-f')
        assert(deltas[8] == '-g')
        assert(deltas[9] == '+f line got deleted')
        assert(deltas[10] == '+add some more')

    def test_diff_buffer(self):
        deltas = diff.diff_files('tests/test_mixed_changes_1', 'tests/test_mixed_changes_2')
        result = diff.diff_buff(deltas)
        expected_result = None
        with open('tests/mixed_output_result') as f:
            expected_result = f.read()
        assert(result.strip() == expected_result.strip())

    def test_diff_read(self):
        buffer = None
        with open('tests/mixed_output_result') as f:
            buffer = f.read()
        deltas = diff.read_deltas_buffer(buffer)
        assert(len(deltas) == 11)
        assert('+2,2' in deltas[0])
        assert(deltas[1] == '-b')
        assert(deltas[2] == '+added line')
        assert(deltas[3] == '+heres another')
        assert('+6' in deltas[4])
        assert(deltas[5] == '+going to add another')
        assert('+8,2' in deltas[6])
        assert(deltas[7] == '-f')
        assert(deltas[8] == '-g')
        assert(deltas[9] == '+f line got deleted')
        assert(deltas[10] == '+add some more')

if __name__ == '__main__':
    unittest.main()

