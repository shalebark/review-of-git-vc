import unittest
import os
import sys
import shutil
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import CONSTANTS
import init
import update_index
import list_index
import check_modified

class IndexTestCase(unittest.TestCase):

    def test_index_functions(self):
        if os.path.exists(CONSTANTS.PATH.BASE_DIRECTORY):
            shutil.rmtree(CONSTANTS.PATH.BASE_DIRECTORY)

        init.init()

        if os.path.exists('TEMP'):
            os.remove('TEMP')

        with open('TEMP', 'w') as f:
            f.write('TEMPORARY FILE')
        update_index.update_index(os.path.relpath('TEMP'), 0)
        output = list_index.list_index()

        tokens = output.split(' ')

        assert(tokens[-1] == 'TEMP')
        assert(bool(re.match(r'[a-z0-9]{40}', tokens[-3])))

        with open('TEMP', 'w') as f:
            f.write('TEMPORARY FILE CHANGED')

        modified = check_modified.list_modified()
        assert(len(modified) == 1)
        assert(modified[0] == 'TEMP')
        os.remove('TEMP')

        shutil.rmtree(CONSTANTS.PATH.BASE_DIRECTORY)

if __name__ == '__main__':
    unittest.main()

