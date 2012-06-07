# Copyright (c) 2008-2012 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from doctest import REPORT_NDIFF, ELLIPSIS
from fixtures import test_files
from glob import glob
from manuel import doctest
from manuel.testing import TestSuite
from testfixtures import LogCapture,TempDirectory
from os.path import dirname, join, pardir

import os

workspace = os.environ.get('WORKSPACE', join(dirname(__file__), pardir, pardir))
tests = glob(join(workspace, 'docs', '*.txt'))

options = REPORT_NDIFF|ELLIPSIS

def setUp(test):
    test.globs['test_files']=test_files
    test.globs['temp_dir']=TempDirectory().path
    test.globs['TempDirectory']=TempDirectory

def tearDown(test):
    TempDirectory.cleanup_all()
    LogCapture.uninstall_all()

def test_suite():
    m =  doctest.Manuel(optionflags=REPORT_NDIFF|ELLIPSIS)
    return TestSuite(m, *tests,
                     setUp=setUp,
                     tearDown=tearDown)
