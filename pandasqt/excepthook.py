# copied and modified from Eric IDE ( credits goes to author )

import time
import cStringIO
import traceback
from pandasqt.compat import QtGui
import codecs
import os
import sys
import tempfile

import pdb

# fallback solution to show a OS independent messagebox
from easygui.boxes.derived_boxes import msgbox

class logFile(object):
    path = os.path.join(tempfile.gettempdir(), "error.log")

    @staticmethod
    def reset():
        logFile.path = os.path.join(tempfile.gettempdir(), "error.log")

def _safeStringConvertion(inputStr):
    try:
        return str(inputStr).decode('utf-8')
    except UnicodeEncodeError, e:
        return unicode(inputStr)

def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.

    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = u'-' * 80

    notice = """An unhandled exception occurred. Please report the problem.\n"""
    notice += """A log has been written to "{}".\n\nError information:""".format(logFile.path)
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    tbinfo = tbinfo.decode('utf-8')

    #try:
        #excValueStr = str(excValue).decode('utf-8')
    #except UnicodeEncodeError, e:
        #excValueStr = unicode(excValue)
    excValueStr = _safeStringConvertion(excValue)

    errmsg = u'{0}: \n{1}'.format(excType, excValueStr)
    sections = [u'\n', separator, timeString, separator, errmsg, separator, tbinfo]
    msg = u'\n'.join(sections)
    try:
        f = codecs.open(logFile.path, "a+", encoding='utf-8')
        f.write(msg)
        f.close()
    except IOError, e:
        _showMessage(u"unable to write to {0}".format(logFile.path))

    _showMessage(unicode(notice) + unicode(msg))

def _showMessage(message):
    # always show an error message
    try:
        if not _isQAppRunning():
            app = QtGui.QApplication([])
        AutoClosingMessageBox.showMessageBox(message)
    except:
        # should only be used if no qt is available at all
        msgbox(message, u"Error")

def _isQAppRunning():
    if QtGui.QApplication.instance() is None:
        return False
    else:
        return True

class AutoClosingMessageBox(QtGui.QMessageBox):

    timeout = 10

    def __init__(self, *__args):
        super(QtGui.QMessageBox, self).__init__(None)
        self.timeout = 0
        self.autoclose = False
        self.currentTime = 0

    def showEvent(self, QShowEvent):
        self.currentTime = 0
        self._updateWindowTitle()
        if self.autoclose:
            self.startTimer(1000)

    def timerEvent(self, *args, **kwargs):
        self.currentTime += 1
        self._updateWindowTitle()
        if self.currentTime >= self.timeout:
            self.done(0)

    def _updateWindowTitle(self):
        self.setWindowTitle("Error, Closing in: {} sec".format(self.timeout - self.currentTime))

    @staticmethod
    def showMessageBox(message):
        msgbox = AutoClosingMessageBox()
        msgbox.autoclose = True
        msgbox.timeout = AutoClosingMessageBox.timeout
        msgbox.setText(message)
        msgbox.setWindowTitle("Error")
        msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgbox.exec_()