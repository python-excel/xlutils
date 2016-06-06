Development
===========

.. highlight:: bash

This package is developed using continuous integration which can be
found here:

https://travis-ci.org/python-excel/xlutils

If you wish to contribute to this project, then you should fork the
repository found here:

https://github.com/python-excel/xlutils

Development of this package also requires local clones of both
:mod:`xlrd` and :mod:`xlwt`. The following example will set up local
clones as required, but you should use your own forks so that you may
push back to them::

  git clone git://github.com/python-excel/xlutils.git
  git clone git://github.com/python-excel/xlrd.git
  git clone git://github.com/python-excel/xlwt.git
  cd xlutils

Once you have an appropriate set of local repositories, you can follow
these instructions to perform various development tasks:

Setting up a virtualenv
-----------------------

The recommended way to set up a development environment is to turn
your checkout into a virtualenv and then install the package in
editable form as follows::

  $ virtualenv .
  $ bin/pip install -U -e .[test,build]

You will now also need to install xlrd and xlwt into the virtualenv::

  $ source bin/activate
  $ cd ../xlrd
  $ pip install -e .
  $ cd ../xlwt
  $ pip install -e .

Running the tests
-----------------

Once you've set up a virtualenv, the tests can be run as follows::

  $ bin/nosetests

Building the documentation
--------------------------

The Sphinx documentation is built by doing the following from the
directory containg setup.py::

  cd docs
  make html

Making a release
----------------

To make a release, just update ``versions.txt``, update the change log, tag it
and push to https://github.com/python-excel/xlutils
and Travis CI should take care of the rest.

Once the above is done, make sure to go to
https://readthedocs.org/projects/xlutils/versions/
and make sure the new release is marked as an Active Version.
