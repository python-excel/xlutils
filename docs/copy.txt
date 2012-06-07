xlutils.copy
============

The function in this module copies :class:`xlrd.Book` objects into
:class:`xlwt.Workbook` objects so they can be manipulated.
You may wish to do this, for example, if you have an existing excel
file where you want to change come cells. 

You would start by opening the file with :mod:`xlrd`:

>>> from os.path import join
>>> from xlrd import open_workbook
>>> rb = open_workbook(join(test_files,'testall.xls'), formatting_info=True, on_demand=True)
>>> rb.sheet_by_index(0).cell(0,0).value
u'R0C0'
>>> rb.sheet_by_index(0).cell(0,1).value
u'R0C1'

You would then use :mod:`xlutils.copy` to copy the :class:`xlrd.Book`
object into an :class:`xlwt.Workbook` object:

>>> from xlutils.copy import copy
>>> wb = copy(rb)

.. paranoid check, no existing files

  >>> temp_dir = TempDirectory()
  >>> temp_dir.listdir()
  No files or directories found.

Now that you have an :class:`xlwt.Workbook`, you can modify cells and
then save the changed workbook back to a file:

>>> wb.get_sheet(0).write(0,0,'changed!')
>>> wb.save(join(temp_dir.path,'output.xls'))
>>> temp_dir.listdir()
output.xls

This file can now be loaded using :mod:`xlrd` to see the changes:

>>> rb = open_workbook(join(temp_dir.path,'output.xls'))
>>> rb.sheet_by_index(0).cell(0,0).value
u'changed!'
>>> rb.sheet_by_index(0).cell(0,1).value
u'R0C1'

.. note:: You should always pass `on_demand=True` to :func:`~xlrd.open_workbook` as this
          uses much less memory!
