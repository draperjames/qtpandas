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
    #if sys.platform == 'darwin':
    raise ImportError('Please install libmagic')
    AUTODETECT = False


class Detector(object):

    def __init__(self):
        if AUTODETECT:
            if sys.platform.startswith('linux'):
                # use the system wide installed version comming with windows, the included magic.mgc might be incompatible
                magic_db = os.path.join('/usr/share/file', 'magic.mgc')
            else:
                magic_db = os.path.join(BASEDIR, '_lib', 'magic', 'db', 'magic.mgc')
            if not os.path.exists(magic_db):
                raise ImportError('Please install libmagic.')
            self.magic = magic.Magic(magic_file=magic_db, mime_encoding=True)
        else:
            self.magic = False

    def detect(self, filepath):
        if self.magic:
            encoding = self.magic.from_file(filepath)
            return encoding
        return None