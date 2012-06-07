# -*- coding: utf-8 -*-
import sys, os, pkginfo, datetime

pkg_info = pkginfo.Develop(os.path.join(os.path.dirname(__file__),'..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
    ]

intersphinx_mapping = {
    'http://docs.python.org': None,
    'http://packages.python.org/testfixtures/': None,
    # XXX - errorhandler
    # XXX - xlrd
    # XXX - xlwt
    }

# General
source_suffix = '.txt'
master_doc = 'index'
project = pkg_info.name
copyright = '2008-%s Simplistix Ltd' % datetime.datetime.now().year
version = release = pkg_info.version
exclude_trees = ['_build']
unused_docs = ['description']
pygments_style = 'sphinx'

# Options for HTML output
html_theme = 'default'
htmlhelp_basename = project+'doc'

# Options for LaTeX output
latex_documents = [
  ('index',project+'.tex', project+u' Documentation',
   'Simplistix Ltd', 'manual'),
]

