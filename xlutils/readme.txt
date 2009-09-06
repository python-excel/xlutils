========
xlutils
========

This package provides a collection of utilities for working with Excel
files. Since these utilities may require either or both of the xlrd
and xlwt packages, they are collected together seperately here.

Installation
============

The easyiest way to install xlutils is:

  easy_install xlutils

Or, if you're using zc.buildout, just specify 'xlutils' as 
a required egg.

However, you can also install in the usual python fashion of unpacking
the source distribution and running::

  python setup.py install

If you do not install using easy_install or zc.buildout, you will 
also need to make sure the following python packages are available 
on your PYTHONPATH:

- **xlrd**
   
  This can be found here:

  http://pypi.python.org/pypi/xlrd
    
- **xlwt**

  This can be found here:

  http://pypi.python.org/pypi/xlwt

- **errorhandler**

  This can be found here:

  http://pypi.python.org/pypi/errorhandler

  This package is only required if you wish to use
  xlutils.filter.ErrorFilter.

The Utilities
=============

Each of the utilities in described in its own file found in the 'docs'
directory of the package: 

*copy.txt*
  Tools for copying xlrd.Book objects to xlwt.Workbook objects.

*display.txt*
  Utility functions for displaying information about xlrd-related
  objects in a user-friendly and safe fashion.

*filter.txt*
  A mini framework for splitting and filtering Excel files into new
  Excel files.

*margins.txt*
  Tools for finding how much of an Excel file contains useful data.

*save.txt*
  Tools for serializing xlrd.Book objects back to Excel files.

*styles.txt*
  Tools for working with formatting information expressed in styles.

Development and Testing
=======================

If you wish to develop or add utilities, please see the documentation
in the comment at the top of buildout.cfg in the subversion
repository for details of how to set up an appropriate buildout and
run the tests.

The subversion repository lives here:

https://secure.simplistix.co.uk/svn/xlutils/

Licensing
=========

Copyright (c) 2008-2009 Simplistix Ltd

This Software is released under the MIT License:
http://www.opensource.org/licenses/mit-license.html
See license.txt for more details.

Credits
=======

**Chris Withers**
  Inception and development

**John Machin**
  The excellent xlrd and xlwt libraries

Changes
=======

1.4.1 (6 September 2009)
------------------------

- Removal of references in the `finish` methods of several filters,
  easing memory usage in large filtering runs

- Speed optimisations for xlutils.filter.BaseFilter, bringing those
  benefits to all subclasses.

- Memory usage reduction when using MemoryLogger

1.4.0 (18 August 2009)
----------------------

- Add sheet density information and onesheet option to
  xlutils.margins. 

- Reduced the memory footprint of xlutils.filter.ColumnTrimmer at the
  expense of speed.

- Fixed incorrect warnings about boolean cells in
  xlutils.filter.ErrorFilter. xlwt has always supported boolean
  cells.

- xlutils.filter.BaseReader now opens workbooks with on_demand = True

- Added support for xlrd Books opened with on_demand as True passed to
  open_workbook. 

- Fixed bug when copying error cells.

- Requires the latest versions of xlrd (0.7.1) and xlwt (0.7.2).

1.3.2 (18 June 2009)
-------------------

- Made installation work when `setuptools` isn't present.

- Made `errorhandler` an optional dependency.

1.3.1 (22 May 2009)
-------------------

- In xlutils.styles, handle there case where two names were mapped to the 
  same xfi, but the first one was empty.

1.3.0 (18 Mar 2009)
-------------------

- fix bug that cause BaseWriter to raise exceptions when handling
  source workbooks opened by xlrd 0.7.0 and above where
  formatting_info had been passed as False

- add xlutils.copy

1.2.1 (19 Dec 2008)
-------------------

- add extremely limited formatting_info support to DummyBook and TestReader

- move to testfixtures 1.5.3 for tests

1.2.0 (10 Dec 2008)
-------------------

- add and implement `start` method to components in xlutils.filter.

- fixed bug when using set_rdsheet with ColumnTrimmer.

- improved installation documentation.

- renamed xlutils.styles.CellStyle to more appropriate
  xlutils.styles.NamedStyle.

- improved documentation for xlutils.styles.

- moved to using TestFixtures and Mock for tests.

- moved to using ErrorHandler rather than duplicating code.

1.1.1 (20 Nov 2008)
-------------------

- prevented generation of excessively long sheet names that cause
  Excel to complain.

- added test that will fail if the filesystem used doesn't support
  filenames with +'s in them.

1.1.0 (14 Nov 2008)
-------------------

- link to the documentation for xlutils.display

- tighten up version requirements for xlrd and xlwt

- use style compression in xlutils.filter.BaseWriter

- prevent generation of bogus sheet names in xlutils.filter.BaseWriter

- xlutils.filter.BaseFilter now keeps track of rdbook, simplifying the
  implementation of filters.

- add another example for xlutils.filter

- add xlutils.filter.XLRDReader

- add xlutils.filter.StreamWriter

- add xlutils.styles

- add xlutils.save

1.0.0 (8 Nov 2008)
------------------

- initial public release
