from pandasqt.compat import QtCore, QtGui, Qt

from pandasqt.translation import DTypeTranslator
from pandasqt.models.SupportedDtypes import SupportedDtypes

import numpy

class DefaultValueValidator(QtGui.QValidator):
    def __init__(self, parent=None):
        super(DefaultValueValidator, self).__init__(parent)
        self.dtype = None

    @QtCore.pyqtSlot(numpy.dtype)
    def validateType(self, dtype):
        self.dtype = dtype

    def validate(self, string, position):
        if self.dtype in SupportedDtypes.intTypes():
            pass

        if self.dtype in SupportedDtypes.uintTypes():
            pass

        if self.dtype in SupportedDtypes.floatTypes():
            pass

        if self.dtype in SupportedDtypes.strTypes():
            pass

        if self.dtype in SupportedDtypes.boolTypes():
            pass

        if self.dtype in SupportedDtypes.datetimeTypes():
            pass

class AddAttributesDialog(QtGui.QDialog):

    accepted = QtCore.pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(AddAttributesDialog, self).__init__(parent)

        self.initUi()

    def initUi(self):
        self.setModal(True)
        self.resize(303, 168)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)

        self.verticalLayout = QtGui.QVBoxLayout(self)

        self.dialogHeading = QtGui.QLabel(self.tr('Add a new attribute column'), self)

        self.gridLayout = QtGui.QGridLayout()

        self.columnNameLineEdit = QtGui.QLineEdit(self)
        self.columnNameLabel = QtGui.QLabel(self.tr('Name'), self)
        self.dataTypeComboBox = QtGui.QComboBox(self)

        self.dataTypeComboBox.addItems(SupportedDtypes.names())

        self.columnTypeLabel = QtGui.QLabel(self.tr('Type'), self)
        self.defaultValueLineEdit = QtGui.QLineEdit(self)
        self.defaultValueLabel = QtGui.QLabel(self.tr('Inital Value(s)'), self)

        self.gridLayout.addWidget(self.columnNameLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.columnNameLineEdit, 0, 1, 1, 1)

        self.gridLayout.addWidget(self.columnTypeLabel, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.dataTypeComboBox, 1, 1, 1, 1)

        self.gridLayout.addWidget(self.defaultValueLabel, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.defaultValueLineEdit, 2, 1, 1, 1)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.dialogHeading)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)



    def accept(self):
        super(AddAttributesDialog, self).accept()
        self.accepted.emit(())


