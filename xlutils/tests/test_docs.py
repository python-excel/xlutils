# Copyright (c) 2008-2009 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os,unittest
from fixtures import test_files
from testfixtures import LogCapture,TempDirectory
from zope.testing.doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS

options = REPORT_NDIFF|ELLIPSIS

def setUp(test):
    test.globs['test_files']=test_files
    test.globs['temp_dir']=TempDirectory().path
    test.globs['TempDirectory']=TempDirectory

def tearDown(test):
    TempDirectory.cleanup_all()
    LogCapture.uninstall_all()

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('../readme.txt', optionflags=options),
        DocFileSuite('../docs/copy.txt',optionflags=options,setUp=setUp,tearDown=tearDown),
        DocFileSuite('../docs/margins.txt',optionflags=options),
        DocFileSuite('../docs/filter.txt',optionflags=options,setUp=setUp,tearDown=tearDown),
        DocFileSuite('../docs/display.txt',optionflags=options),
        DocFileSuite('../docs/styles.txt',optionflags=options,setUp=setUp,tearDown=tearDown),
        DocFileSuite('../docs/save.txt',optionflags=options,setUp=setUp,tearDown=tearDown),
        ))
