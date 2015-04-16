Installation Instructions
=========================

If you want to experiment with xlutils, the easiest way to
install it is::

  pip install xlutils

Or, if you're using `zc.buildout`, just specify ``xlutils`` as a
required egg.

If you do not install using easy_install or zc.buildout, you will 
also need to make sure the following python packages are available 
on your PYTHONPATH:

- **xlrd**
   
  You'll need version 0.7.2 or later. Latest versions can be found
  here:

  http://pypi.python.org/pypi/xlrd
    
- **xlwt**

  You'll need version 0.7.3 or later. Latest versions can be found
  here:

  http://pypi.python.org/pypi/xlwt

If you're installing with pip, easy_install or buildout, these
dependencies will automatically be installed for you.

Additionally, if you want to use an
:class:`~xlutils.filter.ErrorFilter`, you should make sure the
following package is installed:

- **errorhandler**

  This can be found here:

  http://pypi.python.org/pypi/errorhandler

Since this is a soft dependency, it will not be installed by
automatically by pip, easy_install or buildout.

.. topic:: Python version requirements

  This package is support on Python 2.5, 2.6 and 2.7 on Linux,
  Mac OS X and Windows.
