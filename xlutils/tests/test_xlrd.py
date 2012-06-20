# Copyright (c) 2012 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from os import path
from unittest import TestCase
from xlrd import open_workbook

from fixtures import test_files

class XLRDTests(TestCase):

    # shoestring xlrd tests until we can get some real ones set up

    def test_BYTES_X00(self):
        open_workbook(path.join(test_files, 'picture_in_cell.xls'),
                      formatting_info=True)
