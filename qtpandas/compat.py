"""Systematically imports tools needed from PyQt4, PyQt5 and or Pyside as well
as attempts to set sip API values if sip is installed.

@author: qtpandas contributors
"""
import qtpy.QtGui as QtGui
import qtpy.QtWidgets as QtWidgets
import qtpy.QtCore as QtCore
from qtpy.QtCore import (Signal, Slot, Qt)

# QtGui compatility
for sub_mod in dir(QtWidgets):
    QtGui.__dict__[sub_mod] = QtWidgets.__dict__[sub_mod]


__all__ = ['QtCore', 'QtGui', 'Qt', 'Signal', 'Slot']
