# -*- coding: utf-8 -*-

from pandasqt.compat import Qt, QtCore, QtGui


import pytest
import pytestqt

import decimal
import numpy
import pandas

from pandasqt.models.DataFrameModel import DataFrameModel, DATAFRAME_ROLE
from pandasqt.models.DataSearch import DataSearch

class TestDataSearch(object):

    @pytest.fixture
    def dataFrame(self):
        data = [
            [0, 1, 2, 3, 4],
            [5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14]
        ]
        columns = ['Foo', 'Bar', 'Spam', 'Eggs', 'Baz']
        dataFrame = pandas.DataFrame(data, columns=columns)
        return dataFrame

    @pytest.fixture
    def geoDataFrame(self):
        data = [
            [0, 1, 2, 3, 4, 49.1234, 8.123],
            [5, 6, 7, 8, 9, 52.1234, 13.123],
            [10, 11, 12, 13, 14, 55.1234, 16.123]
        ]
        columns = ['Foo', 'Bar', 'Spam', 'Eggs', 'Baz', 'lat', 'lng']
        dataFrame = pandas.DataFrame(data, columns=columns)
        return dataFrame

    def test_init(self, dataFrame):
        filterString = 'Foo < 10'
        datasearch = DataSearch("Test", filterString)
        assert datasearch._filterString == filterString
        assert isinstance(datasearch._dataFrame, pandas.DataFrame)
        assert datasearch.name == 'Test'

        datasearch = DataSearch("Test2")
        assert datasearch._filterString == ''
        assert isinstance(datasearch._dataFrame, pandas.DataFrame)
        assert datasearch.name == 'Test2'

        datasearch = DataSearch("Test3", dataFrame=dataFrame)
        assert datasearch._filterString == ''
        assert isinstance(datasearch._dataFrame, pandas.DataFrame)
        assert datasearch.name == 'Test3'
        assert len(datasearch._dataFrame.index) == 3

    def test_repr(self, dataFrame):
        datasearch = DataSearch("Test2")
        assert str(datasearch).startswith('DataSearch(')
        assert str(datasearch).endswith('Test2 ()')

    def test_dataFrame(self, dataFrame):
        datasearch = DataSearch("Test")
        assert datasearch.dataFrame().empty
        assert isinstance(datasearch.dataFrame(), pandas.DataFrame)

        datasearch = DataSearch("Test", dataFrame=dataFrame)
        assert len(datasearch.dataFrame()) == 3

    def test_filterString(self):
        datasearch = DataSearch("Test")
        assert datasearch.filterString() == ''
        datasearch = DataSearch('Test2', filterString='Hello World')
        assert datasearch.filterString() == 'Hello World'

    def test_setFilterString(self):
        datasearch = DataSearch("Test")
        filterString = 'foo bar'
        datasearch.setFilterString(filterString)
        assert datasearch.filterString() == filterString

        filterString = ' foo bar '
        datasearch.setFilterString(filterString)
        assert datasearch.filterString() != filterString
        assert datasearch.filterString() == filterString.strip()

    def test_search(self, dataFrame):
        datasearch = DataSearch('Test', dataFrame=dataFrame)

        filterString = 'Foo < 10'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 2

        filterString = 'Foo < 10 and Bar'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert not valid

        filterString = '(Foo < 10) & (Bar > 1)'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 1

        filterString = '(Monty < 10) & (Bar > 1)'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert not valid

    def test_freeSearch(self, dataFrame):
        datasearch = DataSearch('Test', dataFrame=dataFrame)

        filterString = 'freeSearch("0")'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 2

        filterString = 'freeSearch(1)'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert not valid

        filterString = 'freeSearch("12")'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 1

    def test_extentSearch(self, geoDataFrame, dataFrame):
        datasearch = DataSearch('Test', dataFrame=geoDataFrame)

        filterString = 'extentSearch(51, 9, 55, 14)'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 1

        datasearch = DataSearch('Test', dataFrame=dataFrame)

        filterString = 'extentSearch(51, 9, 55, 14)'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 0

    def test_indexSearch(self, dataFrame):
        datasearch = DataSearch('Test', dataFrame=dataFrame)

        filterString = 'indexSearch([0])'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 1

        filterString = 'indexSearch([0, 2])'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 2

        filterString = 'indexSearch([0, 1, 2])'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 3

        filterString = 'indexSearch([99])'
        datasearch.setFilterString(filterString)
        ret, valid = datasearch.search()
        assert valid
        assert sum(ret) == 0

if __name__ == '__main__':
    pytest.main()