# copied and modified from Eric IDE ( credits goes to author )

import time
import cStringIO
import traceback
from pandasqt.compat import QtGui
import codecs
import os
import tempfile
# fallback solution to show a OS independent messagebox
from easygui.boxes.derived_boxes import msgbox

def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = u'-' * 80

    logFile = os.path.join(tempfile.gettempdir(), "error.log")
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
    except IOError, e:
        msgbox(u"unable to write to {0}".format(logFile), u"Writing error")

    # always show an error message
    try:
        if not _isQAppRunning():
            app = QtGui.QApplication([])
        _showMessageBox(unicode(notice) + unicode(msg))
    except:
        msgbox(unicode(notice) + unicode(msg), u"Error")
    
def _isQAppRunning():
    if QtGui.QApplication.instance() is None:
        return False
    else:
        return True

def _showMessageBox(text):
    errorbox = QtGui.QMessageBox()
    errorbox.setText(text)
    errorbox.exec_()