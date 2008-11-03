# Copyright (c) 2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import unittest
from fixtures import test_files
from shutil import rmtree
from tempfile import mkdtemp
from zope.testing.doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS

options = REPORT_NDIFF|ELLIPSIS

def setUp(test):
    test.globs['test_files']=test_files
    test.globs['temp_dir']=mkdtemp()

def tearDown(test):
    rmtree(test.globs['temp_dir'])

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('../readme.txt', optionflags=options),
        DocFileSuite('../docs/margins.txt',optionflags=options),
        DocFileSuite('../docs/filter.txt',optionflags=options,setUp=setUp,tearDown=tearDown),
        DocFileSuite('../docs/display.txt',optionflags=options),
        ))
