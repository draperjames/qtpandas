# -*- coding: utf-8 -*-
"""Easy integration of DataFrame into pyqt framework

@author: Jev Kuznetsov, Matthias Ludwig - Datalyze Solutions
"""

from datetime import datetime

from pandasqt.compat import Qt, QtCore, QtGui, Slot, Signal


import pandas
import numpy

import parser
import re

from pandasqt.models.ColumnDtypeModel import ColumnDtypeModel
from pandasqt.models.DataSearch import DataSearch
from pandasqt.models.SupportedDtypes import SupportedDtypes

DATAFRAME_ROLE = Qt.UserRole + 2


class DataFrameModel(QtCore.QAbstractTableModel):
    """data model for use in QTableView, QListView, QComboBox, etc.

    Attributes:
        timestampFormat (unicode): formatting string for conversion of timestamps to QtCore.QDateTime.
            Used in data method.
        sortingAboutToStart (QtCore.pyqtSignal): emitted directly before sorting starts.
        sortingFinished (QtCore.pyqtSignal): emitted, when sorting finished.
        dtypeChanged (Signal(columnName)): passed from related ColumnDtypeModel
            if a columns dtype has changed.
        changingDtypeFailed (Signal(columnName, index, dtype)):
            passed from related ColumnDtypeModel.
            emitted after a column has changed it's data type.
        dataChanged (Signal):
            Emitted, if data has changed, e.x. finished loading, new columns added or removed.
            It's not the same as layoutChanged.
            Usefull to reset delegates in the view.
    """

    _float_precisions = {
        "float16": numpy.finfo(numpy.float16).precision - 2,
        "float32": numpy.finfo(numpy.float32).precision - 1,
        "float64": numpy.finfo(numpy.float64).precision - 1
    }

    """list of int datatypes for easy checking in data() and setData()"""
    _intDtypes = SupportedDtypes.intTypes() + SupportedDtypes.uintTypes()
    """list of float datatypes for easy checking in data() and setData()"""
    _floatDtypes = SupportedDtypes.floatTypes()
    """list of bool datatypes for easy checking in data() and setData()"""
    _boolDtypes = SupportedDtypes.boolTypes()
    """list of datetime datatypes for easy checking in data() and setData()"""
    _dateDtypes = SupportedDtypes.datetimeTypes()

    _timestampFormat = Qt.ISODate

    sortingAboutToStart = Signal()
    sortingFinished = Signal()
    dtypeChanged = Signal(int, object)
    changingDtypeFailed = Signal(object, QtCore.QModelIndex, object)
    dataChanged = Signal()
    dataFrameChanged = Signal()

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
        self.dataChanged.emit()

        self._dataFrameOriginal = None
        self._search = DataSearch("nothing", "")
        self.editable = False

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
            TypeError: if dataFrame is not of type pandas.core.frame.DataFrame.

        Args:
            dataFrame (pandas.core.frame.DataFrame): assign dataFrame to _dataFrame. Holds all the data displayed.
            copyDataFrame (bool, optional): create a copy of dataFrame or use it as is. defaults to False.
                If you use it as is, you can change it from outside otherwise you have to reset the dataFrame
                after external changes.

        """
        if not isinstance(dataFrame, pandas.core.frame.DataFrame):
            raise TypeError("not of type pandas.core.frame.DataFrame")

        self.layoutAboutToBeChanged.emit()
        if copyDataFrame:
            self._dataFrame = dataFrame.copy()
        else:
            self._dataFrame = dataFrame

        self._columnDtypeModel = ColumnDtypeModel(dataFrame)
        self._columnDtypeModel.dtypeChanged.connect(self.propagateDtypeChanges)
        self._columnDtypeModel.changeFailed.connect(
            lambda columnName, index, dtype: self.changingDtypeFailed.emit(columnName, index, dtype)
        )
        self.layoutChanged.emit()
        self.dataChanged.emit()
        self.dataFrameChanged.emit()

    @Slot(int, object)
    def propagateDtypeChanges(self, column, dtype):
        self.dtypeChanged.emit(column, dtype)

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
        if not isinstance(timestampFormat, (unicode, )):
            raise TypeError('not of type unicode')
        #assert isinstance(timestampFormat, unicode) or timestampFormat.__class__.__name__ == "DateFormat", "not of type unicode"
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
            section if orientation == Qt.Vertical
            None if horizontal orientation and section raises IndexError
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                label = self._dataFrame.columns.tolist()[section]
                if label == section:
                    label = section
                return label
            except (IndexError, ):
                return None
        elif orientation == Qt.Vertical:
            return section

    def data(self, index, role=Qt.DisplayRole):
        """return data depending on index, Qt::ItemDataRole and data type of the column.

        Args:
            index (QtCore.QModelIndex): Index to define column and row you want to return
            role (Qt::ItemDataRole): Define which data you want to return.

        Returns:
            None if index is invalid
            None if role is none of: DisplayRole, EditRole, CheckStateRole, DATAFRAME_ROLE

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

            if role DATAFRAME_ROLE:
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
                # TODO this will most likely always be true
                # See: http://stackoverflow.com/a/715455
                # well no: I am mistaken here, the data is already in the dataframe
                # so its already converted to a bool
                value = bool(self._dataFrame.ix[row, col])

            elif columnDtype in self._dateDtypes:
                #print numpy.datetime64(self._dataFrame.ix[row, col])
                value = pandas.Timestamp(self._dataFrame.ix[row, col])
                value = QtCore.QDateTime.fromString(str(value), self.timestampFormat)
                #print value
            # else:
            #     raise TypeError, "returning unhandled data type"
            return value

        row = self._dataFrame.index[index.row()]
        col = self._dataFrame.columns[index.column()]
        columnDtype = self._dataFrame[col].dtype

        if role == Qt.DisplayRole:
            # return the value if you wanne show True/False as text
            if columnDtype == numpy.bool:
                result = self._dataFrame.ix[row, col]
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
        elif role == DATAFRAME_ROLE:
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

        if not self.editable:
            return flags

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

        Raises:
            TypeError: If the value could not be converted to a known datatype.

        Returns:
            True if value is changed. Calls layoutChanged after update.
            False if value is not different from original value.

        """
        if not index.isValid() or not self.editable:
            return False

        if value != index.data(role):

            self.layoutAboutToBeChanged.emit()

            row = self._dataFrame.index[index.row()]
            col = self._dataFrame.columns[index.column()]
            #print 'before change: ', index.data().toUTC(), self._dataFrame.iloc[row][col]
            columnDtype = self._dataFrame[col].dtype

            if columnDtype == object:
                pass

            elif columnDtype in self._intDtypes:
                dtypeInfo = numpy.iinfo(columnDtype)
                if value < dtypeInfo.min:
                    value = dtypeInfo.min
                elif value > dtypeInfo.max:
                    value = dtypeInfo.max

            elif columnDtype in self._floatDtypes:
                value = numpy.float64(value).astype(columnDtype)

            elif columnDtype in self._boolDtypes:
                value = numpy.bool_(value)

            elif columnDtype in self._dateDtypes:
                # convert the given value to a compatible datetime object.
                # if the conversation could not be done, keep the original
                # value.
                if isinstance(value, QtCore.QDateTime):
                    value = value.toString(self.timestampFormat)
                try:
                    value = pandas.Timestamp(value)
                except Exception:
                    raise Exception, u"Can't convert '{0}' into a datetime".format(value)
                    return False
            else:
                raise TypeError, "try to set unhandled data type"

            self._dataFrame.set_value(row, col, value)

            #print 'after change: ', value, self._dataFrame.iloc[row][col]
            self.layoutChanged.emit()
            return True
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

        After sorting the data in ascending or descending order, a signal
        `layoutChanged` is emitted.

        Args:
            columnId (int): columnIndex
            order (Qt::SortOrder, optional): descending(1) or ascending(0). defaults to Qt.AscendingOrder

        """
        self.layoutAboutToBeChanged.emit()
        self.sortingAboutToStart.emit()
        column = self._dataFrame.columns[columnId]
        self._dataFrame.sort(column, ascending=not bool(order), inplace=True)
        self.layoutChanged.emit()
        self.sortingFinished.emit()

    def setFilter(self, search):
        """apply a filter and hide rows.

        The filter must be a `DataSearch` object, which evaluates a python
        expression.
        If there was an error while parsing the expression, the data will remain
        unfiltered.

        Args:
            search(pandasqt.DataSearch): data search object to use.

        Raises:
            TypeError: An error is raised, if the given parameter is not a
                `DataSearch` object.

        """
        if not isinstance(search, DataSearch):
            raise TypeError('The given parameter must an `pandasqt.DataSearch` object')

        self._search = search

        self.layoutAboutToBeChanged.emit()

        if self._dataFrameOriginal is not None:
            self._dataFrame = self._dataFrameOriginal
        self._dataFrameOriginal = self._dataFrame.copy()

        self._search.setDataFrame(self._dataFrame)
        searchIndex, valid = self._search.search()

        if valid:
            self._dataFrame = self._dataFrame[searchIndex]
            self.layoutChanged.emit()
        else:
            self.clearFilter()
            self.layoutChanged.emit()

        self.dataFrameChanged.emit()

    def clearFilter(self):
        """clear all filters.

        """
        if self._dataFrameOriginal is not None:
            self.layoutAboutToBeChanged.emit()
            self._dataFrame = self._dataFrameOriginal
            self._dataFrameOriginal = None
            self.layoutChanged.emit()

    def columnDtypeModel(self):
        """Getter for a ColumnDtypeModel.

        Returns:
            ColumnDtypeModel
        """
        return self._columnDtypeModel


    def enableEditing(self, editable):
        self.editable = editable
        self._columnDtypeModel.setEditable(self.editable)

    def dataFrameColumns(self):
        return self._dataFrame.columns.tolist()

    def addDataFrameColumn(self, columnName, dtype, defaultValue):
        if not self.editable or dtype not in SupportedDtypes.allTypes():
            return False

        elements = self.rowCount()
        columnPosition = self.columnCount()

        newColumn = pandas.Series([defaultValue]*elements, index=self._dataFrame.index, dtype=dtype)

        self.beginInsertColumns(QtCore.QModelIndex(), columnPosition - 1, columnPosition - 1)
        try:
            self._dataFrame.insert(columnPosition, columnName, newColumn, allow_duplicates=False)
        except ValueError, e:
            # columnName does already exist
            return False

        self.endInsertColumns()

        self.propagateDtypeChanges(columnPosition, newColumn.dtype)

        return True

    def addDataFrameRows(self, count=1):
        # don't allow any gaps in the data rows.
        # and always append at the end

        if not self.editable:
            return False

        position = self.rowCount()

        if count < 1:
            return False

        if len(self.dataFrame().columns) == 0:
            # log an error message or warning
            return False

        # Note: This function emits the rowsAboutToBeInserted() signal which
        # connected views (or proxies) must handle before the data is
        # inserted. Otherwise, the views may end up in an invalid state.
        self.beginInsertRows(QtCore.QModelIndex(), position, position + count - 1)

        defaultValues = []
        for dtype in self._dataFrame.dtypes:
            if dtype.type == numpy.dtype('<M8[ns]'):
                val = pandas.Timestamp('')
            elif dtype.type == numpy.dtype(object):
                val = ''
            else:
                val = dtype.type()
            defaultValues.append(val)

        for i in xrange(count):
            self._dataFrame.loc[position + i] = defaultValues
        self._dataFrame.reset_index()
        self.endInsertRows()
        return True

    def removeDataFrameColumns(self, columns):
        if not self.editable:
            return False

        if columns:
            deleted = 0
            errorOccured = False
            for (position, name) in columns:
                position = position - deleted
                if position < 0:
                    position = 0
                self.beginRemoveColumns(QtCore.QModelIndex(), position, position)
                try:
                    self._dataFrame.drop(name, axis=1, inplace=True)
                except ValueError, e:
                    errorOccured = True
                    continue
                self.endRemoveColumns()
                deleted += 1
            self.dataChanged.emit()

            if errorOccured:
                return False
            else:
                return True
        return False

    def removeDataFrameRows(self, rows):
        if not self.editable:
            return False

        if rows:
            position = min(rows)
            count = len(rows)
            self.beginRemoveRows(QtCore.QModelIndex(), position, position + count - 1)

            removedAny = False
            for idx, line in self._dataFrame.iterrows():
                if idx in rows:
                    removedAny = True
                    self._dataFrame.drop(idx, inplace=True)

            if not removedAny:
                return False

            self._dataFrame.reset_index(inplace=True, drop=True)

            self.endRemoveRows()
            return True
        return False