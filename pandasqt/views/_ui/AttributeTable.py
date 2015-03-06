# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AttributeTable.ui'
#
# Created: Fri Mar  6 15:31:39 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AttributeTable(object):
    def setupUi(self, AttributeTable):
        AttributeTable.setObjectName(_fromUtf8("AttributeTable"))
        AttributeTable.resize(996, 637)
        self.gridLayout = QtGui.QGridLayout(AttributeTable)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QFrame(AttributeTable)
        self.buttonBox.setMinimumSize(QtCore.QSize(250, 50))
        self.buttonBox.setMaximumSize(QtCore.QSize(250, 50))
        self.buttonBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.buttonBox.setFrameShadow(QtGui.QFrame.Raised)
        self.buttonBox.setLineWidth(-1)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.buttonBox)
        self.gridLayout_2.setContentsMargins(0, 5, 0, 5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.editButton = QtGui.QToolButton(self.buttonBox)
        self.editButton.setMinimumSize(QtCore.QSize(36, 36))
        self.editButton.setMaximumSize(QtCore.QSize(36, 36))
        self.editButton.setAutoFillBackground(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/document-edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editButton.setIcon(icon)
        self.editButton.setIconSize(QtCore.QSize(36, 36))
        self.editButton.setObjectName(_fromUtf8("editButton"))
        self.gridLayout_2.addWidget(self.editButton, 0, 0, 1, 1)
        self.addColumnButton = QtGui.QToolButton(self.buttonBox)
        self.addColumnButton.setEnabled(False)
        self.addColumnButton.setMinimumSize(QtCore.QSize(36, 36))
        self.addColumnButton.setMaximumSize(QtCore.QSize(36, 36))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit-table-insert-column-right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addColumnButton.setIcon(icon1)
        self.addColumnButton.setIconSize(QtCore.QSize(48, 48))
        self.addColumnButton.setObjectName(_fromUtf8("addColumnButton"))
        self.buttonGroup = QtGui.QButtonGroup(AttributeTable)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.addColumnButton)
        self.gridLayout_2.addWidget(self.addColumnButton, 0, 1, 1, 1)
        self.addRowButton = QtGui.QToolButton(self.buttonBox)
        self.addRowButton.setEnabled(False)
        self.addRowButton.setMinimumSize(QtCore.QSize(36, 36))
        self.addRowButton.setMaximumSize(QtCore.QSize(36, 36))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit-table-insert-row-below.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addRowButton.setIcon(icon2)
        self.addRowButton.setIconSize(QtCore.QSize(48, 48))
        self.addRowButton.setObjectName(_fromUtf8("addRowButton"))
        self.buttonGroup.addButton(self.addRowButton)
        self.gridLayout_2.addWidget(self.addRowButton, 0, 2, 1, 1)
        self.removeColumnButton = QtGui.QToolButton(self.buttonBox)
        self.removeColumnButton.setEnabled(False)
        self.removeColumnButton.setMinimumSize(QtCore.QSize(36, 36))
        self.removeColumnButton.setMaximumSize(QtCore.QSize(36, 36))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit-table-delete-column.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeColumnButton.setIcon(icon3)
        self.removeColumnButton.setIconSize(QtCore.QSize(48, 48))
        self.removeColumnButton.setObjectName(_fromUtf8("removeColumnButton"))
        self.buttonGroup.addButton(self.removeColumnButton)
        self.gridLayout_2.addWidget(self.removeColumnButton, 0, 3, 1, 1)
        self.removeRowButton = QtGui.QToolButton(self.buttonBox)
        self.removeRowButton.setEnabled(False)
        self.removeRowButton.setMinimumSize(QtCore.QSize(36, 36))
        self.removeRowButton.setMaximumSize(QtCore.QSize(36, 36))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit-table-delete-row.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeRowButton.setIcon(icon4)
        self.removeRowButton.setIconSize(QtCore.QSize(48, 48))
        self.removeRowButton.setObjectName(_fromUtf8("removeRowButton"))
        self.buttonGroup.addButton(self.removeRowButton)
        self.gridLayout_2.addWidget(self.removeRowButton, 0, 4, 1, 1)
        self.gridLayout.addWidget(self.buttonBox, 0, 0, 1, 1)
        self.widget = QtGui.QWidget(AttributeTable)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 1)
        self.tableView = QtGui.QTableView(AttributeTable)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)
        self.actionFoo = QtGui.QAction(AttributeTable)
        self.actionFoo.setCheckable(True)
        self.actionFoo.setChecked(False)
        self.actionFoo.setIcon(icon)
        self.actionFoo.setObjectName(_fromUtf8("actionFoo"))

        self.retranslateUi(AttributeTable)
        QtCore.QMetaObject.connectSlotsByName(AttributeTable)

    def retranslateUi(self, AttributeTable):
        AttributeTable.setWindowTitle(_translate("AttributeTable", "Attribute Table", None))
        self.editButton.setToolTip(_translate("AttributeTable", "Edit Data", None))
        self.editButton.setText(_translate("AttributeTable", "Edit Data", None))
        self.addColumnButton.setText(_translate("AttributeTable", "...", None))
        self.addRowButton.setText(_translate("AttributeTable", "...", None))
        self.removeColumnButton.setText(_translate("AttributeTable", "...", None))
        self.removeRowButton.setText(_translate("AttributeTable", "...", None))
        self.actionFoo.setText(_translate("AttributeTable", "foo", None))

import icons_rc
