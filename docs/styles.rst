xlutils.styles
==============

.. currentmodule:: xlutils.styles

This module provides tools for working with formatting information
provided by :mod:`xlrd` relating and expressed in the Excel file as styles.

To use these tools, you need to open the workbook with :mod:`xlrd` and make
sure formatting is enabled:

>>> import os
>>> from xlrd import open_workbook
>>> book = open_workbook(os.path.join(test_files,'testall.xls'), formatting_info=1)

Once you have a :class:`~xlrd.Book` object, you can extract the relevent style
information from it as follows:

>>> from xlutils.styles import Styles
>>> s = Styles(book)

You can now look up style information about any cell:

>>> sheet = book.sheet_by_name('Sheet1')
>>> s[sheet.cell(0,0)]
<xlutils.styles.NamedStyle ...>

.. note:: This is `not` a suitable object for copying styles to a new
    spreadsheet using :mod:`xlwt`. If that is your intention, you're
    recommended to look at :doc:`save` or :doc:`filter`.

If you open up ``testall.xls`` in Microsoft's Excel Viewer or other
suitable software, you'll see that the following information is
correct for cell A1:

>>> A1_style = s[sheet.cell(0,0)]
>>> A1_style.name
u'Style1'

While that may be interesting, the actual style information is locked
away in an ``XF`` record. Thankfully, a :class:`NamedStyle` provides
easy access to this:

>>> A1_xf = A1_style.xf
>>> A1_xf
<xlrd.formatting.XF ...>

Once we have the XF record, for this particular cell, most of the
interesting information is in the font definition for the style:

>>> A1_font = book.font_list[A1_xf.font_index]

Using the book's colour map, you can get the RGB colour for this style,
which is blue in this case:

>>> book.colour_map[A1_font.colour_index]
(0, 0, 128)

You can also see that this style specifies text should be underlined
with a single line:

>>> A1_font.underline_type
1

Finally, the style specifies that text is not displayed with a "strike
through" line:

>>> A1_font.struck_out
0

For completeness, here's the same information but for cell B1:

>>> B1_style = s[sheet.cell(0,1)]
>>> B1_style.name
u'Style2'
>>> B1_font = book.font_list[B1_style.xf.font_index]

In this case, though, the style's colour is green:

>>> book.colour_map[B1_font.colour_index]
(0, 128, 0)

The style specifies that text should not be underlined:

>>> B1_font.underline_type
0

And finally, it specifies that text should be displayed with a "strike
through" line:

>>> B1_font.struck_out
1
