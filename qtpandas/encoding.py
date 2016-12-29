from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import sys
import os
import warnings
BASEDIR = os.path.dirname(os.path.abspath(__file__))

if sys.platform == 'win32':
    # add local folder to path
    lib = os.path.join(BASEDIR, '_lib', 'magic')
    envpath = os.environ['PATH']
    os.environ['PATH'] = ';'.join([lib, envpath])
