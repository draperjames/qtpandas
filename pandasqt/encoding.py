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
except ImportError as e:
    #if sys.platform == 'darwin':
    AUTODETECT = False
    raise ImportError('Please install libmagic')


class Detector(object):

    def __init__(self):
        if AUTODETECT:
            if sys.platform.startswith('darwin'):
                magic_db = None  # Use installation default for compatibility reasons
            else:
                if sys.platform.startswith('linux'):
                    # use the system wide installed version comming with linux, the included magic.mgc might be incompatible
                    magic_db = os.path.join('/usr/share/file', 'magic.mgc')
                else:
                    magic_db = os.path.join(BASEDIR, '_lib', 'magic', 'db', 'magic.mgc')
                if not os.path.exists(magic_db):
                    raise ImportError('Please install libmagic.')
            self._magic = magic.Magic(magic_file=magic_db, mime_encoding=True)
        else:
            self._magic = False

    @property
    def active(self):
        if self._magic:
            return True
        else:
            return False

    def detect(self, filepath):
        """Tries to detect the encoding of given file.

        Args:
            filepath (str): Path of file you want encoding from.

        Returns:
            str representation of encoding or None if no encoding could be detected.
        """
        if self._magic:
            encoding = self._magic.from_file(filepath).decode()
            return encoding
        return None