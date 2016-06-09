Changes
=======

.. currentmodule:: xlutils

2.0.0 (9 June 2016)
-------------------

- Updated documentation.

- Move to virtualenv/pip based development.

- Move to Read The Docs for documentation.

- Use Travis CI for testing and releases.

- Use features of newer :mod:`testfixtures` in
  :class:`~xlutils.view.CheckerView`.

- Python 3 compatibility.

1.7.1 (25 April 2014)
---------------------

- Add support for time cells in :class:`~xlutils.view.View`.

- Add support for ``.xlsx`` files in :class:`~xlutils.view.View` at the
  expense of formatting information being available.

1.7.0 (29 October 2013)
-----------------------

- Added the :mod:`xlutils.view` module.

1.6.0 (5 April 2013)
--------------------

- Moved documentation to be Sphinx based.

- Support for :mod:`xlrd` 0.9.1, which no longer has pickleable
  books.

  .. note:: You may encounter performance problems if you work with
            large spreadsheets and use :mod:`xlutils` 1.6.0 with
            :mod:`xlrd` versions earlier that 0.9.1. 

1.5.2 (13 April 2012)
---------------------

- When using :mod:`xlutils.copy`, the ``datemode`` is now copied across from the
  source solving date problems with certain files.

- The :mod:`errorhandler` package is no longer a hard dependency.

- As a minimum, :mod:`xlrd` 0.7.2 and :mod:`xlwt` 0.7.4 are now required.

1.5.1 (5 March 2012)
--------------------

- Fix packaging problem caused by the move to git

1.5.0 (5 March 2012)
--------------------

- Take advantage of "ragged rows" optimisation in xlrd 0.7.3

- Add support for PANE records to :mod:`xlutils.copy`, which means that zoom
  factors are now copied.

1.4.1 (6 September 2009)
------------------------

- Removal of references in the `finish` methods of several filters,
  easing memory usage in large filtering runs

- Speed optimisations for :class:`~xlutils.filter.BaseFilter`, bringing those
  benefits to all subclasses.

- Memory usage reduction when using :class:`~xlutils.filter.MemoryLogger`

1.4.0 (18 August 2009)
----------------------

- Add sheet density information and onesheet option to
  :mod:`xlutils.margins`. 

- Reduced the memory footprint of :class:`~xlutils.filter.ColumnTrimmer` at the
  expense of speed.

- Fixed incorrect warnings about boolean cells in
  :class:`~xlutils.filter.ErrorFilter`. :mod:`xlwt` has always supported boolean
  cells.

- :class:`~xlutils.filter.BaseReader` now opens workbooks with ``on_demand = True``

- Added support for :mod:`xlrd` Books opened with ``on_demand`` as ``True`` passed to
  :func:`~xlrd.open_workbook`. 

- Fixed bug when copying error cells.

- Requires the latest versions of :mod:`xlrd` (0.7.1) and :mod:`xlwt` (0.7.2).

1.3.2 (18 June 2009)
--------------------

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
