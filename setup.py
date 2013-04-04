# Copyright (c) 2008-2013 Simplistix Ltd
# See license.txt for license details.

import os
from setuptools import setup

name = 'xlutils'
base_dir = os.path.dirname(__file__)

package_dir = os.path.join(os.path.dirname(__file__),'xlutils')

setup(
    name='xlutils',
    version=file(os.path.join(base_dir, name, 'version.txt')).read().strip(),
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description="Utilities for working with Excel files that require both xlrd and xlwt",
    long_description=open(os.path.join(base_dir, 'docs', 'description.txt')).read(),
    url='http://www.python-excel.org',
    keywords="excel xls xlrd xlwt",
    classifiers=[
    'Development Status :: 6 - Mature',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
    packages=['xlutils','xlutils.tests'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
    'xlrd >= 0.7.2',
    'xlwt >= 0.7.4',
    ],
    entry_points = {
        'console_scripts': [
            'margins = xlutils.margins:main',
        ],
        },
    extras_require=dict(
           test=[
            'manuel',
            'mock',
            'testfixtures >= 1.6.1',
            'errorhandler',
            ],
           )
    )
