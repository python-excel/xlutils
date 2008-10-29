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

class DummyBook:

    biff_version = 80
    logfile = sys.stdout
    pickleable = False
    verbosity = 0
    formatting_info = 0
    _xf_index_to_xl_type_map = {}
    _sheet_visibility = [0] # one sheet, visible

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
    book.add(sheet)
    return book

def make_sheet(rows,cell_type=XL_CELL_TEXT,book=None):
    if book is None:
        book = DummyBook()
    sheet = Sheet(book,0,'test sheet',0)
    for rowx in range(len(rows)):
        row = rows[rowx]
        for colx in range(len(row)):
            sheet.put_cell(rowx,colx,cell_type,row[colx],None)
    return sheet

