import time
import cStringIO
import traceback
from pandasqt.compat import QtGui
import codecs
import os
def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = u'-' * 80

    logFile = os.path.join(os.getcwd(), "error.log")
    notice = """An unhandled exception occurred. Please report the problem.\n"""
    notice += """A log has been written to "{}".\n\nError information:""".format(logFile)
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    tbinfo = tbinfo.decode('utf-8')

    try:
        excValueStr = str(excValue).decode('utf-8')
    except UnicodeEncodeError, e:
        excValueStr = unicode(excValue)
    
    errmsg = u'{0}: \n{1}'.format(excType, excValueStr)
    sections = [u'\n', separator, timeString, separator, errmsg, separator, tbinfo]
    msg = u'\n'.join(sections)
    try:
        f = codecs.open(logFile, "a+", encoding='utf-8')
        f.write(msg)
        f.close()
    except IOError:
        raise
    print unicode(notice) + unicode(msg)

    if not _isQAppRunning():
        app = QtGui.QApplication([])
    _showMessageBox(unicode(notice) + unicode(msg))
    
def _isQAppRunning():
    if QtGui.QApplication.instance() is None:
        return False
    else:
        return True

def _showMessageBox(text):
    errorbox = QtGui.QMessageBox()
    errorbox.setText(text)
    errorbox.exec_()