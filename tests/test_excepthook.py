# -*- coding: utf-8 -*-

from pandasqt.compat import Qt, QtCore, QtGui

import pytest
import pytestqt
import sys
from pandasqt.excepthook import excepthook

# TODO write it with pytest...

def exception():
    raise ValueError, "Test Test ä"

def exception2():
    raise ValueError, u"Test Test ä"

def exception3():
    raise ValueError, u"Test Test"

def exception4():
    raise ValueError, "Test Test"

app = QtGui.QApplication([])
sys.excepthook = excepthook
widget = QtGui.QPushButton("raise exceptions")
widget.move(100, 100)
widget.resize(100, 100)
widget.show()
widget.clicked.connect(exception)
widget.clicked.connect(exception2)
widget.clicked.connect(exception3)
widget.clicked.connect(exception4)
app.exec_()
        

#@pytest.fixture()
#def overwriteExcepthook():
    #sys.excepthook = excepthook

#class TestTableViewWidget(object):

    #def test_init(self, qtbot):
        #widget = QtGui.QWidget()
        #qtbot.addWidget(widget)
        #widget.show()
        
    #def test_overwrite(self, overwriteExcepthook):
        #assert True
        
    #def test_raising(self, qtbot, overwriteExcepthook):
        #raise ValueError, "Test Test ä"
        #with pytest.raises(ValueError) as excinfo:
            #raise ValueError, "Test Test ä"
        
        #with pytest.raises(ValueError) as excinfo:
            #raise ValueError, u"Test Test ä"