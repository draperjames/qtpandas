import sys
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))

if sys.platform == 'win32':
    # add local folder to path
    lib = os.path.join(BASEDIR, '_lib', 'magic')
    envpath = os.environ['PATH']
    os.environ['PATH'] = ';'.join([lib, envpath])

try:
    import magic
    AUTODETECT = True
except ImportError, e:
    if sys.platform == 'darwin':
        raise ImportError('Please install libmagic')
    AUTODETECT = False


class Detector(object):
    def __init__(self):
        if AUTODETECT:
            magic_db = os.path.join(BASEDIR, '_lib', 'magic', 'db', 'magic.mgc')
            self.magic = magic.Magic(magic_file=magic_db, mime_encoding=True)
        else:
            self.magic = False


    def detect(self, filepath):
        if self.magic:
            encoding = self.magic.from_file(filepath)
            return encoding
        return None


