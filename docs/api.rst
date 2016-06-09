API Reference
=============

.. automodule:: xlutils.copy
   :members:
   :undoc-members:

.. autofunction:: xlutils.display.quoted_sheet_name

  This returns a string version of the supplied sheet name that is
  safe to display, including encoding the unicode sheet name into a
  string:

  >>> from xlutils.display import quoted_sheet_name
  >>> quoted_sheet_name(u'Price(\xa3)','utf-8')
  b'Price(\xc2\xa3)'

  It also quotes the sheet name if it contains spaces:
  
  >>> quoted_sheet_name(u'My Sheet')
  b"'My Sheet'"

  Single quotes are replaced with double quotes:

  >>> quoted_sheet_name(u"John's Sheet")
  b"'John''s Sheet'"

.. autofunction:: xlutils.display.cell_display

  This returns a string representation of the supplied cell, no matter
  what type of cell it is. Here's some example output:

  >>> import xlrd
  >>> from xlrd.sheet import Cell
  >>> from xlutils.display import cell_display
  >>> from xlutils.compat import PY3
  
  >>> cell_display(Cell(xlrd.XL_CELL_EMPTY, ''))
  'undefined'

  >>> cell_display(Cell(xlrd.XL_CELL_BLANK, ''))
  'blank'

  >>> cell_display(Cell(xlrd.XL_CELL_NUMBER, 1.2))
  'number (1.2000)'

  >>> cell_display(Cell(xlrd.XL_CELL_BOOLEAN, 0))
  'logical (FALSE)'

  >>> cell_display(Cell(xlrd.XL_CELL_DATE, 36892.0))
  'date (2001-01-01 00:00:00)'

  .. some setup

    >>> from xlrd import open_workbook
    >>> from os.path import join

  Erroneous date values will be displayed like this:

  >>> cell_display(Cell(xlrd.XL_CELL_DATE, 1.5))
  'date? (1.500000)'

  .. note:: 

      To display dates correctly, make sure that `datemode` is passed
      and is taken from the `datemode` attribute of the :class:`xlrd.Book` from
      which the cell originated as shown below:

  >>> wb = open_workbook(join(test_files,'date.xls'))
  >>> cell = wb.sheet_by_index(0).cell(0, 0)
  >>> cell_display(cell, wb.datemode)
  'date (2012-04-13 00:00:00)'

  If non-unicode characters are to be displayed, they will be masked
  out:

  >>> cd = cell_display(Cell(xlrd.XL_CELL_TEXT,u'Price (\xa3)'))
  >>> if PY3:
  ...     str(cd) == "text (b'Price (?)')"
  ... else:
  ...     str(cd) == 'text (Price (?))'
  True


  If you want to see these characters, specify an encoding for the
  output string:

  >>> cd = cell_display(Cell(xlrd.XL_CELL_TEXT,u'Price (\xa3)'), encoding='utf-8')
  >>> if PY3:
  ...     str(cd) == "text (b'Price (\\xc2\\xa3)')"
  ... else:
  ...     str(cd) == 'text (Price (\xc2\xa3))'
  True

  Error cells will have their textual description displayed:

  >>> cell_display(Cell(xlrd.XL_CELL_ERROR, 0))
  'error (#NULL!)'

  >>> cell_display(Cell(xlrd.XL_CELL_ERROR, 2000))
  'unknown error code (2000)'

  If you manage to pass a cell with an unknown cell type, an exception
  will be raised:

  >>> cell_display(Cell(69, 0))
  Traceback (most recent call last):
  ...
  Exception: Unknown Cell.ctype: 69

.. automodule:: xlutils.filter
   :members:
   :special-members:

.. module:: xlutils.margins

.. function:: ispunc(character)

  This little helper function returns ``True`` if called with a punctuation
  character and ``False`` with any other:

  >>> from xlutils.margins import ispunc
  >>> ispunc('u')
  False
  >>> ispunc(',')
  True

  It also works fine with unicode characters:

  >>> ispunc(u',')
  True
  >>> ispunc(u'w')
  False

  It does not, however, return sensible answers if called with more
  than one character:

  >>> ispunc(',,,')
  False

.. autofunction:: xlutils.margins.cells_all_junk
  
  This function returns ``True`` if all the cells supplied are junk:

  >>> from xlutils.margins import cells_all_junk
  >>> from xlrd.sheet import Cell,empty_cell
  >>> cells_all_junk([empty_cell,empty_cell,empty_cell])
  True

  But it returns ``False`` as soon as any of the cells supplied are not
  junk:

  >>> from xlrd import XL_CELL_NUMBER
  >>> cells_all_junk([empty_cell,Cell(XL_CELL_NUMBER,1),empty_cell])
  False

  The definition of 'junk' is as follows:

  * Empty cells are junk:

    >>> from xlrd import XL_CELL_EMPTY
    >>> cells_all_junk([Cell(XL_CELL_EMPTY,'')])
    True

  * Blank cells are junk:

    >>> from xlrd import XL_CELL_BLANK
    >>> cells_all_junk([Cell(XL_CELL_BLANK,'')])
    True

  * Number cells containing zero are considered junk:

    >>> from xlrd import XL_CELL_NUMBER
    >>> cells_all_junk([Cell(XL_CELL_NUMBER,0)])
    True

    However, if a number cell contains anything else, it's not junk:

    >>> cells_all_junk([Cell(XL_CELL_NUMBER,1)])
    False

  * Text cells are junk if they don't contain anything:

    >>> from xlrd import XL_CELL_TEXT
    >>> cells_all_junk([Cell(XL_CELL_TEXT,'')])
    True
  
    or if they contain only space characters:

    >>> cells_all_junk([Cell(XL_CELL_TEXT,' \t\n\r')])
    True

    otherwise they aren't considered junk:

    >>> cells_all_junk([Cell(XL_CELL_TEXT,'not junk')])
    False

    However, you can also pass a checker function such as this one:

    >>> def isrubbish(cell): return cell.value=='rubbish'

    Which can then be used to check for junk conditions of your own
    choice: 

    >>> cells_all_junk([Cell(XL_CELL_TEXT,'rubbish')],isrubbish)
    True
    >>> cells_all_junk([Cell(XL_CELL_TEXT,'not rubbish')],isrubbish)
    False
    
    Passing a function like this isn't only limited to text cells:

    >>> def isnegative(cell): return isinstance(cell.value,float) and cell.value<0 or False
	    
    >>> cells_all_junk([Cell(XL_CELL_NUMBER,-1.0)],isnegative)
    True
    >>> cells_all_junk([Cell(XL_CELL_NUMBER,1.0)],isnegative)
    False
 
  * Date, boolean, and error fields are all not considered to be junk:

    >>> from xlrd import XL_CELL_DATE, XL_CELL_BOOLEAN, XL_CELL_ERROR
    >>> cells_all_junk([Cell(XL_CELL_DATE,'')])
    False
    >>> cells_all_junk([Cell(XL_CELL_BOOLEAN,'')])
    False
    >>> cells_all_junk([Cell(XL_CELL_ERROR,'')])
    False

  Be careful, though, as if you call :func:`cells_all_junk` with an empty
  sequence of cells, you'll get True:

  >>> cells_all_junk([])
  True

.. autofunction:: xlutils.margins.number_of_good_rows

  This function returns the number of rows in a sheet that contain
  anything other than junk, as defined by the :func:`~xlutils.margins.cells_all_junk`
  function. 

  For example:

  >>> from xlutils.tests.fixtures import make_sheet
  >>> sheet = make_sheet((
  ...           ('X',' ',' ',' ',' '),
  ...           (' ',' ',' ','X',' '),
  ...           (' ',' ',' ',' ',' '),
  ...           ('X',' ',' ',' ',' '),
  ...           (' ',' ','X',' ',' '),
  ...           (' ',' ',' ',' ',' '),
  ...           ))
  >>> from xlutils.margins import number_of_good_rows
  >>> number_of_good_rows(sheet)
  5

  You can limit the area searched using the `nrows` and `ncols`
  parameters: 

  >>> number_of_good_rows(sheet,nrows=3)
  2
  >>> number_of_good_rows(sheet,ncols=2)
  4
  >>> number_of_good_rows(sheet,ncols=3,nrows=3)
  1

  You can also pass a checking function through to the :func:`~xlutils.margins.cells_all_junk`
  calls:

  >>> number_of_good_rows(sheet,checker=lambda c:c.value=='X')
  0


.. autofunction:: xlutils.margins.number_of_good_cols

  This function returns the number of columns in a sheet that contain
  anything other than junk, as defined by the :func:`~xlutils.margins.cells_all_junk` function.

  For example:

  >>> sheet = make_sheet((
  ...           ('X',' ',' ','X',' ',' '),
  ...           (' ',' ',' ',' ',' ',' '),
  ...           (' ',' ',' ',' ','X',' '),
  ...           (' ','X',' ',' ',' ',' '),
  ...           (' ',' ',' ',' ',' ',' '),
  ...           (' ',' ',' ',' ',' ',' '),
  ...           ))
  >>> from xlutils.margins import number_of_good_cols
  >>> number_of_good_cols(sheet)
  5

  You can limit the area searched using the `nrows` and `ncols`
  parameters: 

  >>> number_of_good_cols(sheet,nrows=2)
  4
  >>> number_of_good_cols(sheet,ncols=2)
  2
  >>> number_of_good_cols(sheet,ncols=3,nrows=3)
  1

  You can also pass a checking function through to the :func:`~xlutils.margins.cells_all_junk`
  calls:

  >>> number_of_good_cols(sheet,checker=lambda c:c.value=='X')
  0

.. automodule:: xlutils.save
   :members:

.. automodule:: xlutils.styles
   :members:
   :special-members:

.. automodule:: xlutils.view
   :members:
   :special-members:

