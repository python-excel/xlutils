# Copyright (c) 2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import sys
import os.path

from xlrd import XL_CELL_TEXT,Book
from xlrd.sheet import Sheet

test_files = os.path.dirname(__file__)

test_xls_path = os.path.join(test_files,'test.xls')

class DummyBook:

    biff_version = 80
    logfile = sys.stdout
    pickleable = False
    verbosity = 0
    _xf_index_to_xl_type_map = {}
    _sheet_visibility = []
    xf_list = []
    datemode = 0
    on_demand = False

    def __init__(self,formatting_info=0):
        self.formatting_info=formatting_info
        self.__sheets = []
        self.__name2sheet = {}
        
    def add(self,sheet):
        self.__sheets.append(sheet)
        self.__name2sheet[sheet.name]=sheet

    @property
    def nsheets(self):
        return len(self.__sheets)

    def sheet_by_index(self,i):
        return self.__sheets[i]

    def sheet_by_name(self,name):
        return self.__name2sheet[name]

    def unload_sheet(self,i):
        pass
        
def make_book(rows=[]):
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
            sheet.put_cell(rowx,colx,cell_type,value,0)
    return sheet
