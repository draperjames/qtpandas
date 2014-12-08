# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

try:
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    from PyQt4.QtCore import Qt
except ImportError:
    from PySide import QtCore
    from PySide import QtGui
    from PySide.QtCore import Qt

import numpy
from BigIntSpinbox import BigIntSpinbox
from DataFrameModel import DataFrameModel

def setDelegatesFromDtype(tableView):
    """set delegates depending on columns dtype into passed tableView

    Args:
        tableView (QTableView): tableView to set delegates. Needs a DataFrameModel to be set.

    Returns:
        Dict of QItemDelegates with column name as key. The table view doen't take ownership of set delegates.
            To prevent them garbage collected they have to be saved somewhere else.
            Otherwise segmentation fault is very likely.

    """
    assert isinstance(tableView, QtGui.QTableView), "not of type QtGui.QTableView"
    if tableView.model():
        itemDelegates = {}
        model = tableView.model()
        assert isinstance(model, DataFrameModel), "model not of type DataFrameModel" 
        dataFrame = model.dataFrame()
        for i, columnName in enumerate(dataFrame.columns):
            columnDtype = dataFrame[columnName].dtype
            if columnDtype in model._intDtypes:
                intInfo = numpy.iinfo(columnDtype)
                delegate = BigIntSpinboxDelegate(intInfo.min, intInfo.max)
                itemDelegates[columnName] = delegate
                tableView.setItemDelegateForColumn(i, delegate)
            elif columnDtype in model._floatDtypes:
                floatInfo = numpy.finfo(columnDtype)
                delegate = CustomDoubleSpinboxDelegate(floatInfo.min, floatInfo.max, decimals=model._float_precisions[str(columnDtype)])
                itemDelegates[columnName] = delegate
                tableView.setItemDelegateForColumn(i, delegate)
            elif columnDtype == object:
                delegate = TextDelegate()
                itemDelegates[columnName] = delegate
                tableView.setItemDelegateForColumn(i, delegate)

        return itemDelegates
    else:
        raise AttributeError, "no model set"

class BigIntSpinboxDelegate(QtGui.QItemDelegate):
    """delegate for very big integers.

    Attributes:
        maximum (int or long): minimum allowed number in BigIntSpinbox.
        minimum (int or long): maximum allowed number in BigIntSpinbox.
        singleStep (int): amount of steps to stepUp BigIntSpinbox.

    """

    def __init__(self, minimum=-18446744073709551616, maximum=18446744073709551615, singleStep=1):
        """construct a new instance of a BigIntSpinboxDelegate.

        Args:
            maximum (int or long, optional): minimum allowed number in BigIntSpinbox. defaults to -18446744073709551616.
            minimum (int or long, optional): maximum allowed number in BigIntSpinbox. defaults to 18446744073709551615.
            singleStep (int, optional): amount of steps to stepUp BigIntSpinbox. defaults to 1.
        """
        super(BigIntSpinboxDelegate, self).__init__()
        assert isinstance(minimum, int) or isinstance(minimum, long)
        assert isinstance(maximum, int) or isinstance(maximum, long)
        assert isinstance(singleStep, int)
        self.minimum = minimum
        self.maximum = maximum
        self.singleStep = singleStep

    def createEditor(self, parent, option, index):
        """Returns the widget used to edit the item specified by index for editing. The parent widget and style option are used to control how the editor widget appears.

        Args:
            parent (QWidget): parent widget.
            option (QStyleOptionViewItem): controls how editor widget appears.
            index (QModelIndex): model data index.
        """
        editor = BigIntSpinbox(parent)
        editor.setMinimum(self.minimum)
        editor.setMaximum(self.maximum)
        editor.setSingleStep(self.singleStep)
        return editor

    def setEditorData(self, spinBox, index):
        """Sets the data to be displayed and edited by the editor from the data model item specified by the model index.

        Args:
            spinBox (BigIntSpinbox): editor widget.
            index (QModelIndex): model data index.
        """
        if index.isValid():
            value = index.model().data(index, QtCore.Qt.EditRole)
            spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        """Gets data from the editor widget and stores it in the specified model at the item index.

        Args:
            spinBox (BigIntSpinbox): editor widget.
            model (QAbstractItemModel): parent model.
            index (QModelIndex): model data index.
        """
        if index.isValid():
            spinBox.interpretText()
            value = spinBox.value()
            model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, spinBox, option, index):
        """Updates the editor for the item specified by index according to the style option given.

        Args:
            spinBox (BigIntSpinbox): editor widget.
            option (QStyleOptionViewItem): controls how editor widget appears.
            index (QModelIndex): model data index.
        """
        spinBox.setGeometry(option.rect)


class CustomDoubleSpinboxDelegate(QtGui.QItemDelegate):
    """delegate for big integers.

    Attributes:
        maximum (int or long): minimum allowed number in BigIntSpinbox.
        minimum (int or long): maximum allowed number in BigIntSpinbox.
        singleStep (int): amount of steps to stepUp BigIntSpinbox
        decimals (int): decimals to use

    """

    def __init__(self, minimum, maximum, decimals=2, singleStep=0.1):
        """construct a new instance of a CustomDoubleSpinboxDelegate.

        Args:
            maximum (int or long): minimum allowed number in BigIntSpinbox.
            minimum (int or long): maximum allowed number in BigIntSpinbox.
            singleStep (int, optional): amount of steps to stepUp BigIntSpinbox. defaults to 0.1.
            decimals (int, optional): decimals to use.  defaults to 2.

        """
        super(CustomDoubleSpinboxDelegate, self).__init__()
        assert numpy.issubdtype(minimum, float), "not of any float type"
        assert numpy.issubdtype(maximum, float), "not of any float type"
        assert isinstance(decimals, int), type(decimals)
        assert isinstance(singleStep, float) or isinstance(singleStep, int), "not of any int type"
        self.minimum = minimum
        self.maximum = maximum
        self.decimals = decimals
        self.singleStep = singleStep

    def createEditor(self, parent, option, index):
        """Returns the widget used to edit the item specified by index for editing. The parent widget and style option are used to control how the editor widget appears.

        Args:
            parent (QWidget): parent widget.
            option (QStyleOptionViewItem): controls how editor widget appears.
            index (QModelIndex): model data index.
        """
        editor = QtGui.QDoubleSpinBox(parent)
        editor.setMinimum(self.minimum)
        editor.setMaximum(self.maximum)
        editor.setSingleStep(self.singleStep)
        editor.setDecimals(self.decimals)
        return editor

    def setEditorData(self, spinBox, index):
        """Sets the data to be displayed and edited by the editor from the data model item specified by the model index.

        Args:
            spinBox (QDoubleSpinBox): editor widget.
            index (QModelIndex): model data index.
        """
        value = index.model().data(index, QtCore.Qt.EditRole)
        spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        """Gets data from the editor widget and stores it in the specified model at the item index.

        Args:
            spinBox (QDoubleSpinBox): editor widget.
            model (QAbstractItemModel): parent model.
            index (QModelIndex): model data index.
        """
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        """Updates the editor for the item specified by index according to the style option given.

        Args:
            spinBox (QDoubleSpinBox): editor widget.
            option (QStyleOptionViewItem): controls how editor widget appears.
            index (QModelIndex): model data index.
        """
        editor.setGeometry(option.rect)

class TextDelegate(QtGui.QItemDelegate):
    """delegate for all kind of text."""

    def __init__(self):
        """construct a new instance of a BigIntSpinboxDelegate.

        Args:

        """
        super(TextDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        """Returns the widget used to edit the item specified by index for editing. The parent widget and style option are used to control how the editor widget appears.

        Args:
            parent (QWidget): parent widget.
            option (QStyleOptionViewItem): controls how editor widget appears.
            index (QModelIndex): model data index.
        """
        editor = QtGui.QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        """Sets the data to be displayed and edited by the editor from the data model item specified by the model index.

        Args:
            editor (QtGui.QLineEdit): editor widget.
            index (QModelIndex): model data index.
        """
        if index.isValid():
            value = index.model().data(index, QtCore.Qt.EditRole)
            editor.setText(unicode(value))

    def setModelData(self, editor, model, index):
        """Gets data from the editor widget and stores it in the specified model at the item index.

        Args:
            editor (QtGui.QLineEdit): editor widget.
            model (QAbstractItemModel): parent model.
            index (QModelIndex): model data index.
        """
        if index.isValid():
            value = editor.text()
            model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        """Updates the editor for the item specified by index according to the style option given.

        Args:
            editor (QtGui.QLineEdit): editor widget.
            option (QStyleOptionViewItem): controls how editor widget appears.
            index (QModelIndex): model data index.
        """
        editor.setGeometry(option.rect)