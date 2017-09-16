# -*- coding:utf-8 -*-

import os
import sys

from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''

install_requires = []

docs_extras = []

yaml_extras = [
    "PyYAML",
]

tests_require = []

testing_extras = tests_require + []

setup(
    name='jqfpy',
    version='0.4.0',
    description='jq for pythonista',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='jq',
    author="podhmo",
    author_email="ababjam61+github@gmail.com",
    url="https://github.com/podhmo/jqfpy",
    packages=find_packages(exclude=["jqfpy.tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
        'yaml': yaml_extras,
        'docs': docs_extras,
    },
    tests_require=tests_require,
    test_suite="jqfpy.tests",
    entry_points="""
    [console_scripts]
    jqfpy=jqfpy.__main__:main
"""
)
