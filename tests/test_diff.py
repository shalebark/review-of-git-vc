import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import diff

class Bin2DecTestCase(unittest.TestCase):

    def test_add_from_empty(self):
        result = diff.diff('tests/test_add_from_empty1', 'tests/test_add_from_empty2')
        assert(len(result['changes']) == 4)
        assert(result['changes'][0]['type'] == 'add' and result['changes'][0]['position'] == 0 and result['changes'][0]['line'] == 'a')
        assert(result['changes'][1]['type'] == 'add' and result['changes'][1]['position'] == 1 and result['changes'][1]['line'] == 'b')
        assert(result['changes'][2]['type'] == 'add' and result['changes'][2]['position'] == 2 and result['changes'][2]['line'] == 'c')
        assert(result['changes'][3]['type'] == 'add' and result['changes'][3]['position'] == 3 and result['changes'][3]['line'] == 'd')

    def test_empty_from_full(self):
        result = diff.diff('tests/test_empty_from_full1', 'tests/test_empty_from_full2')
        assert(len(result['changes']) == 1)
        assert(result['changes'][0]['type'] == 'sub')
        assert(result['changes'][0]['start_position'] == 0)
        assert(result['changes'][0]['length'] == 4)

    def test_mixed_changes(self):
        result = diff.diff('tests/test_mixed_changes_1', 'tests/test_mixed_changes_2')
        assert(len(result['changes']) == 7)
        assert(result['changes'][0]['type'] == 'add' and result['changes'][0]['position'] == 1 and result['changes'][0]['line'] == 'added line')
        assert(result['changes'][1]['type'] == 'add' and result['changes'][1]['position'] == 2 and result['changes'][1]['line'] == 'heres another')
        assert(result['changes'][2]['type'] == 'sub' and result['changes'][2]['start_position'] == 1 and result['changes'][2]['length'] == 1)
        assert(result['changes'][3]['type'] == 'add' and result['changes'][3]['position'] == 5 and result['changes'][3]['line'] == 'going to add another')
        assert(result['changes'][4]['type'] == 'add' and result['changes'][4]['position'] == 7 and result['changes'][4]['line'] == 'f line got deleted')
        assert(result['changes'][5]['type'] == 'add' and result['changes'][5]['position'] == 8 and result['changes'][5]['line'] == 'add some more')
        assert(result['changes'][6]['type'] == 'sub' and result['changes'][6]['start_position'] == 5 and result['changes'][6]['length'] == 2)

if __name__ == '__main__':
    unittest.main()

