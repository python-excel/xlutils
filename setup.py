# Copyright (c) 2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os
from setuptools import setup, find_packages

package_dir = os.path.join(os.path.dirname(__file__),'xlutils')

setup(
    name='xlutils',
    version=file(os.path.join(package_dir,'version.txt')).read().strip(),
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description="Utilities for working with Excel files that require both xlrd and xlwt",
    long_description=open(os.path.join(package_dir,'docs','description.txt')).read(),
    url='https://secure.simplistix.co.uk/svn/xlutils/trunk',
    keywords="excel xls xlrd xlwt",
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    # 'Development Status :: 6 - Mature',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
    'xlrd >= 0.6.1a1',
    'xlwt >= 0.7.1',
    'errorhandler',
    ],
    extras_require=dict(
           test=[
            'mock',
            'testfixtures >= 1.5.3',
            ],
           )
    )

# to build and upload the eggs, do:
# python setup.py sdist bdist_egg bdist_wininst register upload
# ...or...
#  bin/buildout setup setup.py sdist bdist_egg bdist_wininst register upload
# ...on a unix box!

# To check how things will show on pypi, install docutils and then:
# bin/buildout -q setup setup.py --long-description | rst2html.py --link-stylesheet --stylesheet=http://www.python.org/styles/styles.css > dist/desc.html
