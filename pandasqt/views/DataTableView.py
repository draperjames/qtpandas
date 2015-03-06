from pandasqt.compat import QtCore, QtGui, Qt

from pandasqt.views.EditDialogs import AddAttributesDialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class DataTableWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DataTableWidget, self).__init__(parent)
        self.initUi()


    def initUi(self):
        self.gridLayout = QtGui.QGridLayout(self)

        self.buttonFrame = QtGui.QFrame(self)
        self.buttonFrame.setMinimumSize(QtCore.QSize(250, 50))
        self.buttonFrame.setMaximumSize(QtCore.QSize(250, 50))
        self.buttonFrame.setFrameShape(QtGui.QFrame.NoFrame)

        self.buttonFrameLayout = QtGui.QGridLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(0, 6, 0, 6)

        self.editButton = QtGui.QToolButton(self.buttonFrame)
        icon = QtGui.QIcon(QtGui.QPixmap(_fromUtf8(':/icons/document-edit.png')))

        self.editButton.setIcon(icon)

        self.addColumnButton = QtGui.QToolButton(self.buttonFrame)
        icon = QtGui.QIcon(QtGui.QPixmap(_fromUtf8(':/icons/edit-table-insert-column-right.png')))

        self.addColumnButton.setIcon(icon)

        self.addRowButton = QtGui.QToolButton(self.buttonFrame)
        icon = QtGui.QIcon(QtGui.QPixmap(_fromUtf8(':/icons/edit-table-insert-row-below.png')))

        self.addRowButton.setIcon(icon)

        self.removeColumnButton = QtGui.QToolButton(self.buttonFrame)
        icon = QtGui.QIcon(QtGui.QPixmap(_fromUtf8(':/icons/edit-table-delete-column.png')))

        self.removeColumnButton.setIcon(icon)

        self.removeRowButton = QtGui.QToolButton(self.buttonFrame)
        icon = QtGui.QIcon(QtGui.QPixmap(_fromUtf8(':/icons/edit-table-delete-row.png')))

        self.removeRowButton.setIcon(icon)

        self.buttons = [self.editButton, self.addColumnButton, self.addRowButton, self.removeColumnButton, self.removeRowButton]

        for index, button in enumerate(self.buttons):
            button.setMinimumSize(QtCore.QSize(36, 36))
            button.setMaximumSize(QtCore.QSize(36, 36))
            button.setIconSize(QtCore.QSize(36, 36))
            button.setCheckable(True)
            self.buttonFrameLayout.addWidget(button, 0, index, 1, 1)

        for button in self.buttons[1:]:
            button.setEnabled(False)

        self.tableView = QtGui.QTableView(self)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)

        self.gridLayout.addWidget(self.buttonFrame, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)

        self.editButton.toggled.connect(self.enableEditing)
        self.addColumnButton.toggled.connect(self.showAddColumnDialog)

    @QtCore.pyqtSlot(bool)
    def enableEditing(self, enabled):
        for button in self.buttons[1:]:
            button.setEnabled(enabled)
            if button.isChecked():
                button.setChecked(False)


    @QtCore.pyqtSlot(tuple)
    def _foobar(self, data=None):
        print data

    @QtCore.pyqtSlot(bool)
    def showAddColumnDialog(self, triggered):
        if triggered:
            dialog = AddAttributesDialog(self)
            dialog.accepted.connect(self._foobar)
            dialog.show()


