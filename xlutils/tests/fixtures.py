# Copyright (c) 2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import sys
import os.path

from xlrd import XL_CELL_TEXT,Book
from xlrd.sheet import Sheet

test_files = os.path.join(os.path.dirname(__file__))

test_xls_path = os.path.join(test_files,'test.xls')

class DummyBook:

    biff_version = 80
    logfile = sys.stdout
    pickleable = False
    verbosity = 0
    formatting_info = 0
    _xf_index_to_xl_type_map = {}
    _sheet_visibility = []
    xf_list = []
    datemode = 0

    def __init__(self):
        self.__sheets = []
        
    def add(self,sheet):
        self.__sheets.append(sheet)

    @property
    def nsheets(self):
        return len(self.__sheets)

    def sheet_by_index(self,i):
        return self.__sheets[i]
        
def make_book(rows):
    book = DummyBook()
    sheet = make_sheet(rows,book=book)
    return book

def make_sheet(rows,book=None,name='test sheet',number=0):
    if book is None:
        book = DummyBook()
    book._sheet_visibility.append(0)
    sheet = Sheet(book,0,name,number)
    book.add(sheet)
    for rowx in range(len(rows)):
        row = rows[rowx]
        for colx in range(len(row)):
            value = row[colx]
            if isinstance(value,tuple):
                cell_type,value = value
            else:
                cell_type=XL_CELL_TEXT
            sheet.put_cell(rowx,colx,cell_type,value,None)
    return sheet

def compare(tc,actual,expected,cmp=cmp,repr=repr):
    l_expected = len(expected)
    l_actual = len(actual)
    i = 0
    while i<l_expected and i<l_actual:
        if cmp(actual[i],expected[i]):
            break
        i+=1
    if l_expected==l_actual==i:
        return
    tc.fail(('Calls not as expected:\n'
             '    same:%r\n'
             '  actual:%r\n'
             'expected:%r')%(
        [repr(o) for o in actual[:i]],
        [repr(o) for o in actual[i:]],
        [repr(o) for o in expected[i:]]
        ))

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

class TestCallableMethod:
    def __init__(self,tf,name):
        self.tf,self.name = tf,name
    def __call__(self,*args):
        self.tf.called.append((self.name,tuple(args)))

class TestCallable:
    def __init__(self):
        self.called = []
    def __getattr__(self,name):
        return TestCallableMethod(self,name)
    def compare(self,tc,expected):
        compare(tc,self.called,expected)
    def print_called(self):
        for e in self.called:
            print e
    def __repr__(self):
        return '<TestCallable>'
    
class TTBase:

    def __getattr__(self,name):
        if name in ('__hash__','__eq__','__cmp__'):
            raise AttributeError(name)
        return self._t(self.path+'.'+name)

    def __call__(self,*args):
        return self._t(self.path+'('+(', '.join([repr(a) for a in args]))+')')
        

class TTNode(TTBase):

    def __init__(self,path,parent):
        self.path = path
        self.parent = parent
        
    def _t(self,path):
        self.parent.children.remove(self)
        n = TTNode(path,self.parent)
        self.parent.children.add(n)
        return n
        
    def __repr__(self):
        return '<TT:%s>' % self.path

    __str__ = __repr__

class TestTraversable(TTBase):

    path = ''
    
    def __init__(self):
        self.children = set()
        
    def _t(self,path):
        n = TTNode(path,self)
        self.children.add(n)
        return n
        
    def __repr__(self):
        return '<TT:%r>' % self.children

    __str__ = __repr__
    
