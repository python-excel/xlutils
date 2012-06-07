=======
xlutils
=======

This package provides a collection of utilities for working with Excel
files. Since these utilities may require either or both of the xlrd
and xlwt packages, they are collected together here, separate from either
package.

Currently available are:

**xlutils.copy**
  Tools for copying xlrd.Book objects to xlwt.Workbook objects.

**xlutils.display**
  Utility functions for displaying information about xlrd-related
  objects in a user-friendly and safe fashion.

**xlutils.filter**
  A mini framework for splitting and filtering Excel files into new
  Excel files.  

**xlutils.margins**
  Tools for finding how much of an Excel file contains useful data.

**xlutils.save**
  Tools for serializing xlrd.Book objects back to Excel files.

**xlutils.styles**
  Tools for working with formatting information expressed in styles.
