Development
===========

.. highlight:: bash

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

Setting up the buildout
-----------------------

All development requires that you run the buildout::

  python bootstrap.py
  bin/buildout

Running the tests
-----------------

Once you have a buildout, the tests can be run as follows::

  bin/test

Building the documentation
--------------------------

The Sphinx documentation is built by doing the following from the
directory containg setup.py::

  cd docs
  make html

Making a release
----------------

The first thing to do when making a release is to check that the ReST
to be uploaded to PyPI is valid::

  bin/docpy setup.py --long-description | bin/rst2 html \
    --link-stylesheet \
    --stylesheet=http://www.python.org/styles/styles.css > build/desc.html

Once you're certain everything is as it should be, the following will
build the distribution, upload it to PyPI, register the metadata with
PyPI and upload the Sphinx documentation to PyPI::

  bin/buildout -o
  cd docs
  make clean
  make html
  cd ..
  bin/docpy setup.py sdist upload register upload_sphinx --upload-dir=docs/_build/html

The ``bin/buildout`` will make sure the correct package information is
used.

This should all be done on a unix box so that a `.tgz` source
distribution is produced.
