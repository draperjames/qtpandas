import logging
log = logging.getLogger(__name__)

import sip
try:
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    sip.setapi('QDate', 2)
    sip.setapi('QDateTime', 2)
    sip.setapi('QTextStream', 2)
    sip.setapi('QTime', 2)
    sip.setapi('QUrl', 2)
except ValueError as e:
    log.error(e)

try:
    from PyQt4 import QtCore as QtCore_
    from PyQt4 import QtGui as QtGui_
    from PyQt4.QtCore import pyqtSlot as Slot, pyqtSignal as Signal
except ImportError as e:
    from PySide import QtCore as QtCore_
    from PySide import QtGui as QtGui_
    from PySide.QtCore import Slot, Signal


QtCore = QtCore_
QtGui = QtGui_
Qt = QtCore_.Qt

__all__ = ['QtCore', 'QtGui', 'Qt', 'Signal', 'Slot']
