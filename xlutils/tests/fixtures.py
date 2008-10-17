# Copyright (c) 2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import sys

from xlrd import XL_CELL_TEXT,Book
from xlrd.sheet import Sheet

class DummyBook:

    biff_version = 80
    logfile = sys.stdout
    pickleable = False
    verbosity = 0
    formatting_info = 0
    _xf_index_to_xl_type_map = {}
    _sheet_visibility = [0] # one sheet, visible

def make_sheet(rows,cell_type=XL_CELL_TEXT):
    sheet = Sheet(DummyBook(),0,'test sheet',0)
    for rowx in range(len(rows)):
        row = rows[rowx]
        for colx in range(len(row)):
            sheet.put_cell(rowx,colx,cell_type,row[colx],None)
    return sheet

