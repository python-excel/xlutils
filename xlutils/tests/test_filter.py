# Copyright (c) 2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from tempfile import TemporaryFile
from unittest import TestSuite,TestCase,makeSuite
from xlrd import open_workbook,XL_CELL_NUMBER,XL_CELL_ERROR,XL_CELL_TEXT
from xlutils.filter import BaseReader,GlobReader,MethodFilter,BaseWriter,process
from xlutils.tests.fixtures import test_files,test_xls_path,make_book,make_sheet,DummyBook
from xlutils.tests.fixtures import compare,O,TestCallable,TestCallableMethod,TestTraversable
from zope.testing.loggingsupport import InstalledHandler

import os

class TestReader(BaseReader):

    def __init__(self,*sheets):
        self.book = DummyBook()
        index = 0
        for name,rows in sheets:
            make_sheet(rows,self.book,name,index)
            index+=1
            
    def get_workbooks(self):
        yield self.book,'test.xls'

class TestTestReader(TestCase):

    def test_cell_type(self):
        r = TestReader(('Sheet1',(((XL_CELL_NUMBER,0.0),),)))
        book = tuple(r.get_workbooks())[0][0]
        cell = book.sheet_by_index(0).cell(0,0)
        self.assertEqual(cell.value,0.0)
        self.assertEqual(cell.ctype,XL_CELL_NUMBER)
        
class TestBaseReader(TestCase):

    def test_no_implementation(self):
        r = BaseReader()
        f = TestCallable()
        self.assertRaises(NotImplementedError,r,f)
        self.assertEqual(f.called,[])
        
    def test_custom_filepaths(self):
        # also tests the __call__ method
        class TestReader(BaseReader):
            def get_filepaths(self):
                return (test_xls_path,)
        t = TestReader()
        f = TestCallable()
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
        f = TestCallable()
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
        self.filter.next = self.tf = TestCallable()

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
                         
    def test_set_rdsheet(self):
        self.filter.set_rdsheet('rdsheet2')
        self.assertEqual(self.tf.called,[
            ('set_rdsheet',('rdsheet2',))
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

class OurMethodFilter(MethodFilter):
    def __init__(self,collector,call_on=True):
        MethodFilter.__init__(self,call_on)
        self.collector = collector        
    def method(self,name,*args):
        self.collector.append((name,args))
        
class TestMethodFilter(TestCase):

    def setUp(self):
        self.called = []

    def do_calls_and_test(self,filter):
        filter.next = tf = TestCallable()
        filter.workbook('rdbook','wtbook_name')
        filter.sheet('rdsheet','wtsheet_name')
        filter.row(0,1)
        filter.cell(0,1,2,3)
        filter.set_rdsheet('rdsheet2')
        filter.finish()
        self.assertEqual(tf.called,[
            ('workbook',('rdbook','wtbook_name')),
            ('sheet',('rdsheet','wtsheet_name')),
            ('row',(0,1)),
            ('cell',(0,1,2,3)),
            ('set_rdsheet',('rdsheet2',)),
            ('finish',()),
            ])
        
    def test_all(self):
        self.do_calls_and_test(OurMethodFilter(self.called))
        self.assertEqual(self.called,[
            ('workbook',('rdbook','wtbook_name')),
            ('sheet',('rdsheet','wtsheet_name')),
            ('row',(0,1)),
            ('cell',(0,1,2,3)),
            ('set_rdsheet',('rdsheet2',)),
            ('finish',()),
            ])

    def test_somecalls_and_test(self):
        self.do_calls_and_test(OurMethodFilter(self.called,['row','cell']))
        self.assertEqual(self.called,[
            ('row',(0,1)),
            ('cell',(0,1,2,3)),
            ])

    def test_none(self):
        self.do_calls_and_test(OurMethodFilter(self.called,()))
        self.assertEqual(self.called,[])

    def test_workbook(self):
        self.do_calls_and_test(OurMethodFilter(self.called,['workbook']))
        self.assertEqual(self.called,[
            ('workbook',('rdbook','wtbook_name')),
            ])

    def test_sheet(self):
        self.do_calls_and_test(OurMethodFilter(self.called,['sheet']))
        self.assertEqual(self.called,[
            ('sheet',('rdsheet','wtsheet_name')),
            ])

    def test_set_rdsheet(self):
        self.do_calls_and_test(OurMethodFilter(self.called,['set_rdsheet']))
        self.assertEqual(self.called,[
            ('set_rdsheet',('rdsheet2',)),
            ])

    def test_row(self):
        self.do_calls_and_test(OurMethodFilter(self.called,['row']))
        self.assertEqual(self.called,[
            ('row',(0,1)),
            ])

    def test_cell(self):
        self.do_calls_and_test(OurMethodFilter(self.called,['cell']))
        self.assertEqual(self.called,[
            ('cell',(0,1,2,3)),
            ])

    def test_finish(self):
        self.do_calls_and_test(OurMethodFilter(self.called,['finish']))
        self.assertEqual(self.called,[
            ('finish',()),
            ])

    def test_invalid(self):
        self.assertRaises(Exception,OurMethodFilter,self.called,['foo'])
    
from xlutils.filter import Echo

class TestEcho(TestCase):

    def test_method(self):
        filter = Echo(methods=['workbook'])
        from StringIO import StringIO
        import sys
        try:
            sys.stdout = out = StringIO()
            filter.method('name','foo',1)
        finally:
            sys.stdout = sys.__stdout__
        self.assertEqual(out.getvalue(),"name:('foo', 1)\n")
        
    def test_method_with_name(self):
        filter = Echo('echo',['workbook'])
        from StringIO import StringIO
        import sys
        try:
            sys.stdout = out = StringIO()
            filter.method('name','foo',1)
        finally:
            sys.stdout = sys.__stdout__
        self.assertEqual(out.getvalue(),"'echo' name:('foo', 1)\n")
        
    def test_inheritance(self):
        self.failUnless(isinstance(Echo(),MethodFilter))

class TestMemoryLogger(TestCase):
    
    def setUp(self):
        from xlutils.filter import MemoryLogger
        self.filter = MemoryLogger('somepath',['workbook'])

    def test_method(self):
        import xlutils.filter
        try:
            o = xlutils.filter.h
            xlutils.filter.h = h = TestTraversable()
            self.filter.method('name','foo',1)
        finally:
            xlutils.filter.h = o
        self.assertEqual(len(h.children),1)
        self.assertEqual(tuple(h.children)[0].path,
                         ".heap().stat.dump('somepath')")
    
    def test_method_no_heapy(self):
        import xlutils.filter
        try:
            o = xlutils.filter.h
            xlutils.filter.h = None
            self.filter.method('name','foo',1)
        finally:
            xlutils.filter.h = o
    
    def test_inheritance(self):
        self.failUnless(isinstance(self.filter,MethodFilter))

from xlutils.filter import ErrorFilter

class TestErrorFilter(TestCase):

    def test_set_rdsheet_1(self):
        h = InstalledHandler('')
        r = TestReader(
            ('Sheet1',[['S1R0C0']]),
            ('Sheet2',[[(XL_CELL_ERROR,0)]]),
            )
        book = tuple(r.get_workbooks())[0][0]
        # fire methods on filter
        f = ErrorFilter()
        f.next = c = TestCallable()
        f.workbook(book,'new.xls')
        f.sheet(book.sheet_by_index(0),'new')
        f.cell(0,0,0,0)
        f.set_rdsheet(book.sheet_by_index(1))
        f.cell(0,0,1,0)
        f.finish()
        compare(self,c.called,[])
        self.assertEqual(len(h.records),2)
        self.assertEqual(
            h.records[0].getMessage(),
            "Cell A1 of sheet 'Sheet2' contains a bad value: error (#NULL!)"
            )
        self.assertEqual(
            h.records[1].getMessage(),
            'No output as errors have occurred.'
            )

    def test_set_rdsheet_2(self):
        h = InstalledHandler('')
        r = TestReader(
            ('Sheet1',[['S1R0C0']]),
            ('Sheet2',[[(XL_CELL_ERROR,0)]]),
            )
        book = tuple(r.get_workbooks())[0][0]
        # fire methods on filter
        f = ErrorFilter()
        f.next = c = TestCallable()
        f.workbook(book,'new.xls')
        f.sheet(book.sheet_by_index(0),'new')
        f.cell(0,0,0,0)
        f.cell(0,0,1,0)
        f.finish()
        compare(self,c.called,[
            ('workbook', (O('xlrd.Book'), 'new.xls')),
            ('sheet', (O('xlrd.sheet.Sheet'), u'new')),
            ('row', (0, 0)),
            ('cell', (0, 0, 0, 0)),
            ('row', (1, 1)),
            ('cell', (1, 0, 1, 0)),
            ('finish', ())
            ])
        self.assertEqual(c.called[1][1][0].name,'new')
        self.assertEqual(len(h.records),0)
    
    def test_multiple_workbooks_with_same_name(self):
        h = InstalledHandler('')
        r = TestReader(
            ('Sheet1',[['S1R0C0']]),
            )
        book = tuple(r.get_workbooks())[0][0]
        # fire methods on filter
        f = ErrorFilter()
        f.next = c = TestCallable()
        f.workbook(book,'new.xls')
        f.sheet(book.sheet_by_index(0),'new1')
        f.cell(0,0,0,0)
        f.workbook(book,'new.xls')
        f.sheet(book.sheet_by_index(0),'new2')
        f.cell(0,0,0,0)
        f.finish()
        compare(self,c.called,[
            ('workbook', (O('xlrd.Book'), 'new.xls')),
            ('sheet', (O('xlrd.sheet.Sheet'), u'new1')),
            ('row', (0, 0)),
            ('cell', (0, 0, 0, 0)),
            ('workbook', (O('xlrd.Book'), 'new.xls')),
            ('sheet', (O('xlrd.sheet.Sheet'), u'new2')),
            ('row', (0, 0)),
            ('cell', (0, 0, 0, 0)),
            ('finish', ())
            ])
        self.assertEqual(c.called[1][1][0].name,'new1')
        self.assertEqual(c.called[5][1][0].name,'new2')
        self.assertEqual(len(h.records),0)
    
from xlutils.filter import ColumnTrimmer

class TestColumnTrimmer(TestCase):

    def test_set_rdsheet(self):
        h = InstalledHandler('')
        r = TestReader(
            ('Sheet1',[['X',' ']]),
            ('Sheet2',[['X','X']]),
            )
        book = tuple(r.get_workbooks())[0][0]
        # fire methods on filter
        f = ColumnTrimmer()
        f.next = c = TestCallable()
        f.workbook(book,'new.xls')
        f.sheet(book.sheet_by_index(0),'new')
        f.row(0,0)
        f.cell(0,0,0,0)
        f.set_rdsheet(book.sheet_by_index(1))
        f.cell(0,0,0,1)
        f.finish()
        compare(self,c.called,[
            ('workbook', (O('xlutils.tests.fixtures.DummyBook'), 'new.xls')),
            ('sheet', (O('xlrd.sheet.Sheet'), u'new')),
            ('row', (0, 0)),
            ('cell', (0, 0, 0, 0)),
            ('set_rdsheet', (O('xlrd.sheet.Sheet'),)),
            ('cell', (0, 0, 0, 1)),
            ('finish', ())
            ])
        self.assertEqual(c.called[1][1][0].name,'Sheet1')
        self.assertEqual(c.called[4][1][0].name,'Sheet2')
        self.assertEqual(len(h.records),0)

    def test_use_write_sheet_name_in_logging(self):
        h = InstalledHandler('')
        r = TestReader(
            ('Sheet1',[['X',' ']]),
            )
        book = tuple(r.get_workbooks())[0][0]
        # fire methods on filter
        f = ColumnTrimmer()
        f.next = c = TestCallable()
        f.workbook(book,'new.xls')
        f.sheet(book.sheet_by_index(0),'new')
        f.row(0,0)
        f.cell(0,0,0,0)
        f.cell(0,1,0,1)
        f.finish()
        compare(self,c.called,[
            ('workbook', (O('xlutils.tests.fixtures.DummyBook'), 'new.xls')),
            ('sheet', (O('xlrd.sheet.Sheet'), u'new')),
            ('row', (0, 0)),
            ('cell', (0, 0, 0, 0)),
            ('finish', ())
            ])
        self.assertEqual(c.called[1][1][0].name,'Sheet1')
        self.assertEqual(len(h.records),1)
        self.assertEqual(h.records[0].getMessage(),
                         "Number of columns trimmed from 2 to 1 for sheet 'new'")
        

    def test_multiple_books(self):
        h = InstalledHandler('')
        r = GlobReader(os.path.join(test_files,'*.xls'))
        book = tuple(r.get_workbooks())[0][0]
        # fire methods on filter
        f = ColumnTrimmer()
        f.next = c = TestCallable()
        r(f)
        compare(self,c.called,[
            ('workbook', (O('xlrd.Book'), 'test.xls')),
            ('sheet', (O('xlrd.sheet.Sheet'), u'Sheet1')),
            ('row', (0, 0)),
            ('row', (1, 1)),
            ('cell', (0, 0, 0, 0)),('cell', (0, 1, 0, 1)),
            ('cell', (1, 0, 1, 0)),('cell', (1, 1, 1, 1)),
            ('sheet', (O('xlrd.sheet.Sheet'), u'Sheet2')),
            ('row', (0, 0)),
            ('row', (1, 1)),
            ('cell', (0, 0, 0, 0)),('cell', (0, 1, 0, 1)),
            ('cell', (1, 0, 1, 0)),('cell', (1, 1, 1, 1)),
            ('workbook', (O('xlrd.Book'), 'testall.xls')),
            ('sheet', (O('xlrd.sheet.Sheet'), u'Sheet1')),
            ('row', (0, 0)),
            ('row', (1, 1)),
            ('row', (2, 2)),
            ('row', (3, 3)),
            ('row', (4, 4)),
            ('row', (5, 5)),
            ('cell', (0, 0, 0, 0)),('cell', (0, 1, 0, 1)),
            ('cell', (1, 0, 1, 0)),('cell', (1, 1, 1, 1)),
            ('cell', (2, 0, 2, 0)),('cell', (2, 1, 2, 1)),
            ('cell', (3, 0, 3, 0)),('cell', (3, 1, 3, 1)),
            ('cell', (4, 0, 4, 0)),('cell', (4, 1, 4, 1)),
            ('cell', (5, 0, 5, 0)),('cell', (5, 1, 5, 1)),
            ('sheet', (O('xlrd.sheet.Sheet'), u'Sheet2')),
            ('row', (0, 0)),
            ('row', (1, 1)),
            ('cell', (0, 0, 0, 0)),('cell', (0, 1, 0, 1)),
            ('cell', (1, 0, 1, 0)),('cell', (1, 1, 1, 1)),
            ('finish', ())
            ])
        self.assertEqual(len(h.records),0)
    
class CloseableTemporaryFile:
    def __init__(self,parent,filename):
        self.file = TemporaryFile()
        self.parent=parent
        self.filename=filename
    def close(self):
        self.parent.closed.add(self.filename)
        self.file.seek(0)
    def write(self,*args,**kw):
        self.file.write(*args,**kw)
    def real_close(self):
        self.file.close()
        
class TestWriter(BaseWriter):

    def __init__(self):
        self.files = {}
        self.closed = set()
        
    def get_stream(self,filename):
        f = CloseableTemporaryFile(self,filename)
        self.files[filename]=f
        return f
        
class TestBaseWriter(TestCase):

    def note_index(self,ao,eo,name):
        if name not in self.noted_indexes:
            self.noted_indexes[name]={}
        mapping = self.noted_indexes[name]
        a,e = getattr(ao,name),getattr(eo,name)
        if a not in mapping:
            mapping[a]=set()
        # for style compression, we may get multiple expected indexes
        # for each actual index in the output file. We just need to make
        # sure all the data is the same.
        mapping.get(a).add(e)
        
    def check_file(self,writer,path,
                   l_a_xf_list=20,
                   l_e_xf_list=26,
                   l_a_format_map=38,
                   l_e_format_map=37,
                   l_a_font_list=9,
                   l_e_font_list=7):
        self.noted_indexes = {}
        # now open the source file
        e = open_workbook(path,pickleable=0,formatting_info=1)
        # and the target file
        f = writer.files[os.path.split(path)[1]].file
        a = open_workbook(file_contents=f.read(),pickleable=0,formatting_info=1)
        f.close()
        # and then compare
        def assertEqual(e,a,*names):
            for name in names:
                aa = getattr(e,name)
                ea = getattr(a,name)
                self.assertEqual(aa,ea,'%s:%r!=%r'%(name,aa,ea))

        assertEqual(e,a,'nsheets')
        for sheet_x in range(a.nsheets):
            ash = a.sheet_by_index(sheet_x)
            es = e.sheet_by_index(sheet_x)
            # BUG: xlwt does nothing with col_default_width, it should :-(
            self.assertEqual(es.standardwidth,None)
            self.assertEqual(es.defcolwidth,11)
            self.assertEqual(ash.standardwidth,None)
            self.assertEqual(ash.defcolwidth,None)
            # /BUG
            
            # order doesn't matter in this list
            compare(self,sorted(ash.merged_cells),sorted(es.merged_cells))

            assertEqual(
                ash,es,
                'show_formulas',
                'show_grid_lines',
                'show_sheet_headers',
                'panes_are_frozen',
                'show_zero_values',
                'automatic_grid_line_colour',
                'columns_from_right_to_left',
                'show_outline_symbols',
                'remove_splits_if_pane_freeze_is_removed',
                'sheet_selected',
                'sheet_visible',
                'show_in_page_break_preview',
                'first_visible_rowx',
                'first_visible_colx',
                'gridline_colour_index',
                'cached_page_break_preview_mag_factor',
                'cached_normal_view_mag_factor',
                'default_row_height',
                'default_row_height_mismatch',
                'default_row_hidden',
                'default_additional_space_above',
                'default_additional_space_below',
                'nrows',
                'ncols',
                )
            for col_x in range(ash.ncols):
                ac = ash.colinfo_map[col_x]
                ec = es.colinfo_map[col_x]
                assertEqual(ac,ec,
                            'width',
                            'hidden',
                            'outline_level',
                            'collapsed',
                            )
                self.note_index(ac,ec,'xf_index')
            for row_x in range(ash.nrows):
                ar = ash.rowinfo_map.get(row_x)
                er = es.rowinfo_map.get(row_x)
                if er is None:
                    # NB: wlxt always writes Rowinfos, even
                    #     if none is supplied.
                    #     So, they end up with default values
                    #     which is what this tests
                    er = ar.__class__
                else:
                    assertEqual(ar,er,
                                'height',
                                'has_default_height',
                                'height_mismatch',
                                'outline_level',
                                'outline_group_starts_ends',
                                'hidden',
                                'additional_space_above',
                                'additional_space_below',
                                'has_default_xf_index',
                                )
                    if ar.has_default_xf_index:
                        self.note_index(ar,er,'xf_index')
                for col_x in range(ash.ncols):
                    ac = ash.cell(row_x,col_x)
                    ec = es.cell(row_x,col_x)
                    assertEqual(ac,ec,
                                'ctype',
                                'value')
                    self.note_index(ac,ec,'xf_index')

        # only XFs that are in use are copied,
        # but we check those copied are identical
        self.assertEqual(len(a.xf_list),l_a_xf_list)
        self.assertEqual(len(e.xf_list),l_e_xf_list)
        for ai,eis in self.noted_indexes['xf_index'].items():
            axf = a.xf_list[ai]
            for ei in eis:
                exf = e.xf_list[ei]
                self.note_index(axf,exf,'format_key')
                self.note_index(axf,exf,'font_index')
                ap = axf.protection
                ep = exf.protection
                assertEqual(ap,ep,
                            'cell_locked',
                            'formula_hidden',
                            )
                ab = axf.border
                eb = exf.border
                assertEqual(ab,eb,
                            'left_line_style',
                            'right_line_style',
                            'top_line_style',
                            'bottom_line_style',
                            'diag_line_style',
                            'left_colour_index',
                            'right_colour_index',
                            'top_colour_index',
                            'bottom_colour_index',
                            'diag_colour_index',
                            'diag_down',
                            'diag_up',
                            )
                ab = axf.background
                eb = exf.background
                assertEqual(ab,eb,
                            'fill_pattern',
                            'pattern_colour_index',
                            'background_colour_index',
                            )
                aa = axf.alignment
                ea = exf.alignment
                assertEqual(aa,ea,
                            'hor_align',
                            'vert_align',
                            'text_direction',
                            'rotation',
                            'text_wrapped',
                            'shrink_to_fit',
                            'indent_level',
                            )
            
        # xlwt writes more formats than exist in an original,
        # but we check those copied are identical
        self.assertEqual(len(a.format_map),l_a_format_map)
        self.assertEqual(len(e.format_map),l_e_format_map)
        for ai,eis in self.noted_indexes['format_key'].items():
            af = a.format_map[ai]
            for ei in eis:
                ef = e.format_map[ei]
                assertEqual(af,ef,
                            'format_str',
                            'type')
        # xlwt writes more fonts than exist in an original,
        # but we check those that exist in both...
        self.assertEqual(len(a.font_list),l_a_font_list)
        self.assertEqual(len(e.font_list),l_e_font_list)
        for ai,eis in self.noted_indexes['font_index'].items():
            af = a.font_list[ai]
            for ei in eis:
                ef = e.font_list[ei]
                assertEqual(af,ef,
                            'height',
                            'italic',
                            'struck_out',
                            'outline',
                            'colour_index',
                            'bold',
                            'weight',
                            'escapement',
                            'underline_type',
                            'family',
                            'character_set',
                            'name',
                            )

    def test_single_workbook_with_all_features(self):
        # create test reader
        test_xls_path = os.path.join(test_files,'testall.xls')
        r = GlobReader(test_xls_path)
        # source sheet must have merged cells for test!
        book = tuple(r.get_workbooks())[0][0]
        self.failUnless(book.sheet_by_index(0).merged_cells)
        # send straight to writer
        w = TestWriter()
        r(w)
        # check stuff on the writer
        self.assertEqual(w.files.keys(),['testall.xls'])
        self.failUnless('testall.xls' in w.closed)
        self.check_file(w,test_xls_path)

    def test_multiple_workbooks(self):
        # globreader is tested elsewhere
        r = GlobReader(os.path.join(test_files,'*.xls'))
        # send straight to writer
        w = TestWriter()
        r(w)
        # check stuff on the writer
        self.assertEqual(w.files.keys(),['test.xls','testall.xls'])
        self.failUnless('test.xls' in w.closed)
        self.failUnless('testall.xls' in w.closed)
        self.check_file(w,os.path.join(test_files,'testall.xls'))
        self.check_file(w,os.path.join(test_files,'test.xls'),
                        18,21,38,37,7,4)
    
    def test_set_rd_sheet(self):
        # also tests that 'row' doesn't have to be called,
        # only cell
        r = TestReader(
            ('Sheet1',(('S1R0C0',),
                       ('S1R1C0',),)),
            ('Sheet2',(('S2R0C0',),
                       ('S2R1C0',),)),
            )
        book = tuple(r.get_workbooks())[0][0]
        # fire methods on writer
        w = TestWriter()
        w.workbook(book,'new.xls')
        w.sheet(book.sheet_by_index(0),'new')
        w.row(0,0)
        w.cell(0,0,0,0)
        w.set_rdsheet(book.sheet_by_index(1))
        w.cell(0,0,1,0)
        w.set_rdsheet(book.sheet_by_index(0))
        w.cell(1,0,2,0)
        w.set_rdsheet(book.sheet_by_index(1))
        w.cell(1,0,3,0)
        w.finish()
        # check everything got written and closed
        self.assertEqual(w.files.keys(),['new.xls'])
        self.failUnless('new.xls' in w.closed)
        # now check the cells written
        f = w.files['new.xls'].file
        a = open_workbook(file_contents=f.read(),pickleable=0,formatting_info=1)
        self.assertEqual(a.nsheets,1)
        sheet = a.sheet_by_index(0)
        self.assertEqual(sheet.nrows,4)
        self.assertEqual(sheet.ncols,1)
        self.assertEqual(sheet.cell(0,0).value,'S1R0C0')
        self.assertEqual(sheet.cell(1,0).value,'S2R0C0')
        self.assertEqual(sheet.cell(2,0).value,'S1R1C0')
        self.assertEqual(sheet.cell(3,0).value,'S2R1C0')
        
    def test_bogus_sheet_name(self):
        r = TestReader(
            ('sheet',([['S1R0C0']]),),
            ('Sheet',([['S2R0C0']]),),
            )
        book = tuple(r.get_workbooks())[0][0]
        # fire methods on writer
        self.assertRaises(ValueError,r,TestWriter())
    
    def test_empty_sheet_name(self):
        r = TestReader(
            ('',([['S1R0C0']]),),
            )
        book = tuple(r.get_workbooks())[0][0]
        # fire methods on writer
        self.assertRaises(ValueError,r,TestWriter())
    
class TestProcess(TestCase):

    def test_setup(self):
        class DummyReader:
            def __call__(self,filter):
                filter.finished()
        F1 = TestCallable()
        F2 = TestCallable()
        process(DummyReader(),F1,F2)
        self.failUnless(F1.next is F2)
        self.failUnless(isinstance(F2.next,TestCallableMethod))
        F1.compare(self,[('finished',())])
        F2.compare(self,())
    
class TestExamples(TestCase):

    def test_mutate_cell(self):
        from xlutils.filter import GlobReader,BaseFilter,process
        class ChangeCell(BaseFilter):
            def cell(self,rdrowx,rdcolx,wtrowx,wtcolx):
                if self.rdsheet.name=='Sheet1' and rdrowx==0 and rdcolx==0:
                    cell = self.rdsheet.cell(rdrowx,rdcolx)
                    self.rdsheet.put_cell(rdrowx,rdcolx,cell.ctype,'Changed',cell.xf_index)
                self.next.cell(rdrowx,rdcolx,wtrowx,wtcolx)
        w = TestWriter()
        process(
            GlobReader(os.path.join(test_files,'testall.xls')),
            ChangeCell(),
            w
            )
        self.assertEqual(w.files.keys(),['testall.xls'])
        f = w.files['testall.xls'].file
        actual = open_workbook(file_contents=f.read(),pickleable=0,formatting_info=1)
        f.close()
        cell = actual.sheet_by_name('Sheet1').cell(0,0)
        self.assertEqual(cell.ctype,XL_CELL_TEXT)
        self.assertEqual(cell.value,'Changed')
        font = actual.font_list[actual.xf_list[cell.xf_index].font_index]
        self.assertEqual(font.underline_type,1)
            
def test_suite():
    return TestSuite((
        makeSuite(TestBaseReader),
        makeSuite(TestTestReader),
        makeSuite(TestBaseFilter),
        makeSuite(TestMethodFilter),
        makeSuite(TestEcho),
        makeSuite(TestMemoryLogger),
        makeSuite(TestErrorFilter),
        makeSuite(TestColumnTrimmer),
        makeSuite(TestBaseWriter),
        makeSuite(TestProcess),
        makeSuite(TestExamples),
        ))
