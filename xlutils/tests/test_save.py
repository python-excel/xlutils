# Copyright (c) 2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os
from fixtures import TestCallable
from shutil import rmtree
from StringIO import StringIO
from tempfile import mkdtemp,TemporaryFile
from unittest import TestSuite,TestCase,makeSuite
from xlutils import save
from xlutils.filter import process,XLRDReader,StreamWriter

class TestSave(TestCase):

    def test_save_path(self):
        wb = object()
        c = TestCallable()
        temp_dir=mkdtemp()
        path = os.path.join(temp_dir,'path.xls')
        try:
            save.process = c
            save.save(wb,path)
        finally:
            rmtree(temp_dir)
            save.process = process
        self.assertEqual(len(c.called),1)
        args = c.called[0][1]
        self.assertEqual(len(args),2)
        r = args[0]
        self.failUnless(isinstance(r,XLRDReader))
        self.failUnless(r.wb is wb)
        self.assertEqual(r.filename,'path.xls')
        w = args[1]
        self.failUnless(isinstance(w,StreamWriter))
        f = w.stream
        self.failUnless(isinstance(f,file))
        self.assertEqual(f.name,path)
        self.assertEqual(f.mode,'wb')
        self.assertEqual(f.closed,True)
        
    def test_save_stringio(self):
        wb = object()
        c = TestCallable()
        s = StringIO()
        try:
            save.process = c
            save.save(wb,s)
        finally:
            save.process = process
        self.assertEqual(len(c.called),1)
        args = c.called[0][1]
        self.assertEqual(len(args),2)
        r = args[0]
        self.failUnless(isinstance(r,XLRDReader))
        self.failUnless(r.wb is wb)
        self.assertEqual(r.filename,'unknown.xls')
        w = args[1]
        self.failUnless(isinstance(w,StreamWriter))
        self.failUnless(w.stream is s)

    def test_save_tempfile(self):
        wb = object()
        c = TestCallable()
        ef = TemporaryFile()
        try:
            save.process = c
            save.save(wb,ef)
        finally:
            save.process = process
        self.assertEqual(len(c.called),1)
        args = c.called[0][1]
        self.assertEqual(len(args),2)
        r = args[0]
        self.failUnless(isinstance(r,XLRDReader))
        self.failUnless(r.wb is wb)
        self.assertEqual(r.filename,'unknown.xls')
        w = args[1]
        self.failUnless(isinstance(w,StreamWriter))
        af = w.stream
        self.failUnless(af is ef)
        self.assertEqual(ef.closed,False)
    
def test_suite():
    return TestSuite((
        makeSuite(TestSave),
        ))
