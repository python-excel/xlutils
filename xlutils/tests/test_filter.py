# Copyright (c) 2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from unittest import TestSuite,TestCase,makeSuite
from xlutils.filter import BaseReader,process
from xlutils.tests.fixtures import test_files,make_book

import os

class O:
    """
    A proxy for use in expected values to indicate that
    only the class of the object is important.
    """
    def __init__(self,class_name):
        self.class_name = class_name
    def __cmp__(self,other):
        c = other.__class__
        return cmp(
            self.class_name,
            c.__module__+'.'+c.__name__
            )
    def __repr__(self):
        return '<O:%s>'%self.class_name

class TestFilterMethod:
    def __init__(self,tf,name):
        self.tf,self.name = tf,name
    def __call__(self,*args):
        self.tf.called.append((self.name,tuple(args)))

class TestFilter:
    def __init__(self):
        self.called = []
    def __getattr__(self,name):
        return TestFilterMethod(self,name)
    def compare(self,tc,expected):
        l_expected = len(expected)
        l_called = len(self.called)
        errors = []
        i = 0
        while i<l_expected and i<l_called:
            if self.called[i]!=expected[i]:
                break
            i+=1
        if l_expected==l_called==i:
            return
        tc.fail(('Calls not as expected:\n'
                 '    same:%r\n'
                 '  actual:%r\n'
                 'expected:%r')%(
            self.called[:i],
            self.called[i:],
            expected[i:]
            ))
            
    
class TestBaseReader(TestCase):

    def test_no_implementation(self):
        r = BaseReader()
        f = TestFilter()
        self.assertRaises(NotImplementedError,r,f)
        self.assertEqual(f.called,[])
        
    def test_custom_filepaths(self):
        # also tests the __call__ method
        class TestReader(BaseReader):
            def get_filepaths(self):
                return (os.path.join(test_files,'test.xls'),)
        t = TestReader()
        f = TestFilter()
        t(f)
        f.compare(self,[
            ('workbook',(O('xlrd.Book'),'test.xls')),
            ('sheet',(O('xlrd.sheet.Sheet'),u'Sheet1')),
            ('row',(0,0)),
            ('cell',(0,0,0,0)),
            ('cell',(0,1,0,1)),
            ('row',(1,1)),
            ('cell',(1,0,1,0)),
            ('cell',(1,1,1,1)),
            ('sheet',(O('xlrd.sheet.Sheet'),u'Sheet2')),
            ('row',(0,0)),
            ('cell',(0,0,0,0)),
            ('cell',(0,1,0,1)),
            ('row',(1,1)),
            ('cell',(1,0,1,0)),
            ('cell',(1,1,1,1)),
            ('finish',()),
            ])
        # check we're opening things correctly
        book = f.called[0][1][0]
        self.assertEqual(book.pickleable,0)
        self.assertEqual(book.formatting_info,1)

    def test_custom_getworkbooks(self):
        book = make_book((('1','2','3'),))
        class TestReader(BaseReader):
            def get_workbooks(self):
                yield book,'test.xls'
        t = TestReader()
        f = TestFilter()
        t(f)
        f.compare(self,[
            ('workbook',(O('xlutils.tests.fixtures.DummyBook'),'test.xls')),
            ('sheet',(O('xlrd.sheet.Sheet'),'test sheet')),
            ('row',(0,0)),
            ('cell',(0,0,0,0)),
            ('cell',(0,1,0,1)),
            ('cell',(0,2,0,2)),
            ('finish',()),
            ])
        # check we're getting the right things
        self.failUnless(f.called[0][1][0] is book)
        self.failUnless(f.called[1][1][0] is book.sheet_by_index(0))
    
class TestBaseFilter(TestCase):

    def setUp(self):
        from xlutils.filter import BaseFilter
        self.filter = BaseFilter()
        self.filter.next = self.tf = TestFilter()

    def test_workbook(self):
        self.filter.workbook('rdbook','wtbook_name')
        self.assertEqual(self.tf.called,[
            ('workbook',('rdbook','wtbook_name'))
            ])
                         
    def test_sheet(self):
        self.filter.sheet('rdsheet','wtsheet_name')
        self.assertEqual(self.tf.called,[
            ('sheet',('rdsheet','wtsheet_name'))
            ])
                         
    def test_row(self):
        self.filter.row(0,1)
        self.assertEqual(self.tf.called,[
            ('row',(0,1))
            ])
                         
    def test_cell(self):
        self.filter.cell(0,1,2,3)
        self.assertEqual(self.tf.called,[
            ('cell',(0,1,2,3))
            ])
                         
    def test_finish(self):
        self.filter.finish()
        self.assertEqual(self.tf.called,[
            ('finish',())
            ])

class TestMethodFilter(TestCase):

    def test_all(self):
        pass

    def test_none(self):
        pass

    def test_one(self):
        pass

    def test_invalid(self):
        pass
    
    def setUp(self):
        from xlutils.filter import BaseFilter
        self.filter = BaseFilter()
        self.filter.next = self.tf = TestFilter()

    def test_workbook(self):
        self.filter.workbook('rdbook','wtbook_name')
        self.assertEqual(self.tf.called,[
            ('workbook',('rdbook','wtbook_name'))
            ])
                         
    def test_sheet(self):
        self.filter.sheet('rdsheet','wtsheet_name')
        self.assertEqual(self.tf.called,[
            ('sheet',('rdsheet','wtsheet_name'))
            ])
                         
    def test_row(self):
        self.filter.row(0,1)
        self.assertEqual(self.tf.called,[
            ('row',(0,1))
            ])
                         
    def test_cell(self):
        self.filter.cell(0,1,2,3)
        self.assertEqual(self.tf.called,[
            ('cell',(0,1,2,3))
            ])
                         
    def test_finish(self):
        self.filter.finish()
        self.assertEqual(self.tf.called,[
            ('finish',())
            ])

class TestProcess(TestCase):

    def test_setup(self):
        class DummyReader:
            def __call__(self,filter):
                filter.finished()
        F1 = TestFilter()
        F2 = TestFilter()
        process(DummyReader(),F1,F2)
        self.failUnless(F1.next is F2)
        self.failUnless(isinstance(F2.next,TestFilterMethod))
        F1.compare(self,[('finished',())])
        F2.compare(self,())
    
def test_suite():
    return TestSuite((
        makeSuite(TestBaseReader),
        makeSuite(TestBaseFilter),
        # makeSuite(TestMethodFilter),
        makeSuite(TestProcess),
        ))
