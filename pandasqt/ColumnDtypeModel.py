# -*- coding: utf-8 -*-
"""Easy integration of DataFrame into pyqt framework

@author: Matthias Ludwig - Datalyze Solutions
"""

from pandasqt.compat import Qt, QtCore, QtGui


import pandas
import numpy as np

import translation

DTYPE_ROLE = Qt.UserRole + 1
DTYPE_CHANGE_ROLE = Qt.UserRole + 3

class ColumnDtypeModel(QtCore.QAbstractTableModel):
    """data model returning datatypes per column

    Attributes:
        dtypeChanged (QtCore.pyqtSignal(columnName)): emitted after a column has changed it's data type.
        changeFailed (QtCore.pyqtSignal('QString')): emitted if a column
            datatype could not be changed. An errormessage is provided.
    """
    dtypeChanged = QtCore.pyqtSignal(object)
    changeFailed = QtCore.pyqtSignal('QString')

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

    def translator(self):
        """getter function to `_dtypeTranslator`. Holds all data.

        Note:
            It's not implemented with python properties to keep Qt conventions.

        """
        return self._dtypeTranslator

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
            TypeError: if dataFrame is not of type pandas.core.frame.DataFrame.

        Args:
            dataFrame (pandas.core.frame.DataFrame): assign dataFrame to _dataFrame. Holds all the data displayed.

        """
        if not isinstance(dataFrame, pandas.core.frame.DataFrame):
            raise TypeError('Argument is not of type pandas.core.frame.DataFrame')

        self.layoutAboutToBeChanged.emit()
        self._dataFrame = dataFrame
        self.layoutChanged.emit()

    def autoApplyChanges(self):
        """getter to _autoApplyChanges """
        return self._autoApplyChanges

    def setAutoApplyChanges(self, autoApplyChanges):
        """setter to _autoApplyChanges. apply changes while changing dtype.

        Raises:
            TypeError: if autoApplyChanges is not of type bool.

        Args:
            autoApplyChanges (bool): apply changes while changing dtype.

        """
        if not isinstance(autoApplyChanges, bool):
            raise TypeError('Argument is not of type bool')
        self._autoApplyChanges = autoApplyChanges

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """defines which labels the view/user shall see.

        Args:
            section (int): the row or column number.
            orientation (Qt.Orienteation): Either horizontal or vertical.
            role (Qt.ItemDataRole, optional): Defaults to `Qt.DisplayRole`.

        Returns
            str if a header for the appropriate section is set and the requesting
                role is fitting, None if not.

        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                return self.headers[section]
            except (IndexError, ):
                return None

    def data(self, index, role=Qt.DisplayRole):
        """Retrieve the data stored in the model at the given `index`.

        Args:
            index (QtCore.QModelIndex): The model index, which points at a
                data object.
            role (Qt.ItemDataRole, optional): Defaults to `Qt.DisplayRole`. You
                have to use different roles to retrieve different data for an
                `index`. Accepted roles are `Qt.DisplayRole`, `Qt.EditRole` and
                `DTYPE_ROLE`.

        Returns:
            None if an invalid index is given, the role is not accepted by the
            model or the column is greater than `1`.
            The column name will be returned if the given column number equals `0`
            and the role is either `Qt.DisplayRole` or `Qt.EditRole`.
            The datatype will be returned, if the column number equals `1`. The
            `Qt.DisplayRole` or `Qt.EditRole` return a human readable, translated
            string, whereas the `DTYPE_ROLE` returns the raw data type.

        """

        # an index is invalid, if a row or column does not exist or extends
        # the bounds of self.columnCount() or self.rowCount()
        # therefor a check for col>1 is unnecessary.
        if not index.isValid():
            return None

        col = index.column()

        #row = self._dataFrame.columns[index.column()]
        columnName = self._dataFrame.columns[index.row()]
        columnDtype = self._dataFrame[columnName].dtype

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if col == 0:
                if columnName == index.row():
                    return index.row()
                return columnName
            elif col == 1:
                return self._dtypeTranslator.tr(columnDtype)
        elif role == DTYPE_ROLE:
            if col == 1:
                return columnDtype
            else:
                return None

    def setData(self, index, value, role=DTYPE_CHANGE_ROLE):
        """Updates the datatype of a column.

        The model must be initated with a dataframe already, since valid
        indexes are necessary. The `value` is a translated description of the
        data type. The translations can be found at
        `pandasqt.translation.DTypeTranslator`.

        If a datatype can not be converted, e.g. datetime to integer, a
        `NotImplementedError` will be raised.

        Args:
            index (QtCore.QModelIndex): The index of the column to be changed.
            value (str): The description of the new datatype, e.g.
                `positive kleine ganze Zahl (16 Bit)`.
            role (Qt.ItemDataRole, optional): The role, which accesses and
                changes data. Defaults to `DTYPE_CHANGE_ROLE`.

        Raises:
            NotImplementedError: If an error during conversion occured.

        Returns:
            bool: `True` if the datatype could be changed, `False` if not or if
                the new datatype equals the old one.

        """
        if role != DTYPE_CHANGE_ROLE or not index.isValid():
            return False

        self.layoutAboutToBeChanged.emit()

        dtype, language = self._dtypeTranslator.lookup(value)
        currentDtype = np.dtype(index.data(role=DTYPE_ROLE))
        if dtype is not None:
            if dtype != currentDtype:
                col = index.column()
                #row = self._dataFrame.columns[index.column()]
                columnName = self._dataFrame.columns[index.row()]

                if self.autoApplyChanges():
                    try:
                        if dtype == np.dtype('<M8[ns]'):
                            self._dataFrame[columnName] = self._dataFrame[columnName].apply(pandas.to_datetime)
                        else:
                            self._dataFrame[columnName] = self._dataFrame[columnName].astype(dtype)
                        self.layoutChanged.emit()
                        self.dtypeChanged.emit(columnName)
                        return True
                    except Exception as e:
                        message = 'Could not change datatype %s of column %s to datatype %s' % (currentDtype, columnName, dtype)
                        self.changeFailed.emit(message)
                        # self._dataFrame[columnName] = self._dataFrame[columnName].astype(currentDtype)
                        # self.layoutChanged.emit()
                        # self.dtypeChanged.emit(columnName)
                        #raise NotImplementedError, "dtype changing not fully working, original error:\n{}".format(e)
        return False


    def flags(self, index):
        """Returns the item flags for the given index as ored value, e.x.: Qt.ItemIsUserCheckable | Qt.ItemIsEditable

        Args:
            index (QtCore.QModelIndex): Index to define column and row

        Returns:
            for column 'column': Qt.ItemIsSelectable | Qt.ItemIsEnabled
            for column 'data type': Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

        """
        if not index.isValid():
            return Qt.NoItemFlags

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

class DtypeComboDelegate(QtGui.QStyledItemDelegate):
    """Combobox to set dtypes in a ColumnDtypeModel.

    Parent has to be a QTableView with a set model of type ColumnDtypeModel.

    """
    def __init__(self, parent=None):
        """Constructs a `DtypeComboDelegate` object with the given `parent`.

        Args:
            parent (Qtcore.QObject, optional): The parent argument causes this
                objected to be owned by Qt instead of PyQt if. Defaults to `None`.

        """
        super(DtypeComboDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        """Creates an Editor Widget for the given index.

        Enables the user to manipulate the displayed data in place. An editor
        is created, which performs the change.
        The widget used will be a `QComboBox` with all available datatypes in the
        `pandas` project.

        Args:
            parent (QtCore.QWidget): Defines the parent for the created editor.
            option (QtGui.QStyleOptionViewItem): contains all the information
                that QStyle functions need to draw the items.
            index (QtCore.QModelIndex): The item/index which shall be edited.

        Returns:
            QtGui.QWidget: he widget used to edit the item specified by index
                for editing.

        """
        translator = index.model().translator()
        combo = QtGui.QComboBox(parent)
        combo.addItems(translator.translationTuple())
        combo.currentIndexChanged.connect(self.currentIndexChanged)
        return combo

    def setEditorData(self, editor, index):
        """Sets the current data for the editor.

        The data displayed has the same value as `index.data(Qt.EditRole)`
        (the translated name of the datatype). Therefor a lookup for all items
        of the combobox is made and the matching item is set as the currently
        displayed item.

        Signals emitted by the editor are blocked during exection of this method.

        Args:
            editor (QtGui.QComboBox): The current editor for the item. Should be
                a `QtGui.QComboBox` as defined in `createEditor`.
            index (QtCore.QModelIndex): The index of the current item.

        """
        editor.blockSignals(True)
        data = index.data()
        dataIndex = editor.findData(data, role=Qt.EditRole)
        editor.setCurrentIndex(dataIndex)
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        """Updates the model after changing data in the editor.

        Args:
            editor (QtGui.QComboBox): The current editor for the item. Should be
                a `QtGui.QComboBox` as defined in `createEditor`.
            model (ColumnDtypeModel): The model which holds the displayed data.
            index (QtCore.QModelIndex): The index of the current item of the model.

        """
        model.setData(index, editor.itemText(editor.currentIndex()))

    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        """Emits a signal after changing the selection for a `QComboBox`.

        """
        self.commitData.emit(self.sender())