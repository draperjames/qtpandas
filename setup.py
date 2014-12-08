
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

try:
    import sip
except ImportError as e:
    raise e, "install sip first (comming with PyQt4)"

try:
    import PyQt4
except ImportError as e:
    raise e, "install PyQt4 or PySide"

import pandasqt

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

tests_require = ['pyside', 'pytest', 'pytest-cov', 'pytest-qt']
setup(
    name='pandas-qt',
    version=pandasqt.__version__,
    url='https://github.com/datalyze-solutions/pandas-qt',
    license='MIT License',
    namespace_packages = ['pandasqt'],
    author='Matthias Ludwig',
    tests_require=tests_require,
    install_requires=['pandas >= 0.15.1'],
    cmdclass={'test': PyTest},
    author_email='m.Ludwig@datalyze-solutions.com',
    description='catches exceptions inside qt applications and writes them to a message box and into a log file',
    long_description=long_description,
    packages=['pandasqt'],
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: German',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces'
        ],
    extras_require={
        'testing': tests_require,
    }
)