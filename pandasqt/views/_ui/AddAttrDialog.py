# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddAttributesDialog.ui'
#
# Created: Tue Mar  3 17:09:27 2015
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
        Dialog.resize(264, 157)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 120, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.dialogHeading = QtGui.QLabel(Dialog)
        self.dialogHeading.setGeometry(QtCore.QRect(40, 10, 178, 13))
        self.dialogHeading.setObjectName(_fromUtf8("dialogHeading"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 30, 241, 84))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dataTypeComboBox = QtGui.QComboBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataTypeComboBox.sizePolicy().hasHeightForWidth())
        self.dataTypeComboBox.setSizePolicy(sizePolicy)
        self.dataTypeComboBox.setObjectName(_fromUtf8("dataTypeComboBox"))
        self.gridLayout.addWidget(self.dataTypeComboBox, 1, 1, 1, 1)
        self.columnTypeLabel = QtGui.QLabel(self.widget)
        self.columnTypeLabel.setObjectName(_fromUtf8("columnTypeLabel"))
        self.gridLayout.addWidget(self.columnTypeLabel, 1, 0, 1, 1)
        self.columnNameLineEdit = QtGui.QLineEdit(self.widget)
        self.columnNameLineEdit.setObjectName(_fromUtf8("columnNameLineEdit"))
        self.gridLayout.addWidget(self.columnNameLineEdit, 0, 1, 1, 1)
        self.columnNameLabel = QtGui.QLabel(self.widget)
        self.columnNameLabel.setObjectName(_fromUtf8("columnNameLabel"))
        self.gridLayout.addWidget(self.columnNameLabel, 0, 0, 1, 1)
        self.defaultValueLabel = QtGui.QLabel(self.widget)
        self.defaultValueLabel.setObjectName(_fromUtf8("defaultValueLabel"))
        self.gridLayout.addWidget(self.defaultValueLabel, 2, 0, 1, 1)
        self.defaultValueLineEdit = QtGui.QLineEdit(self.widget)
        self.defaultValueLineEdit.setObjectName(_fromUtf8("defaultValueLineEdit"))
        self.gridLayout.addWidget(self.defaultValueLineEdit, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Add Attribute", None))
        self.dialogHeading.setText(_translate("Dialog", "Add a new Attribute to the data", None))
        self.columnTypeLabel.setText(_translate("Dialog", "Type", None))
        self.columnNameLabel.setText(_translate("Dialog", "Name", None))
        self.defaultValueLabel.setText(_translate("Dialog", "Inital Value", None))

