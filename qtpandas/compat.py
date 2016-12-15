"""Systematically imports tools needed from PyQt4, PyQt5 and or Pyside as well
as attempts to set sip API values if sip is installed.

@author: qtpandas contributors
"""

import types

import qtpy.QtGui as _QtGui
import qtpy.QtWidgets as _QtWidgets
import qtpy.QtCore as _QtCore

from qtpy.QtCore import (Signal, Slot, Qt)

# QtCore compatility
QtCore = types.ModuleType("QtCore")
QtCore = _QtCore

# QtGui compatility
QtGui = types.ModuleType("QtGui")
QtGui = _QtGui

for sub_mod in dir(_QtWidgets):
    QtGui.__dict__[sub_mod] = _QtWidgets.__dict__[sub_mod]

__all__ = ['QtCore', 'QtGui', 'Qt', 'Signal', 'Slot']
