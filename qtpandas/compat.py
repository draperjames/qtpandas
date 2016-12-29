"""Systematically imports tools needed from PyQt4, PyQt5 and or Pyside as well
as attempts to set sip API values if sip is installed.

@author: qtpandas contributors
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import qtpy.QtGui as _QtGui
import qtpy.QtWidgets as _QtWidgets
import qtpy.QtCore as _QtCore
from qtpy.QtCore import (Signal, Slot, Qt)
QtGui = _QtGui
QtCore = _QtCore
# QtGui compatility
for sub_mod in dir(_QtWidgets):
    QtGui.__dict__[sub_mod] = _QtWidgets.__dict__[sub_mod]


__all__ = ['QtCore', 'QtGui', 'Qt', 'Signal', 'Slot']
