# copied and modified from Eric IDE ( credits goes to author )

import time
import io
import traceback
from qtpandas.compat import QtGui
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
    separator = '-' * 80

    logFile = os.path.join(tempfile.gettempdir(), "error.log")
    notice = """An unhandled exception occurred. Please report the problem.\n"""
    notice += """A log has been written to "{}".\n\nError information:""".format(logFile)
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    try:
        tbinfo = tbinfo.decode('utf-8')
    except AttributeError as e:
        pass

    try:
        excValueStr = str(excValue).decode('utf-8')
    except UnicodeEncodeError as e:
        excValueStr = str(excValue)

    errmsg = '{0}: \n{1}'.format(excType, excValueStr)
    sections = ['\n', separator, timeString, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)
    try:
        f = codecs.open(logFile, "a+", encoding='utf-8')
        f.write(msg)
        f.close()
    except IOError as e:
        msgbox("unable to write to {0}".format(logFile), "Writing error")

    # always show an error message
    try:
        if not _isQAppRunning():
            app = QtGui.QApplication([])
        _showMessageBox(str(notice) + str(msg))
    except:
        msgbox(str(notice) + str(msg), "Error")


def _isQAppRunning():
    if QtGui.QApplication.instance() is None:
        return False
    else:
        return True


def _showMessageBox(text):
    errorbox = QtGui.QMessageBox()
    errorbox.setText(text)
    errorbox.exec_()
