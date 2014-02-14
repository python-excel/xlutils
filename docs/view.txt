xlutils.view
============

.. currentmodule:: xlutils.view

Iterating over the cells in a :class:`~xlrd.sheet.Sheet` can be
tricky, especially if you want to exclude headers and the like.
This module is designed to make things easier.

For example, to iterate over the cells in the first sheet of a
workbook:

>>> def print_data(rows):
...     for row in rows:
...         for value in row:
...             print value,
...         print

>>> from os.path import join
>>> from xlutils.view import View
>>> view = View(join(test_files,'testall.xls'))
>>> print_data(view[0])
R0C0 R0C1
R1C0 R1C1
A merged cell 
<BLANKLINE>
<BLANKLINE>
More merged cells 

You can also get a sheet by name:

>>> print_data(view['Sheet2'])
R0C0 R0C1
R1C0 R1C1

One helpful feature is that dates are converted to
:class:`~datetime.datetime` objects rather than being left as numbers:

>>> for row in View(join(test_files,'datetime.xls'))[0]:
...     for value in row:
...         print repr(value)
datetime.datetime(2012, 4, 13, 0, 0)
datetime.time(12, 54, 37)
datetime.datetime(2014, 2, 14, 4, 56, 23)

Now, things get really interesting when you start slicing the view of
a sheet:

>>> print_data(view['Sheet1'][:2, :1])
R0C0
R1C0

As you can see, these behave exactly as slices into lists would, with
the first slice being on rows and the second slice being on columns.

Since looking at a sheet and working with the row and column labels
shown is much easier, :class:`Row` and :class:`Col` helpers are
provided. When these are used for the ``stop`` part of a slice, they
are inclusive. For example:

>>> from xlutils.view import Row, Col
>>> print_data(view['Sheet1'][Row(1):Row(2), Col('A'):Col('B')])
R0C0 R0C1
R1C0 R1C1

Finally, to aid with automated tests, there is a :class:`CheckerView`
subclass of :class:`View` that provides :class:`CheckSheet` views onto
sheets in a workbook. These have a :meth:`~CheckSheet.compare` method
that produces informative :class:`AssertionError` exceptions when the
data in the view of the sheet is not as expected:

>>> from xlutils.view import CheckerView
>>> sheet_view = CheckerView(join(test_files,'testall.xls'))[0]
>>> sheet_view[:, Col('A'):Col('A')].compare(
...     ('R0C0', ),
...     ('R0C1', ),
... )
Traceback (most recent call last):
...
AssertionError: Sequence not as expected:
<BLANKLINE>
same:
(('R0C0',),)
<BLANKLINE>
first:
(('R0C1',),)
<BLANKLINE>
second:
((u'R1C0',), (u'A merged cell',), ('',), ('',), (u'More merged cells',))

Use of the :meth:`~CheckSheet.compare` method requires
`testfixtures`__ to be installed.

__ http://www.simplistix.co.uk/software/python/testfixtures

Looking at the implementation of :class:`CheckerView` will also show
you how you can wire in :class:`SheetView` subclasses to provide any
extra methods you may require.
