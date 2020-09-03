import unittest
import shutil
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bvc

def clean_bvc():
    if os.path.exists('.bvc'):
        shutil.rmtree('.bvc')

class TestBVC:

    def test_init(self, tmpdir):
        bvc.init()

        assert os.path.exists('.bvc')
        assert os.path.exists('.bvc/HEAD')
        assert os.path.exists('.bvc/INDEX')
        assert os.path.exists('.bvc/objects')

    def test_stage_add(self):
        changes = bvc.status()

        # empty directory, no changes
        assert not changes[0] and not changes[1] and not changes[2] and not changes[3]

        with open('__first', 'w') as f:
            f.write('First File')

        bvc.stage('__first')

        # __first is now in added
        changes = bvc.status()

        assert '__first' in changes[0]

    def test_commit(self):
        bvc.commit('Added First File')
        changes = bvc.status()
        assert not changes[0] and not changes[1] and not changes[2] and not changes[3]


        # Changed the first file, second file is still untracked, should not show up.
        with open('__second', 'w') as f:
            f.write('Second File')

        with open('__first', 'w') as f:
            f.write('Change to first file.')

        changes = bvc.status()
        assert '__first' in changes[3]
        assert not changes[0] and not changes[1] and not changes[2]

        bvc.commit('Changed first file, second file still untracked')

        # Add second to stage, first is removed
        bvc.stage('__second')
        bvc.stage('__first', False)

        changes = bvc.status()
        assert '__second' in changes[0] and '__first' in changes[1]
        assert not os.path.exists('__first')

        bvc.commit('Removed first file, add second file to index')
        changes = bvc.status()
        assert not changes[0] and not changes[1] and not changes[2] and not changes[3]

    def test_log(self):
        log = bvc.log()
        ll = log.split('\n')

        assert 'Removed first file, add second file to index' in ll[0]
        assert 'Changed first file, second file still untracked' in ll[1]
        assert 'Added First File' in ll[2]

    def test_diff(self):
        with open('__second', 'w') as f:
            f.write('Diff for second file.')
        bvc.stage('__second')
        changes = bvc.status()

        bvc.commit('diff test for first file')
        logs = [ tuple(l.split('\t')) for l in bvc.log().split('\n') if l]

        ch1 = logs[0][0]
        ch2 = logs[1][0]

        diffs = bvc.diff(ch1, '__second', ch2, '__second').split('\n')
        assert diffs[6] == '-Second File'
        assert diffs[7] == '+Diff for second file.'

    @classmethod
    def setup_class(cls):
        clean_bvc()

    @classmethod
    def teardown_class(cls):
        if os.path.exists('__first'):
            os.remove('__first')
        if os.path.exists('__second'):
            os.remove('__second')
        clean_bvc()
