# -*- coding: utf-8 -*-


from pandasqt.compat import Qt, QtCore, QtGui

import numpy
from pandasqt.views.BigIntSpinbox import BigIntSpinbox
from pandasqt.models.DataFrameModel import DataFrameModel
from pandasqt.models.SupportedDtypes import SupportedDtypes

def createDelegate(dtype, column, view):
    try:
        model = view.model()
    except AttributeError:
        raise

    if model is None:
        raise ValueError('no model set for the current view')

    if not isinstance(model, DataFrameModel):
        raise TypeError('model is not of type DataFrameModel')

    if dtype in model._intDtypes:
        intInfo = numpy.iinfo(dtype)
        delegate = BigIntSpinboxDelegate(intInfo.min, intInfo.max, parent=view)
    elif dtype in model._floatDtypes:
        floatInfo = numpy.finfo(dtype)
        delegate = CustomDoubleSpinboxDelegate(floatInfo.min, floatInfo.max, decimals=model._float_precisions[str(dtype)], parent=view)
    elif dtype == object:
        delegate = TextDelegate(parent=view)
    else:
        delegate = None

    # get old delegate
    oldDelegate = view.itemDelegateForColumn(column)
    if oldDelegate is not None:
        del oldDelegate
    # update the view
    view.setItemDelegateForColumn(column, delegate)
    return delegate

class BigIntSpinboxDelegate(QtGui.QItemDelegate):
    """delegate for very big integers.

    Attributes:
        maximum (int or long): minimum allowed number in BigIntSpinbox.
        minimum (int or long): maximum allowed number in BigIntSpinbox.
        singleStep (int): amount of steps to stepUp BigIntSpinbox.

    """

    def __init__(self, minimum=-18446744073709551616, maximum=18446744073709551615, singleStep=1, parent=None):
        """construct a new instance of a BigIntSpinboxDelegate.

        Args:
            maximum (int or long, optional): minimum allowed number in BigIntSpinbox. defaults to -18446744073709551616.
            minimum (int or long, optional): maximum allowed number in BigIntSpinbox. defaults to 18446744073709551615.
            singleStep (int, optional): amount of steps to stepUp BigIntSpinbox. defaults to 1.
        """
        super(BigIntSpinboxDelegate, self).__init__(parent)
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
        try:
            editor.setMinimum(self.minimum)
            editor.setMaximum(self.maximum)
            editor.setSingleStep(self.singleStep)
        except TypeError, err:
            # initiate the editor with default values
            pass
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
    """delegate for floats.

    Attributes:
        maximum (float): minimum allowed number in QDoubleSpinBox.
        minimum (float): maximum allowed number in QDoubleSpinBox.
        singleStep (int): amount of steps to stepUp QDoubleSpinBox
        decimals (int): decimals to use

    """

    def __init__(self, minimum, maximum, decimals=2, singleStep=0.1, parent=None):
        """construct a new instance of a CustomDoubleSpinboxDelegate.

        Args:
            maximum (float): minimum allowed number in QDoubleSpinBox.
            minimum (float): maximum allowed number in QDoubleSpinBox.
            singleStep (int, optional): amount of steps to stepUp QDoubleSpinBox. defaults to 0.1.
            decimals (int, optional): decimals to use.  defaults to 2.

        """
        super(CustomDoubleSpinboxDelegate, self).__init__(parent)

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
        try:
            editor.setMinimum(self.minimum)
            editor.setMaximum(self.maximum)
            editor.setSingleStep(self.singleStep)
            editor.setDecimals(self.decimals)
        except TypeError, err:
            # initiate the spinbox with default values.
            pass
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

    def __init__(self, parent=None):
        """construct a new instance of a BigIntSpinboxDelegate.

        Args:

        """
        super(TextDelegate, self).__init__(parent)

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