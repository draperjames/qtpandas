# -*- coding: utf-8 -*-
"""Easy integration of DataFrame into pyqt framework

@author: Matthias Ludwig - Datalyze Solutions
"""

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

import pandas
import numpy as np

import translation

class ColumnDtypeModel(QtCore.QAbstractTableModel):
    """data model returning datatypes per column

    Attributes:
        dtypeChanged (QtCore.pyqtSignal(columnName)): emitted after a column has changed it's data type.
        changingDtypeFailed (QtCore.pyqtSignal(columnName, index, dtype)): emitted after a column has changed it's data type.
    """
    dtypeChanged = QtCore.pyqtSignal(object)
    changingDtypeFailed = QtCore.pyqtSignal(object, QtCore.QModelIndex, object)

    def __init__(self, dataFrame=None, language='en', autoApplyChanges=True):
        """the __init__ method.

        Args:
            dataFrame (pandas.core.frame.DataFrame, optional): initializes the model with given DataFrame. 
                If none is given an empty DataFrame will be set. defaults to None.
            language (str, optional): one of available languages provided by translation.DTypeTranslator: 'python', 'en', 'de'.
                defaults to 'en'.
            autoApplyChanges (bool, optional): apply changes while changing dtype. defaults to True.

        """
        super(ColumnDtypeModel, self).__init__()
        self.headers = ['column', 'data type']
        self._dtypeTranslator = translation.DTypeTranslator(language)

        self._autoApplyChanges = True
        self.setAutoApplyChanges(autoApplyChanges)

        self._dataFrame = pandas.DataFrame()
        if dataFrame is not None:
            self.setDataFrame(dataFrame)

    def dataFrame(self):
        """getter function to _dataFrame. Holds all data.

        Note:
            It's not implemented with python properties to keep Qt conventions.

        """
        return self._dataFrame

    def setDataFrame(self, dataFrame):
        """setter function to _dataFrame. Holds all data.

        Note:
            It's not implemented with python properties to keep Qt conventions.

        Raises:
            AssertionError: if dataFrame is not of type pandas.core.frame.DataFrame.

        Args:
            dataFrame (pandas.core.frame.DataFrame): assign dataFrame to _dataFrame. Holds all the data displayed.

        """
        self.layoutAboutToBeChanged.emit()
        assert isinstance(dataFrame, pandas.core.frame.DataFrame), "not of type pandas.core.frame.DataFrame"
        self._dataFrame = dataFrame
        self.layoutChanged.emit()

    def autoApplyChanges(self):
        """getter to _autoApplyChanges """
        return self._autoApplyChanges

    def setAutoApplyChanges(self, autoApplyChanges):
        """setter to _autoApplyChanges. apply changes while changing dtype.

        Raises:
            AssertionError: if autoApplyChanges is not of type bool.

        Args:
            autoApplyChanges (bool): apply changes while changing dtype.

        """
        assert isinstance(autoApplyChanges, bool), 'not of type bool'
        self._autoApplyChanges = autoApplyChanges

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                return self.headers[section]
            except (IndexError, ):
                return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        col = index.column()
        #row = self._dataFrame.columns[index.column()]
        columnName = self._dataFrame.columns[index.row()]
        columnDtype = self._dataFrame[columnName].dtype

        if role == Qt.DisplayRole:
            if col == 0:
                return columnName
            elif col == 1:
                return self._dtypeTranslator.tr(columnDtype)
            else:
                return None
        elif role == Qt.EditRole:
            if col == 0:
                return columnName
            elif col == 1:
                return self._dtypeTranslator.tr(columnDtype)
            else:
                return None
        elif role == Qt.UserRole:
            if col == 1:
                return columnDtype
            else:
                return None

    def setData(self, index, value, role=Qt.DisplayRole):
        self.layoutAboutToBeChanged.emit()
        if index.isValid():
            #print "value", value
            #print "lookup", self._dtypeTranslator.lookup(value)
            dtype, language = self._dtypeTranslator.lookup(value)

            if dtype is not None:
                #print "compare", np.dtype(index.data(role=Qt.UserRole))
                if dtype != np.dtype(index.data(role=Qt.UserRole)):
                    col = index.column()
                    #row = self._dataFrame.columns[index.column()]
                    columnName = self._dataFrame.columns[index.row()]

                    if self.autoApplyChanges():
                        try:
                            self._dataFrame[columnName] = self._dataFrame[columnName].astype(dtype)
                            self.layoutChanged.emit()
                            self.dtypeChanged.emit(columnName)
                            return True
                        #except ValueError as e:
                            #raise NotImplementedError, "dtype changing not fully working, original error:\n{}".format(e)
                        #except TypeError as e:
                            #raise NotImplementedError, "dtype changing not fully working, original error:\n{}".format(e)
                            #self.changingDtypeFailed.emit(columnName, index, dtype)
                            ##raise e, "cant convert dtype"
                            #return False
                        except Exception as e:
                            raise NotImplementedError, "dtype changing not fully working, original error:\n{}".format(e)
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def flags(self, index):
        """Returns the item flags for the given index as ored value, e.x.: Qt.ItemIsUserCheckable | Qt.ItemIsEditable

        Args:
            index (QtCore.QModelIndex): Index to define column and row

        Returns:
            for column 'column': Qt.ItemIsSelectable | Qt.ItemIsEnabled
            for column 'data type': Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        """
        col = index.column()

        if col == 0:
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

        return flags

    def rowCount(self, index=QtCore.QModelIndex()):
        """returns number of rows

        Args:
            index (QtCore.QModelIndex, optional): Index to define column and row. defaults to empty QModelIndex

        Returns:
            number of rows
        """
        return len(self._dataFrame.columns)

    def columnCount(self, index=QtCore.QModelIndex()):
        """returns number of columns

        Args:
            index (QtCore.QModelIndex, optional): Index to define column and row. defaults to empty QModelIndex

        Returns:
            number of columns
        """
        return len(self.headers)

class DtypeComboDelegate(QtGui.QItemDelegate):
    """Combobox to set dtypes in a ColumnDtypeModel. 
    Parent has to be a QTableView with a set model of type ColumnDtypeModel.

    """
    def __init__(self, parent):
        super(DtypeComboDelegate, self).__init__(parent)
        assert isinstance(parent.model(), ColumnDtypeModel)
        if hasattr(parent.model(), '_dtypeTranslator'):
            _dtypeTranslator = parent.model()._dtypeTranslator
            self._options = _dtypeTranslator.translationTuple()
        else:
            self._options = ('')

    def createEditor(self, parent, option, index):
        combo = QtGui.QComboBox(parent)
        combo.addItems(self._options)
        combo.currentIndexChanged.connect(self.currentIndexChanged)
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(editor.currentIndex())
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.itemText(editor.currentIndex()))

    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())