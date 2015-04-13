import sys
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))

if sys.platform == 'win32':
    # add local folder to path
    libs = os.path.join(BASEDIR, '_lib', 'magic')
    sys.path.append(libs)


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


