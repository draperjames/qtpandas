# -*- coding: utf-8 -*-
"""Easy integration of DataFrame into pyqt framework

@author: Jev Kuznetsov, Matthias Ludwig - Datalyze Solutions
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
import numpy
from ColumnDtypeModel import ColumnDtypeModel

class DataFrameModel(QtCore.QAbstractTableModel):
    """data model for use in QTableView, QListView, QComboBox, etc.

    Attributes:
        timestampFormat (unicode): formatting string for conversion of timestamps to QtCore.QDateTime. 
            Used in data method.
        sortingAboutToStart (QtCore.pyqtSignal): emitted directly before sorting starts.
        sortingFinished (QtCore.pyqtSignal): emitted, when sorting finished.
        dtypeChanged (QtCore.pyqtSignal(columnName)): passed from related ColumnDtypeModel
            if a columns dtype has changed.
        changingDtypeFailed (QtCore.pyqtSignal(columnName, index, dtype)): 
            passed from related ColumnDtypeModel.
            emitted after a column has changed it's data type.
    """

    _float_precisions = {
        "float16": numpy.finfo(numpy.float16).precision - 2,
        "float32": numpy.finfo(numpy.float32).precision - 1,
        "float64": numpy.finfo(numpy.float64).precision - 1,
        "float128": numpy.finfo(numpy.float128).precision - 1,
    }

    """list of int datatypes for easy checking in data() and setData()"""
    _intDtypes = [
        numpy.int8,
        numpy.int16,
        numpy.int32,
        numpy.int64,
        numpy.uint8,
        numpy.uint16,
        numpy.uint32,
        numpy.uint64
    ]
    """list of float datatypes for easy checking in data() and setData()"""
    _floatDtypes = [
        numpy.float16,
        numpy.float32,
        numpy.float64,
        numpy.float128,
    ]
    """list of bool datatypes for easy checking in data() and setData()"""
    _boolDtypes = [
        numpy.bool,
        numpy.bool_
    ]
    """list of datetime datatypes for easy checking in data() and setData()"""
    _dateDtypes = [
        numpy.dtype('<M8[ns]')
    ]

    sortingAboutToStart = QtCore.pyqtSignal()
    sortingFinished = QtCore.pyqtSignal()
    dtypeChanged = QtCore.pyqtSignal(object)
    changingDtypeFailed = QtCore.pyqtSignal(object, QtCore.QModelIndex, object)

    def __init__(self, dataFrame=None, copyDataFrame=False):
        """the __init__ method.

        Args:
            dataFrame (pandas.core.frame.DataFrame, optional): initializes the model with given DataFrame. 
                If none is given an empty DataFrame will be set. defaults to None.
            copyDataFrame (bool, optional): create a copy of dataFrame or use it as is. defaults to False.
                If you use it as is, you can change it from outside otherwise you have to reset the dataFrame
                after external changes.

        """
        super(DataFrameModel, self).__init__()

        self._dataFrame = pandas.DataFrame()
        if dataFrame is not None:
            self.setDataFrame(dataFrame, copyDataFrame=copyDataFrame)

        self._timestampFormat = Qt.ISODate

        self._dataFrameOriginal = None

    def dataFrame(self):
        """getter function to _dataFrame. Holds all data.

        Note:
            It's not implemented with python properties to keep Qt conventions.

        """
        return self._dataFrame

    def setDataFrame(self, dataFrame, copyDataFrame=False):
        """setter function to _dataFrame. Holds all data.

        Note:
            It's not implemented with python properties to keep Qt conventions.

        Raises:
            AssertionError: if dataFrame is not of type pandas.core.frame.DataFrame.

        Args:
            dataFrame (pandas.core.frame.DataFrame): assign dataFrame to _dataFrame. Holds all the data displayed.
            copyDataFrame (bool, optional): create a copy of dataFrame or use it as is. defaults to False.
                If you use it as is, you can change it from outside otherwise you have to reset the dataFrame
                after external changes.

        """
        assert isinstance(dataFrame, pandas.core.frame.DataFrame), "not of type pandas.core.frame.DataFrame"
        self.layoutAboutToBeChanged.emit()
        if copyDataFrame:
            self._dataFrame = dataFrame.copy()
        else:
            self._dataFrame = dataFrame

        self._columnDtypeModel = ColumnDtypeModel(dataFrame)
        self._columnDtypeModel.dtypeChanged.connect(
            lambda columnName: self.dtypeChanged.emit(columnName)
        )
        self._columnDtypeModel.changingDtypeFailed.connect(
            lambda columnName, index, dtype: self.changingDtypeFailed.emit(columnName, index, dtype)
        )
        self.layoutChanged.emit()

    @property
    def timestampFormat(self):
        """getter to _timestampFormat"""
        return self._timestampFormat
    
    @timestampFormat.setter
    def timestampFormat(self, timestampFormat):
        """setter to _timestampFormat. Formatting string for conversion of timestamps to QtCore.QDateTime

        Raises:
            AssertionError: if timestampFormat is not of type unicode.

        Args:
            timestampFormat (unicode): assign timestampFormat to _timestampFormat. 
                Formatting string for conversion of timestamps to QtCore.QDateTime. Used in data method.

        """
        assert isinstance(timestampFormat, unicode) or timestampFormat.__class__.__name__ == "DateFormat", "not of type unicode"
        self._timestampFormat = timestampFormat

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """return the header depending on section, orientation and Qt::ItemDataRole

        Args:
            section (int): For horizontal headers, the section number corresponds to the column number. 
                Similarly, for vertical headers, the section number corresponds to the row number.
            orientation (Qt::Orientations):
            role (Qt::ItemDataRole):

        Returns:
            None if not Qt.DisplayRole
            _dataFrame.columns.tolist()[section] if orientation == Qt.Horizontal
            _dataFrame.index.tolist()[section] if orientation == Qt.Vertical
            None if vertical or horizontal orientation and section raises IndexError
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                return self._dataFrame.columns.tolist()[section]
            except (IndexError, ):
                return None
        elif orientation == Qt.Vertical:
            try:
                return self._dataFrame.index.tolist()[section]
            except (IndexError, ):
                return None

    def data(self, index, role=Qt.DisplayRole):
        """return data depending on index, Qt::ItemDataRole and data type of the column.

        Args:
            index (QtCore.QModelIndex): Index to define column and row you want to return
            role (Qt::ItemDataRole): Define which data you want to return.

        Returns:
            None if index is invalid
            None if role is none of: DisplayRole, EditRole, CheckStateRole, UserRole

            if role DisplayRole:
                unmodified _dataFrame value if column dtype is object (string or unicode).
                _dataFrame value as int or long if column dtype is in _intDtypes.
                _dataFrame value as float if column dtype is in _floatDtypes. Rounds to defined precision (look at: _float16_precision, _float32_precision).
                None if column dtype is in _boolDtypes.
                QDateTime if column dtype is numpy.timestamp64[ns]. Uses timestampFormat as conversion template.

            if role EditRole:
                unmodified _dataFrame value if column dtype is object (string or unicode).
                _dataFrame value as int or long if column dtype is in _intDtypes.
                _dataFrame value as float if column dtype is in _floatDtypes. Rounds to defined precision (look at: _float16_precision, _float32_precision).
                _dataFrame value as bool if column dtype is in _boolDtypes.
                QDateTime if column dtype is numpy.timestamp64[ns]. Uses timestampFormat as conversion template.

            if role CheckStateRole:
                Qt.Checked or Qt.Unchecked if dtype is numpy.bool_ otherwise None for all other dtypes.

            if role UserRole:
                unmodified _dataFrame value.

            raises TypeError if an unhandled dtype is found in column.
        """

        if not index.isValid():
            return None

        def convertValue(row, col, columnDtype):
            value = None
            if columnDtype == object:
                value = self._dataFrame.ix[row, col]
            elif columnDtype in self._floatDtypes:
                value = round(float(self._dataFrame.ix[row, col]), self._float_precisions[str(columnDtype)])
            elif columnDtype in self._intDtypes:
                value = int(self._dataFrame.ix[row, col])
            elif columnDtype in self._boolDtypes:
                value = bool(self._dataFrame.ix[row, col])
            elif columnDtype in self._dateDtypes:
                value = numpy.datetime64(self._dataFrame.ix[row, col])
                value = QtCore.QDateTime.fromString(str(value), self.timestampFormat)
            else:
                raise TypeError, "returning unhandled data type"
            return value

        row = self._dataFrame.index[index.row()]
        col = self._dataFrame.columns[index.column()]        
        columnDtype = self._dataFrame[col].dtype

        if role == Qt.DisplayRole:
            # return the value if you wanne show True/False as text
            if columnDtype == numpy.bool:
                result = None
            else:
                result = convertValue(row, col, columnDtype)
        elif role  == Qt.EditRole:
            result = convertValue(row, col, columnDtype)
        elif role  == Qt.CheckStateRole:
            if columnDtype == numpy.bool_:
                if convertValue(row, col, columnDtype):
                    result = Qt.Checked
                else:
                    result = Qt.Unchecked
            else:
                result = None
        elif role == Qt.UserRole:
            result = self._dataFrame.ix[row, col]
        else:
            result = None
        return result

    def flags(self, index):
        """Returns the item flags for the given index as ored value, e.x.: Qt.ItemIsUserCheckable | Qt.ItemIsEditable

        If a combobox for bool values should pop up ItemIsEditable have to set for bool columns too.

        Args:
            index (QtCore.QModelIndex): Index to define column and row

        Returns:
            if column dtype is not boolean Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
            if column dtype is boolean Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        """
        flags = super(DataFrameModel, self).flags(index)

        col = self._dataFrame.columns[index.column()]
        if self._dataFrame[col].dtype == numpy.bool:
            flags |= Qt.ItemIsUserCheckable
        else:
            # if you want to have a combobox for bool columns set this
            flags |= Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role=Qt.DisplayRole):
        """Set the value to the index position depending on Qt::ItemDataRole and data type of the column

        Args:
            index (QtCore.QModelIndex): Index to define column and row.
            value (object): new value.
            role (Qt::ItemDataRole): Use this role to specify what you want to do.

        Returns:
            True if value is changed. Calls layoutChanged after update.
            False if value is not different from original value.
        """
        self.layoutAboutToBeChanged.emit()
        if index.isValid():
            if value != index.data(role):

                row = self._dataFrame.index[index.row()]
                col = self._dataFrame.columns[index.column()]

                columnDtype = self._dataFrame[col].dtype
                if columnDtype == object:
                    value = value
                elif columnDtype in self._intDtypes:
                    dtypeInfo = numpy.iinfo(columnDtype)
                    if value < dtypeInfo.min:
                        value = dtypeInfo.min
                    elif value > dtypeInfo.max:
                        value = dtypeInfo.max

                    #for dtype in [numpy.int8, numpy.int16, numpy.int32, numpy.int64, \
                            #numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64]:
                        #if columnDtype == dtype:
                            #print dtype

                            #dtypeInfo = numpy.iinfo(dtype)
                            #if value < dtypeInfo.min:
                                #value = dtypeInfo.min
                            #elif value > dtypeInfo.max:
                                #value = dtypeInfo.max
                            #break
                elif columnDtype in self._floatDtypes:
                    value = numpy.float64(value).astype(columnDtype)
                    #value = value.astype(columnDtype)
                    #for dtype in [numpy.float16, numpy.float32, numpy.float64]:
                        #if columnDtype == dtype:
                            #return dtype(value)
                            #break

                elif columnDtype in self._boolDtypes:
                    value = numpy.bool_(value)
                elif columnDtype in self._dateDtypes:
                    try:
                        value = numpy.datetime64(value.toString(self.timestampFormat))
                    except AttributeError:
                        value = value
                    except:
                        raise
                else:
                    raise TypeError, "try to set unhandled data type"

                self._dataFrame.set_value(row, col, value)
                self.layoutChanged.emit()
                return True
            else:
                return False
        else:
            return False

    def rowCount(self, index=QtCore.QModelIndex()):
        """returns number of rows

        Args:
            index (QtCore.QModelIndex, optional): Index to define column and row. defaults to empty QModelIndex

        Returns:
            number of rows
        """
        # len(df.index) is faster, so use it:
        # In [12]: %timeit df.shape[0]
        # 1000000 loops, best of 3: 437 ns per loop
        # In [13]: %timeit len(df.index)
        # 10000000 loops, best of 3: 110 ns per loop
        # %timeit df.__len__()
        # 1000000 loops, best of 3: 215 ns per loop
        return len(self._dataFrame.index)

    def columnCount(self, index=QtCore.QModelIndex()):
        """returns number of columns

        Args:
            index (QtCore.QModelIndex, optional): Index to define column and row. defaults to empty QModelIndex

        Returns:
            number of columns
        """
        # speed comparison:
        # In [23]: %timeit len(df.columns)
        # 10000000 loops, best of 3: 108 ns per loop

        # In [24]: %timeit df.shape[1]
        # 1000000 loops, best of 3: 440 ns per loop
        return len(self._dataFrame.columns)

    def sort(self, columnId, order=Qt.AscendingOrder):
        """sort the model column

        Args:
            columnId (int): columnIndex
            order (Qt::SortOrder, optional): descending(1) or ascending(0). defaults to Qt.AscendingOrder

        Returns:
            emits layoutChanged
        """
        self.layoutAboutToBeChanged.emit()
        self.sortingAboutToStart.emit()
        column = self._dataFrame.columns[columnId]
        self._dataFrame.sort(column, ascending=not bool(order), inplace=True)
        self.layoutChanged.emit()
        self.sortingFinished.emit() 

    def setFilter(self, filterCondition):
        """apply a filter and hide rows

        Args:
            filterCondition (): filter to use.
        """
        #filterCondition = u"self._dataFrame['int8_value'] >= 10"

        try:
            self.layoutAboutToBeChanged.emit()
            filterCondition = eval(filterCondition)

            if self._dataFrameOriginal is not None:
                self._dataFrame = self._dataFrameOriginal
            self._dataFrameOriginal = self._dataFrame.copy()
            self._dataFrame = self._dataFrame[filterCondition]
            self.layoutChanged.emit()
        except:
            raise

    def clearFilter(self):
        """clear all filters"""
        if self._dataFrameOriginal is not None:
            self.layoutAboutToBeChanged.emit()
            self._dataFrame = self._dataFrameOriginal
            self._dataFrameOriginal = None
            self.layoutChanged.emit()

    def columnDtypeModel(self):
        """returns a ColumnDtypeModel"""
        return self._columnDtypeModel