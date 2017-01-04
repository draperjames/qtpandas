# from __future__ import unicode_literals
# from __future__ import print_function
# from __future__ import division
# from __future__ import absolute_import
#
# from builtins import open
# from future import standard_library
# standard_library.install_aliases()

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import re
import sys

# TODO: Remove the commented out loop below. Users should take care of the
# PySide or PyQt requirements before they install that way they can decide what
# works best for them. Then we can just use qtpy through the compat.py file
# to handle whatever Qt solution they picked.

# has_qt4 = True
# try:
#     # sip is only needed for PyQt4, they should be imported together.
#     # If we can let's remove all of the references to PyQt or Pyside in favor
#     # of qtpy.
#     import PyQt4
#     # import sip
# except ImportError as e:
#     has_qt4 = False
#
# try:
#     import PySide
# except ImportError as e:
#     if not has_qt4:
#         # We know we failed to import PyQt4/sip...
#         # And we failed to import pyside.
#         raise ImportError("\n\nPlease install PyQt4 and sip or PySide")
#     else:
#         print("Using PyQt4")

here = os.path.abspath(os.path.dirname(__file__))

version_file = open(os.path.join(here, 'qtpandas', '__init__.py'), 'rU')
__version__ = re.sub(
    r".*\b__version__\s+=\s+'([^']+)'.*",
    r'\1',
    [line.strip() for line in version_file if '__version__' in line].pop(0)
)
version_file.close()


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

short_description = """Utilities to use pandas (the data analysis / manipulation
library for Python) with Qt."""

try:
    long_description = read('README.md')
except IOError:
    long_description = "See README.md where installed."


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


tests_require = ["pandas >= 0.17.1",
                 'easygui',
                 'pyqt',
                 # 'pyside',
                 'pytest',
                 'pytest-qt',
                 'pytest-cov',
                 'future',
                 # 'python-magic==0.4.6'
                 ]

setup(
    name='qtpandas',
    version=__version__,
    url='https://github.com/draperjames/qtpandas',
    license='MIT License',
    namespace_packages=['qtpandas'],
    author='Matthias Ludwig, Marcel Radischat, Zeke Barge, James Draper',
    tests_require=tests_require,
    install_requires=[
                      "pandas >= 0.17.1",
                      'easygui',
                      'pytest',
                      'pytest-qt>=1.2.2',
                      'qtpy',
                      'future',
                      'pytest-cov',
                      # 'python-magic==0.4.6'
                      ],

    cmdclass={'test': PyTest},
    author_email='james.draper@duke.edu',
    description=short_description,
    long_description=long_description,
    include_package_data=True,
    packages=['qtpandas'],

    platforms='any',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces'
        ],
    extras_require={
        'testing': tests_require,
    }
)
