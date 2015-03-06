# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddAttributesDialog.ui'
#
# Created: Fri Mar  6 16:32:51 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(303, 168)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(303, 168))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.dialogHeading = QtGui.QLabel(Dialog)
        self.dialogHeading.setMinimumSize(QtCore.QSize(279, 12))
        self.dialogHeading.setMaximumSize(QtCore.QSize(279, 12))
        self.dialogHeading.setObjectName(_fromUtf8("dialogHeading"))
        self.verticalLayout.addWidget(self.dialogHeading)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dataTypeComboBox = QtGui.QComboBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataTypeComboBox.sizePolicy().hasHeightForWidth())
        self.dataTypeComboBox.setSizePolicy(sizePolicy)
        self.dataTypeComboBox.setObjectName(_fromUtf8("dataTypeComboBox"))
        self.gridLayout.addWidget(self.dataTypeComboBox, 1, 1, 1, 1)
        self.columnTypeLabel = QtGui.QLabel(Dialog)
        self.columnTypeLabel.setObjectName(_fromUtf8("columnTypeLabel"))
        self.gridLayout.addWidget(self.columnTypeLabel, 1, 0, 1, 1)
        self.defaultValueLineEdit = QtGui.QLineEdit(Dialog)
        self.defaultValueLineEdit.setObjectName(_fromUtf8("defaultValueLineEdit"))
        self.gridLayout.addWidget(self.defaultValueLineEdit, 2, 1, 1, 1)
        self.columnNameLineEdit = QtGui.QLineEdit(Dialog)
        self.columnNameLineEdit.setObjectName(_fromUtf8("columnNameLineEdit"))
        self.gridLayout.addWidget(self.columnNameLineEdit, 0, 1, 1, 1)
        self.defaultValueLabel = QtGui.QLabel(Dialog)
        self.defaultValueLabel.setObjectName(_fromUtf8("defaultValueLabel"))
        self.gridLayout.addWidget(self.defaultValueLabel, 2, 0, 1, 1)
        self.columnNameLabel = QtGui.QLabel(Dialog)
        self.columnNameLabel.setObjectName(_fromUtf8("columnNameLabel"))
        self.gridLayout.addWidget(self.columnNameLabel, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setMinimumSize(QtCore.QSize(291, 32))
        self.buttonBox.setMaximumSize(QtCore.QSize(291, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.columnTypeLabel.setBuddy(self.dataTypeComboBox)
        self.defaultValueLabel.setBuddy(self.defaultValueLineEdit)
        self.columnNameLabel.setBuddy(self.columnNameLineEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Add Attribute", None))
        self.dialogHeading.setText(_translate("Dialog", "Add a new Attribute to the data", None))
        self.columnTypeLabel.setText(_translate("Dialog", "Type", None))
        self.defaultValueLabel.setText(_translate("Dialog", "Inital Value", None))
        self.columnNameLabel.setText(_translate("Dialog", "Name", None))

