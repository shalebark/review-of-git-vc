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

    def test_branch(self):

        with open('__second', 'r') as f:
            c1 = f.read()

        assert bvc.current_branch()[0] == 'master'
        bvc.make_branch('test')

        old_id = bvc.id()
        bvc.checkout_branch('test')
        new_id = bvc.id()
        assert new_id != old_id
        assert bvc.current_branch()[0] == 'test'

        with open('__second', 'w') as f:
            f.write('switched to branch test')

        changes = bvc.status()
        assert not changes[0] and not changes[1] and not changes[2]
        assert '__second' in changes[3]

        bvc.stage('__second')
        bvc.commit('change __second in branch test')

        bvc.checkout_branch('master')

        changes = bvc.status()
        assert not changes[0] and not changes[1] and not changes[2] and not changes[3]

        with open('__second', 'r') as f:
            c = f.read()
        assert c == 'Diff for second file.'

        bvc.checkout_branch('test')
        changes = bvc.status()
        assert not changes[0] and not changes[1] and not changes[2] and not changes[3]
        with open('__second', 'r') as f:
            c = f.read()
        assert c == 'switched to branch test'

    def test_common_ancestor(self):
        bvc.checkout_branch('master')
        cma = bvc.id()

        bvc.make_branch('sidea')
        bvc.make_branch('sideb')

        bvc.checkout_branch('sidea')

        with open('__second', 'w') as f:
            f.write('sidea1')

        bvc.stage('__second')
        bvc.commit('sidea1')
        sidea_id = bvc.id()

        bvc.checkout_branch('sideb')

        with open('__second', 'w') as f:
            f.write('sideab')

        bvc.stage('__second')
        bvc.commit('sideb1')
        sideb_id = bvc.id()

        assert cma == bvc.common_ancestor(sideb_id, sidea_id)

        bvc.checkout_branch('master')
        bvc.make_branch('sidec')
        bvc.checkout_branch('sidec')
        cma = bvc.id()
        sidec_id = cma
        bvc.make_branch('sided')
        bvc.checkout_branch('sided')

        with open('__second', 'w') as f:
            f.write('sidec should be cma')

        bvc.stage('__second')
        bvc.commit('sidec __second update')
        sided_id = bvc.id()
        assert cma == bvc.common_ancestor(sidec_id, sided_id)

    def test_merge(self):
        bvc.checkout_branch('master')
        with open('__mdiff', 'w') as f:
            f.write('1\n2\n3\n4\n5\n6\n\n7\n8\n9\n10')
        bvc.stage('__mdiff')
        bvc.commit('1 to 10 mdiff')

        bvc.make_branch('mdiffa')
        bvc.make_branch('mdiffb')

        bvc.checkout_branch('mdiffa')
        # adds 11
        with open('__mdiff', 'w') as f:
            f.write('1\n2\n3\n4\n5\n6\n\n7\n8\n9\n10\n11')
        bvc.stage('__mdiff')
        bvc.commit('added 11')
        mda_id = bvc.id()

        bvc.checkout_branch('mdiffb')
        mdb_id = bvc.id()

        print('first set')
        bvc.merge(mda_id, mdb_id, '__mdiff')

        bvc.checkout_branch('mdiffa')
        """
            mdiffa changed lines 3 to 6 to:
            3 three
            4 four
            5 five
            6 six
        """
        with open('__mdiff', 'w') as f:
            f.write('1\n2\n3 three\n4 four\n5 five\n6 six\n7\n8\n9\n10')

        bvc.stage('__mdiff')
        bvc.commit('mdiff change for a')

        mdiffa_id = bvc.id()

        bvc.checkout_branch('mdiffb')
        """
            mdiffb changed lines 3 to 6 to:
            3 three // - gets deleted
            4 for
            5 fev
            6 // - no change
        """
        with open('__mdiff', 'w') as f:
            f.write('1\n2\n4 for\n5 fev\n6\n7\n8\n9\n10')

        bvc.stage('__mdiff')
        bvc.commit('mdiff change for b')

        mdiffb_id = bvc.id()

        print('second set')
        bvc.merge(mdiffb_id, mdiffa_id, '__mdiff')



    @classmethod
    def setup_class(cls):
        clean_bvc()

    @classmethod
    def teardown_class(cls):
        if os.path.exists('__first'):
            os.remove('__first')
        if os.path.exists('__second'):
            os.remove('__second')
        if os.path.exists('__mdiff'):
            os.remove('__mdiff')
        clean_bvc()
