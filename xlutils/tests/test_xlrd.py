# Copyright (c) 2010 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from fixtures import make_sheet
from unittest import TestSuite,TestCase,makeSuite

class TestXlrd(TestCase):

    # some tests for things in xlrd, these should
    # really be *in* xlrd, but sadly it currently
    # has no testing framework
    
    def test_grow_rows_no_formatting(self):
        sheet = make_sheet()
        sheet.put_cell(0,0,0,'',0)
        sheet.put_cell(0,1,0,'',0)
        sheet.put_cell(0,2,0,'',0)
        sheet.put_cell(1,0,0,'',0)
        self.assertEqual(len(sheet._cell_types[1]),1)
        self.assertEqual(len(sheet._cell_types[1]),1)
        self.assertEqual(len(sheet._cell_xf_indexes),0)
    
    def test_grow_rows_formatting(self):
        sheet = make_sheet()
        sheet.formatting_info = True
        sheet.put_cell(0,0,0,'',0)
        sheet.put_cell(0,1,0,'',0)
        sheet.put_cell(0,2,0,'',0)
        sheet.put_cell(1,0,0,'',0)
        self.assertEqual(len(sheet._cell_types[1]),1)
        self.assertEqual(len(sheet._cell_types[1]),1)
        self.assertEqual(len(sheet._cell_xf_indexes[1]),1)
    
def test_suite():
    return TestSuite((
        makeSuite(TestXlrd),
        ))
