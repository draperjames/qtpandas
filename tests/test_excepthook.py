# -*- coding: utf-8 -*-
from pandasqt.compat import Qt, QtCore, QtWidgets

import pytest
import pytestqt
import sys
from pandasqt.excepthook import (
    excepthook, AutoClosingMessageBox, _safeStringConvertion as safeStringConvertion, _isQAppRunning,
    logFile
)

testMessages = [
    "Test Test ä",
    u"Test Test ä",
    u"Test Test",
    "Test Test",
]

@pytest.fixture()
def overwriteExcepthook():
    sys.excepthook = excepthook

def test_logFile():
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        assert logFile.path == "/tmp/error.log"
    elif _platform == "darwin":
        # OS X
        pass
    elif _platform == "win32":
        assert logFile.path == "c:\TEMP\error.log"

def test_overwrite(overwriteExcepthook):
    assert True

def test_isQtAppRunning(overwriteExcepthook):
    #assert _isQAppRunning() == False
    app = QtWidgets.QApplication([])
    assert _isQAppRunning()

class TestLogFile(object):

    def test_filePathNotExisting(self, qtbot, overwriteExcepthook):

        def exception():
            raise ValueError("Test")

        widget = QtWidgets.QPushButton("raise exceptions")
        widget.clicked.connect(exception)
        qtbot.addWidget(widget)

        logFile.path = "/abcde/logfile"
        AutoClosingMessageBox.timeout = 2

        qtbot.mouseClick(widget, Qt.LeftButton)
        assert sys.last_type is ValueError
        #assert safeStringConvertion(sys.last_value) == safeStringConvertion(exceptionMessage)
        logFile.reset()

class TestWithQt(object):

    @pytest.mark.parametrize(
        "inputStr", [testMessages[0], testMessages[1], testMessages[2], testMessages[3]]
    )
    def test_safeStringConvertion(self, inputStr):
        safeStringConvertion(inputStr)

    @pytest.mark.parametrize(
        "exceptionType, exceptionMessage",
        [
            (ValueError, testMessages[0]),
            (ValueError, testMessages[1]),
            (ValueError, testMessages[2]),
            (ValueError, testMessages[3]),
        ]
    )
    def test_raising(self, qtbot, overwriteExcepthook, exceptionType, exceptionMessage):

        def exception():
            raise exceptionType(exceptionMessage)

        widget = QtWidgets.QPushButton("raise exceptions")
        widget.clicked.connect(exception)
        qtbot.addWidget(widget)

        # set a minimal timeout
        AutoClosingMessageBox.timeout = 1

        qtbot.mouseClick(widget, Qt.LeftButton)
        assert sys.last_type is ValueError
        assert safeStringConvertion(sys.last_value) == safeStringConvertion(exceptionMessage)