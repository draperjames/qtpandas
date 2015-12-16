# -*- coding: utf-8 -*-

from pandasqt.compat import Qt, QtCore, QtGui


import pytest
import pytestqt

import decimal
import numpy
import pandas

from pandasqt.models.ColumnDtypeModel import ColumnDtypeModel, DTYPE_ROLE
from pandasqt.models.SupportedDtypes import SupportedDtypes
from pandasqt.views.CustomDelegates import DtypeComboDelegate


@pytest.fixture()
def dataframe():
    data = [
        [0, 1, 2, 3, 4],
        [5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14]
    ]
    columns = ['Foo', 'Bar', 'Spam', 'Eggs', 'Baz']
    dataFrame = pandas.DataFrame(data, columns=columns)
    return dataFrame

@pytest.fixture()
def language_values():

    return SupportedDtypes._all


class TestColumnDType(object):
    def test_customDTypeModel_check_init(self):
        model = ColumnDtypeModel()

        assert model.dataFrame().empty == True
        assert model.editable() == False

        model = ColumnDtypeModel(editable=True)
        assert model.editable() == True


    def test_headerData(self):
        model = ColumnDtypeModel()

        ret = model.headerData(0, Qt.Horizontal)
        assert ret == 'column'
        ret = model.headerData(1, Qt.Horizontal)
        assert ret == 'data type'
        ret = model.headerData(2, Qt.Horizontal)
        assert ret == None
        ret = model.headerData(0, Qt.Horizontal, Qt.EditRole)
        assert ret == None
        ret = model.headerData(0, Qt.Vertical)
        assert ret == None

    def test_data(self, dataframe):
        model = ColumnDtypeModel(dataFrame=dataframe)
        index = model.index(0, 0)

        # get data for display role
        ret = index.data()
        assert ret == 'Foo'

        # edit role does the same as display role
        ret = index.data(Qt.EditRole)
        assert ret == 'Foo'

        # datatype only defined for column 1
        ret = index.data(DTYPE_ROLE)
        assert ret == None

        # datatype column
        index = index.sibling(0, 1)
        ret = index.data(DTYPE_ROLE)
        assert ret == numpy.dtype(numpy.int64)
        # check translation / display text
        assert index.data() == 'integer (64 bit)' == SupportedDtypes.description(ret)

        # column not defined
        index = index.sibling(0, 2)
        assert index.data(DTYPE_ROLE) == None

        # invalid index
        index = QtCore.QModelIndex()
        assert model.data(index) == None

        index = model.index(2, 0)

        # get data for display role
        ret = index.data()
        assert ret == 'Spam'

    def test_setData(self, dataframe, language_values, qtbot):
        model = ColumnDtypeModel(dataFrame=dataframe)
        index = model.index(3, 1)
        model.setEditable(True)

        # change all values except datetime
        datetime = ()
        for (expected_type, string) in language_values:
            if expected_type == numpy.dtype('<M8[ns]'):
                datetime = (string, expected_type)
                continue
            else:
                model.setData(index, string)
                assert index.data(DTYPE_ROLE) == expected_type

        assert model.setData(index, 'bool', Qt.DisplayRole) == False

        with pytest.raises(Exception) as err:
            model.setData(index, datetime[0])
        assert "Can't convert a boolean value into a datetime value" in str(err.value)

        # rewrite this with parameters
        for data in [
                ["2012-12-13"],
                ["2012-12-13 19:10"],
                ["2012-12-13 19:10:10"]
        ]:
            df = pandas.DataFrame(data, columns=["datetime"])
            model = ColumnDtypeModel(dataFrame=df)
            index = model.index(0, 0)
            model.setEditable(True)
            assert model.setData(index, "date and time") == True

        # convert datetime to anything else does not work and leave the
        # datatype unchanged. An error message is emitted.

        with qtbot.waitSignal(model.changeFailed):
            model.setData(index, 'bool')

    def test_flags(self, dataframe):
        model = ColumnDtypeModel(dataFrame=dataframe)
        model.setEditable(True)

        index = model.index(0, 0)
        assert model.flags(index) == Qt.ItemIsEnabled | Qt.ItemIsSelectable
        index = index.sibling(0, 1)
        assert model.flags(index) == Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

        index = index.sibling(15, 1)
        assert model.flags(index) == Qt.NoItemFlags

    def test_columnCount(self):
        model = ColumnDtypeModel()
        assert model.columnCount() == 2

    def test_rowCount(self, dataframe):
        model = ColumnDtypeModel()
        assert model.rowCount() == 0

        model.setDataFrame(dataframe)
        assert model.rowCount(5)

    def test_setDataFrame(self, dataframe):
        model = ColumnDtypeModel()

        model.setDataFrame(dataframe)
        assert model.rowCount(5)

        with pytest.raises(TypeError) as err:
            model.setDataFrame(['some', 'neat', 'list', 'entries'])
        assert 'not of type pandas.core.frame.DataFrame' in str(err.value)


class TestDtypeComboDelegate(object):
    def test_editing(self, dataframe, qtbot):
        model = ColumnDtypeModel(dataFrame=dataframe)

        model.setEditable(True)

        tableView = QtGui.QTableView()
        qtbot.addWidget(tableView)

        tableView.setModel(model)
        delegate = DtypeComboDelegate(tableView)
        tableView.setItemDelegateForColumn(1, delegate)
        tableView.show()

        index = model.index(0, 1)
        preedit_data = index.data(DTYPE_ROLE)

        tableView.edit(index)
        editor = tableView.findChildren(QtGui.QComboBox)[0]
        selectedIndex = editor.currentIndex()
        editor.setCurrentIndex(selectedIndex+1)
        postedit_data = index.data(DTYPE_ROLE)

        assert preedit_data != postedit_data

if __name__ == '__main__':
    pytest.main()