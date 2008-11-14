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

However, you can also install by unpacking the source
distribution and placing the 'xlutils' folder somewhere on your 
PYTHONPATH.

If you do not install using easy_install or zc.buildout, you will 
also need to make sure the following python packages are available 
on your PYTHONPATH:

- **xlrd**
   
  This can be found here:

  http://pypi.python.org/pypi/xlrd
    
- **xlwt**

  This can be found here:

  http://pypi.python.org/pypi/xlwt

The Utilities
=============

Each of the utilities in described in its own file found in the 'docs'
directory of the package: 

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

Copyright (c) 2008 Simplistix Ltd

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

1.x.0
-----

- link to the documentation for xlutils.display

1.0.0
-----

- initial public release
