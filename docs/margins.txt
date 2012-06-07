xlutils.margins
===============

.. currentmodule:: xlutils.margins

This combined module and script provide information on how much space
is taken up in an Excel file by cells containing no meaningful data.
If :mod:`xlutils` is installed using ``easy_install``, ``pip`` or
``zc.buildout``, a console script called ``margins`` will be created.

The following example shows how it is used as a script::

  python -m xlutils.margins [options] *.xls

To get a list of the available options, do the following::

  python -m xlutils.margins --help

The module also provides the tools that do the work for the above
script as the helpful :func:`ispunc`, :func:`cells_all_junk`,
:func:`number_of_good_rows` and :func:`number_of_good_cols` functions.

See the :doc:`api` for more information.
