import logging
log = logging.getLogger(__name__)

import sip
try:
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
except ValueError, e:
    log.error(e)

try:
    from PyQt4 import QtCore as QtCore_
    from PyQt4 import QtGui as QtGui_
except ImportError, e:
    from PySide import QtCore as QtCore_
    from PySide import QtGui as QtGui_


__all__ = ['QtCore', 'QtGui', 'Qt']

QtCore = QtCore_
QtGui = QtGui_
Qt = QtCore_.Qt
