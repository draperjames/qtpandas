import re

from pandasqt.compat import QtCore, QtGui, Qt

from pandasqt.translation import DTypeTranslator
from pandasqt.models.SupportedDtypes import SupportedDtypes

import numpy
from pandas import Timestamp

class DefaultValueValidator(QtGui.QValidator):
    def __init__(self, parent=None):
        super(DefaultValueValidator, self).__init__(parent)
        self.dtype = None

        self.intPattern = re.compile('[-+]?\d+')
        self.uintPattern = re.compile('\d+')
        self.floatPattern = re.compile('[+-]? *(?:\d+(?:\.\d*)?|\.\d+)')
        self.boolPattern = re.compile('(1|t|0|f){1}$')

    @QtCore.pyqtSlot(numpy.dtype)
    def validateType(self, dtype):
        self.dtype = dtype


    def fixup(self, string):
        if self.dtype in SupportedDtypes.datetimeTypes():
            string =  string.replace('\w', '')

    def validate(self, s, pos):
        # TODO Check for PySide compability

        if not s:
            # s is emtpy
            return (QtGui.QValidator.Acceptable, s, pos)

        if self.dtype in SupportedDtypes.strTypes():
            return (QtGui.QValidator.Acceptable, s, pos)

        elif self.dtype in SupportedDtypes.boolTypes():
            match = re.match(self.boolPattern, s)
            if match:
                return (QtGui.QValidator.Acceptable, s, pos)
            else:
                return (QtGui.QValidator.Invalid, s, pos)

        elif self.dtype in SupportedDtypes.datetimeTypes():
            try:
                ts = Timestamp(s)
            except ValueError, e:
                return (QtGui.QValidator.Intermediate, s, pos)
            return (QtGui.QValidator.Acceptable, s, pos)

        else:
            dtypeInfo = None
            if self.dtype in SupportedDtypes.intTypes():
                match = re.search(self.intPattern, s)
                if match:
                    try:
                        value = int(match.string)
                    except ValueError, e:
                        return (QtGui.QValidator.Invalid, s, pos)

                    dtypeInfo = numpy.iinfo(self.dtype)

            elif self.dtype in SupportedDtypes.uintTypes():
                match = re.search(self.uintPattern, s)
                if match:
                    try:
                        value = int(match.string)
                    except ValueError, e:
                        return (QtGui.QValidator.Invalid, s, pos)

                    dtypeInfo = numpy.iinfo(self.dtype)

            elif self.dtype in SupportedDtypes.floatTypes():
                match = re.search(self.floatPattern, s)
                print match
                if match:
                    try:
                        value = float(match.string)
                    except ValueError, e:
                        return (QtGui.QValidator.Invalid, s, pos)

                    dtypeInfo = numpy.finfo(self.dtype)


            if dtypeInfo is not None:
                if value >= dtypeInfo.min and value <= dtypeInfo.max:
                    return (QtGui.QValidator.Acceptable, s, pos)
                else:
                    return (QtGui.QValidator.Invalid, s, pos)
            else:
                return (QtGui.QValidator.Invalid, s, pos)

        return (QtGui.QValidator.Invalid, s, pos)


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
        self.lineEditValidator = DefaultValueValidator(self)
        self.defaultValueLineEdit.setValidator(self.lineEditValidator)
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

        self.dataTypeComboBox.currentIndexChanged.connect(self.updateValidatorDtype)
        self.updateValidatorDtype(self.dataTypeComboBox.currentIndex())

    def accept(self):
        super(AddAttributesDialog, self).accept()
        self.accepted.emit((self.columnNameLineEdit.text(),
                            self.dataTypeComboBox.currentText(),
                            self.defaultValueLineEdit.text()))

    @QtCore.pyqtSlot(int)
    def updateValidatorDtype(self, index):
        (dtype, name) = SupportedDtypes.tupleAt(index)
        self.lineEditValidator.clear()
        self.lineEditValidator.validateType(dtype)




