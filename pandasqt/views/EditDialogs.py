import re

from pandasqt.compat import QtCore, QtGui, Qt, Slot, Signal

from pandasqt.models.SupportedDtypes import SupportedDtypes

import numpy
from pandas import Timestamp
from pandas.tslib import NaTType

class DefaultValueValidator(QtGui.QValidator):
    def __init__(self, parent=None):
        super(DefaultValueValidator, self).__init__(parent)
        self.dtype = None

        self.intPattern = re.compile('[-+]?\d+')
        self.uintPattern = re.compile('\d+')
        self.floatPattern = re.compile('[+-]? *(?:\d+(?:\.\d*)?|\.\d+)')
        self.boolPattern = re.compile('(1|t|0|f){1}$')

    @Slot(numpy.dtype)
    def validateType(self, dtype):
        self.dtype = dtype


    def fixup(self, string):
        pass

    def validate(self, s, pos):
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

    accepted = Signal(str, object, object)

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

        newColumn = self.columnNameLineEdit.text()
        dtype = SupportedDtypes.dtype(self.dataTypeComboBox.currentText())

        defaultValue = self.defaultValueLineEdit.text()
        try:
            if dtype in SupportedDtypes.intTypes() + SupportedDtypes.uintTypes():
                defaultValue = int(defaultValue)
            elif dtype in SupportedDtypes.floatTypes():
                defaultValue = float(defaultValue)
            elif dtype in SupportedDtypes.boolTypes():
                defaultValue = defaultValue.lower() in ['t', '1']
            elif dtype in SupportedDtypes.datetimeTypes():
                defaultValue = Timestamp(defaultValue)
                if isinstance(defaultValue, NaTType):
                    defaultValue = Timestamp('')
            else:
                defaultValue = dtype.type()
        except ValueError, e:
            defaultValue = dtype.type()

        self.accepted.emit(newColumn, dtype, defaultValue)

    @Slot(int)
    def updateValidatorDtype(self, index):
        (dtype, name) = SupportedDtypes.tupleAt(index)
        self.defaultValueLineEdit.clear()
        self.lineEditValidator.validateType(dtype)


class RemoveAttributesDialog(QtGui.QDialog):

    accepted = Signal(list)

    def __init__(self, columns, parent=None):
        super(RemoveAttributesDialog, self).__init__(parent)
        self.columns = columns
        self.initUi()

    def initUi(self):
        self.setWindowTitle(self.tr('Remove Attributes'))
        self.setModal(True)
        self.resize(366, 274)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

        self.gridLayout = QtGui.QGridLayout(self)

        self.dialogHeading = QtGui.QLabel(self.tr('Select the attribute column(s) which shall be removed'), self)

        self.listView = QtGui.QListView(self)

        model = QtGui.QStandardItemModel()
        for column in self.columns:
            item = QtGui.QStandardItem(column)
            model.appendRow(item)

        self.listView.setModel(model)
        self.listView.setSelectionMode(QtGui.QListView.MultiSelection)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.dialogHeading, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.listView, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)



    def accept(self):
        selection = self.listView.selectedIndexes()
        names = []
        for index in selection:
            position = index.row()
            names.append((position, index.data(QtCore.Qt.DisplayRole)))

        super(RemoveAttributesDialog, self).accept()
        self.accepted.emit(names)