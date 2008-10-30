# Copyright (c) 2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os
import xlrd

from glob import glob

class BaseReader:

    def get_filepaths(self):
        """
        This is the most common method to implement. It must return an
        interable sequence of paths to excel files.
        """
        raise NotImplementedError

    def get_workbooks(self):
        """
        If the data to be processed is not stored in files or if
        special parameters need to be passed to xlrd.open_workbook
        then this method must be overriden.
        Any implementation must return an iterable sequence of tuples.
        The first element of which must be an xlrd.Book object and the
        second must be the filename of the file from which the book
        object came.
        """
        for path in self.get_filepaths():
            yield (
                xlrd.open_workbook(path, pickleable=0, formatting_info=1),
                os.path.split(path)[1]
                )

    def __call__(self,filter):
        """
        Once instantiated, a reader will be called and have the first
        filter in the chain passed. The implementation of this method
        should call the appropriate methods on the filter based on the
        cells found in the Book objects returned from the
        get_workbooks method.
        """
        for workbook,filename in self.get_workbooks():
            filter.workbook(workbook,filename)
            for sheet_x in range(workbook.nsheets):
                sheet = workbook.sheet_by_index(sheet_x)
                filter.sheet(sheet,sheet.name)
                for row_x in xrange(sheet.nrows):
                    filter.row(row_x,row_x)
                    for col_x in xrange(sheet.ncols):
                        filter.cell(row_x,col_x,row_x,col_x)
        filter.finish()
    
class BaseFilter:
    """
    This is a simple filter that just calls the next filter in the
    chain. The 'next' attribute is set up by the process method.
    It can make a good base class for a new filter.
    """

    def workbook(self,rdbook,wtbook_name):
        """
        The workbook method is called every time processing of a new
        workbook starts.

        rdbook - the xlrd.Book object from which the new workbook
                 should be created.

        wtbook_name - the name of the workbook into which content
                      should be written.
        """
        self.next.workbook(rdbook,wtbook_name)
   
    def sheet(self,rdsheet,wtsheet_name):
        """
        The sheet method is called every time processing of a new
        sheet in the current workbook starts.

        rdsheet - the xlrd.sheet.Sheet object from which the new
                  sheet should be created.

        wtsheet_name - the name of the sheet into which content
                       should be written.
        """
        self.next.sheet(rdsheet,wtsheet_name)
       
    def row(self,rdrowx,wtrowx):
        """
        The row method is called every time processing of a new
        row in the current sheet starts.
        It is primarily for copying row-based formatting from the
        source row to the target row.

        rdrowx - the index of the row in the current sheet from which
                 information for the row to be written should be
                 copied. 

        wtrowx - the index of the row in sheet to be written to which
                 information should be written for the row being read.
        """
        self.next.row(rdrowx,wtrowx)

    def cell(self,rdrowx,rdcolx,wtrowx,wtcolx):
        """
        This is called for every cell in the sheet being processed.
        This is the most common method in which filtering and queuing
        of onward calls to the next filter takes place.

        rdrowx - the index of the row to be read from in the current
                 sheet. 

        rdcolx - the index of the column to be read from in the current
                 sheet. 

        wtrowx - the index of the row to be written to in the current
                 output sheet. 

        wtcolx - the index of the column to be written to in the current
                 output sheet. 
        """
        self.next.cell(rdrowx,rdcolx,wtrowx,wtcolx)

    def finish(self):
        """
        This method is called once processing of all workbooks has
        been completed.

        A filter should call this method on the next filter in the
        chain as an indication that no further calls will be made to
        any methods.
        """
        self.next.finish()

class GlobReader(BaseReader):

    def __init__(self,spec):
        self.spec = spec
        
    def get_filepaths(self):
        return glob(self.spec)

class MethodFilter:
    """
    This is a base class that implements functionality for filters
    that want to do a common task such as logging, printing or memory
    usage recording on certain calls.
    """

    def __init__(self,call_on=(
        'workbook',
        'sheet',
        'row',
        'cell',
        'finish',
        )):
        self.call_on = call_on

    def __getattr__(self,name):
        pass
        
def process(reader,*chain):
    for i in range(len(chain)-1):
        chain[i].next = chain[i+1]
    reader(chain[0])
