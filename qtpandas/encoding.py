import sys
import os
import warnings
BASEDIR = os.path.dirname(os.path.abspath(__file__))

if sys.platform == 'win32':
    # add local folder to path
    lib = os.path.join(BASEDIR, '_lib', 'magic')
    envpath = os.environ['PATH']
    os.environ['PATH'] = ';'.join([lib, envpath])
