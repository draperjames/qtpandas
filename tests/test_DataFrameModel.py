# -*- coding: utf-8 -*-

import sip
try:
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
except ValueError, e:
    raise RuntimeError('Could not set API version (%s): did you import PyQt4 directly?' % e)

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

import pytest
import pytestqt

import decimal
import numpy
import pandas

from pandasqt.DataFrameModel import DataFrameModel

def test_initDataFrame():
    model = DataFrameModel()
    assert model.dataFrame().empty

def test_initDataFrameWithDataFrame():
    dataFrame = pandas.DataFrame([0], columns=['A'])
    model = DataFrameModel(dataFrame)
    assert not model.dataFrame().empty
    assert model.dataFrame() is dataFrame

def test_setDataFrame():
    dataFrame = pandas.DataFrame([0], columns=['A'])
    model = DataFrameModel()
    model.setDataFrame(dataFrame)
    assert not model.dataFrame().empty
    assert model.dataFrame() is dataFrame

    with pytest.raises(AssertionError) as excinfo:
        model.setDataFrame(None)
    assert "pandas.core.frame.DataFrame" in unicode(excinfo.value)

@pytest.mark.parametrize(
    "copy, operator", 
    [
        (True, numpy.not_equal), 
        (False, numpy.equal)
    ]
)
def test_copyDataFrame(copy, operator):
    dataFrame = pandas.DataFrame([0], columns=['A'])
    model = DataFrameModel(dataFrame, copyDataFrame=copy)
    assert operator(id(model.dataFrame()), id(dataFrame))

    model.setDataFrame(dataFrame, copyDataFrame=copy)
    assert operator(id(model.dataFrame()), id(dataFrame))

def test_TimestampFormat():
    model = DataFrameModel()
    assert model.timestampFormat == Qt.ISODate
    newFormat = u"yy-MM-dd hh:mm"
    model.timestampFormat = newFormat
    assert model.timestampFormat == newFormat

    with pytest.raises(AssertionError) as excinfo:
        model.timestampFormat = "yy-MM-dd hh:mm"
    assert "unicode" in unicode(excinfo.value)

#def test_signalUpdate(qtbot):
    #model = DataFrameModel()
    #with qtbot.waitSignal(model.layoutAboutToBeChanged) as layoutAboutToBeChanged:
        #model.signalUpdate()
    #assert layoutAboutToBeChanged.signal_triggered

    #with qtbot.waitSignal(model.layoutChanged) as blocker:
        #model.signalUpdate()
    #assert blocker.signal_triggered

@pytest.mark.parametrize(
    "orientation, role, index, expectedHeader", 
    [
        (Qt.Horizontal, Qt.EditRole, 0, None),
        (Qt.Vertical, Qt.EditRole, 0, None),
        (Qt.Horizontal, Qt.DisplayRole, 0, 'A'),
        (Qt.Horizontal, Qt.DisplayRole, 1, None),   # run into IndexError
        (Qt.Vertical, Qt.DisplayRole, 0, 0),
        (Qt.Vertical, Qt.DisplayRole, 1, None),     # run into IndexError
    ]
)
def test_headerData(orientation, role, index, expectedHeader):
    model = DataFrameModel(pandas.DataFrame([0], columns=['A']))
    assert model.headerData(index, orientation, role) == expectedHeader

def test_flags():
    model = DataFrameModel(pandas.DataFrame([0], columns=['A']))
    index = model.index(0, 0)
    assert index.isValid()
    assert model.flags(index) == Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    model.setDataFrame(pandas.DataFrame([True], columns=['A']))
    index = model.index(0, 0)
    assert model.flags(index) != Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
    assert model.flags(index) == Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable

def test_rowCount():
    model = DataFrameModel(pandas.DataFrame([0], columns=['A']))
    assert model.rowCount() == 1
    model = DataFrameModel(pandas.DataFrame(numpy.arange(100), columns=['A']))
    assert model.rowCount() == 100

def test_columnCount():
    model = DataFrameModel(pandas.DataFrame([0], columns=['A']))
    assert model.columnCount() == 1

    model = DataFrameModel( pandas.DataFrame(numpy.arange(100).reshape(1, 100), columns=numpy.arange(100)) )
    assert model.columnCount() == 100

class TestSort(object):

    @pytest.fixture
    def dataFrame(self):
        return pandas.DataFrame(numpy.random.rand(10), columns=['A'])

    @pytest.fixture
    def model(self, dataFrame):
        return DataFrameModel(dataFrame)

    @pytest.mark.parametrize(
        "signal", 
        [
            "layoutAboutToBeChanged", 
            "layoutChanged",
            "sortingAboutToStart",
            "sortingFinished",
        ]
    )
    def test_signals(self, model, qtbot, signal):
        with qtbot.waitSignal(getattr(model, signal)) as blocker:
            model.sort(0)
        assert blocker.signal_triggered

    def test_returnValues(self, model):
        model.sort(0)

    @pytest.mark.parametrize(
        "testAscending, modelAscending, isIdentic", 
        [
            (True, Qt.AscendingOrder, True),
            (False, Qt.DescendingOrder, True),
            (True, Qt.DescendingOrder, False),
        ]
    )
    def test_sort(self, model, dataFrame, testAscending, modelAscending, isIdentic):
        temp = dataFrame.sort('A', ascending=testAscending)
        model.sort(0, order=modelAscending)
        assert (dataFrame['A'] == temp['A']).all() == isIdentic

class TestData(object):

    @pytest.fixture
    def dataFrame(self):
        return pandas.DataFrame(numpy.random.rand(10), columns=['A'])

    @pytest.fixture
    def model(self, dataFrame):
        return DataFrameModel(dataFrame)

    @pytest.fixture
    def index(self, model):
        index = model.index(0, 0)
        assert index.isValid()
        return index

    def test_invalidIndex(self, model):
        assert model.data(QtCore.QModelIndex()) is None

    def test_unknownRole(self, model, index):
        assert index.isValid()
        assert model.data(index, role="unknownRole") == None

    def test_unhandledDtype(self, model, index):
        dataFrame = pandas.DataFrame([92.289+151.96j], columns=['A'])
        dataFrame['A'] = dataFrame['A'].astype(numpy.complex64)
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()
        with pytest.raises(TypeError) as excinfo:
            assert model.data(index) == value
        assert "unhandled data type" in unicode(excinfo.value)

    @pytest.mark.parametrize(
        "value, dtype", [
            ("test", object),
            (u"äöü", object),
        ]
    )
    def test_strAndUnicode(self, model, index, value, dtype):
        dataFrame = pandas.DataFrame([value], columns=['A'])
        dataFrame['A'] = dataFrame['A'].astype(dtype)
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()
        assert model.data(index) == value
        assert model.data(index, role=Qt.DisplayRole) == value
        assert model.data(index, role=Qt.EditRole) == value
        assert model.data(index, role=Qt.CheckStateRole) == None
        assert isinstance(model.data(index, role=Qt.UserRole), dtype)

    @pytest.mark.parametrize(
        "value, dtype, precision", [
            (1, numpy.int8, None),
            (1, numpy.int16, None),
            (1, numpy.int32, None),
            (1, numpy.int64, None),
            (1, numpy.uint8, None),
            (1, numpy.uint16, None),
            (1, numpy.uint32, None),
            (1, numpy.uint64, None),
            (1.11111, numpy.float16, DataFrameModel._float_precisions[str('float16')]),
            (1.11111111, numpy.float32, DataFrameModel._float_precisions[str('float32')]),
            (1.1111111111111111, numpy.float64, DataFrameModel._float_precisions[str('float64')]),
            (1.11111111111111111111, numpy.float128, DataFrameModel._float_precisions[str('float128')]),
        ]
    )
    def test_numericalValues(self, model, index, value, dtype, precision):
        dataFrame = pandas.DataFrame([value], columns=['A'])
        dataFrame['A'] = dataFrame['A'].astype(dtype)
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()
        if precision:
            modelValue = model.data(index, role=Qt.DisplayRole)
            assert model.data(index) == round(value, precision)
            assert model.data(index, role=Qt.DisplayRole) == round(value, precision)
            assert model.data(index, role=Qt.EditRole) == round(value, precision)
        else:
            assert model.data(index) == value
            assert model.data(index, role=Qt.DisplayRole) == value
            assert model.data(index, role=Qt.EditRole) == value
        assert model.data(index, role=Qt.CheckStateRole) == None
        assert isinstance(model.data(index, role=Qt.UserRole), dtype)
        assert model.data(index, role=Qt.UserRole).dtype == dtype

    #@pytest.mark.parametrize(
        #"border1, modifier, border2, dtype", [
            #("min", -1, "max", numpy.uint8),
            #("max", +1, "min", numpy.uint8),
            #("min", -1, "max", numpy.uint16),
            #("max", +1, "min", numpy.uint16),
            #("min", -1, "max", numpy.uint32),
            #("max", +1, "min", numpy.uint32),
            #("min", -1, "max", numpy.uint64),
            ##("max", +1, "min", numpy.uint64),  # will raise OverFlowError caused by astype function, 
                                                ## uneffects models data method
            #("min", -1, "max", numpy.int8),
            #("max", +1, "min", numpy.int8),
            #("min", -1, "max", numpy.int16),
            #("max", +1, "min", numpy.int16),
            #("min", -1, "max", numpy.int32),
            #("max", +1, "min", numpy.int32),
            ##("min", -1, "max", numpy.int64),   # will raise OverFlowError caused by astype function
                                                ## uneffects models data method
            ##("max", +1, "min", numpy.int64),   # will raise OverFlowError caused by astype function
                                                ## uneffects models data method
        #]
    #)
    #def test_integerBorderValues(self, model, index, border1, modifier, border2, dtype):
        #ii = numpy.iinfo(dtype)
        #dataFrame = pandas.DataFrame([getattr(ii, border1) + modifier], columns=['A'])
        #dataFrame['A'] = dataFrame['A'].astype(dtype)
        #model.setDataFrame(dataFrame)
        #assert not model.dataFrame().empty
        #assert model.dataFrame() is dataFrame

        #assert index.isValid()
        #assert model.data(index) == getattr(ii, border2)

    @pytest.mark.parametrize(
        "value, qtbool", 
        [
            (True, Qt.Checked),
            (False, Qt.Unchecked)
        ]
    )
    def test_bool(self, model, index, value, qtbool):
        dataFrame = pandas.DataFrame([value], columns=['A'])
        dataFrame['A'] = dataFrame['A'].astype(numpy.bool_)
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()
        assert model.data(index, role=Qt.DisplayRole) == None
        assert model.data(index, role=Qt.EditRole) == value
        assert model.data(index, role=Qt.CheckStateRole) == qtbool
        assert model.data(index, role=Qt.UserRole) == value
        assert isinstance(model.data(index, role=Qt.UserRole), numpy.bool_)

    def test_date(self, model, index):
        numpyDate = numpy.datetime64("1990-10-08T10:15:45+0100")
        qDate = QtCore.QDateTime.fromString(str(numpyDate), Qt.ISODate)
        dataFrame = pandas.DataFrame([numpyDate], columns=['A'])
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()
        assert model.data(index, role=Qt.DisplayRole) == qDate
        assert model.data(index, role=Qt.EditRole) == qDate
        assert model.data(index, role=Qt.CheckStateRole) == None
        assert model.data(index, role=Qt.UserRole) == numpyDate
        assert isinstance(model.data(index, role=Qt.UserRole), pandas.lib.Timestamp)

class TestSetData(object):

    @pytest.fixture
    def dataFrame(self):
        return pandas.DataFrame([10], columns=['A'])

    @pytest.fixture
    def model(self, dataFrame):
        return DataFrameModel(dataFrame)

    @pytest.fixture
    def index(self, model):
        return model.index(0, 0)

    def test_invalidIndex(self, model):
        assert model.setData(QtCore.QModelIndex(), None) == False

    def test_nothingHasChanged(self, model, index):
        assert model.setData(index, 10) == False

    def test_unhandledDtype(self, model, index):
        dataFrame = pandas.DataFrame([92.289+151.96j], columns=['A'])
        dataFrame['A'] = dataFrame['A'].astype(numpy.complex64)
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()
        with pytest.raises(TypeError) as excinfo:
            model.setData(index, numpy.complex64(92+151j))
        assert "unhandled data type" in unicode(excinfo.value)

    @pytest.mark.parametrize(
        "value, dtype", [
            ("test", object),
            (u"äöü", object),
        ]
    )
    def test_strAndUnicode(self, model, index, value, dtype):
        dataFrame = pandas.DataFrame([value], columns=['A'])
        dataFrame['A'] = dataFrame['A'].astype(dtype)
        model.setDataFrame(dataFrame)
        newValue = u"{}123".format(value)
        assert model.setData(index, newValue)
        assert model.data(index) == newValue
        assert model.data(index, role=Qt.DisplayRole) == newValue
        assert model.data(index, role=Qt.EditRole) == newValue
        assert model.data(index, role=Qt.CheckStateRole) == None
        assert model.data(index, role=Qt.UserRole) == newValue
        assert isinstance(model.data(index, role=Qt.UserRole), dtype)

    @pytest.mark.parametrize(
        "value, qtbool", 
        [
            (True, Qt.Checked),
            (False, Qt.Unchecked)
        ]
    )
    def test_bool(self, model, index, value, qtbool):
        dataFrame = pandas.DataFrame([value], columns=['A'])
        dataFrame['A'] = dataFrame['A'].astype(numpy.bool_)
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()
        assert model.setData(index, qtbool)
        assert model.data(index, role=Qt.DisplayRole) == None
        assert model.data(index, role=Qt.EditRole) == value
        assert model.data(index, role=Qt.CheckStateRole) == qtbool
        assert model.data(index, role=Qt.UserRole) == value
        assert isinstance(model.data(index, role=Qt.UserRole), numpy.bool_)

    def test_date(self, model, index):
        numpyDate = numpy.datetime64("1990-10-08T10:15:45+0100")
        qDate = QtCore.QDateTime.fromString(str(numpyDate), Qt.ISODate)
        dataFrame = pandas.DataFrame([numpyDate], columns=['A'])
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()
        newDate = numpy.datetime64("2000-12-08T10:15:45+0100")
        newQDate = QtCore.QDateTime.fromString(str(newDate), Qt.ISODate)
        assert model.setData(index, newQDate)
        assert model.data(index, role=Qt.DisplayRole) == newQDate
        assert model.data(index, role=Qt.EditRole) == newQDate
        assert model.data(index, role=Qt.CheckStateRole) == None
        assert model.data(index, role=Qt.UserRole) == newDate
        assert isinstance(model.data(index, role=Qt.UserRole), pandas.lib.Timestamp)

    @pytest.mark.parametrize(
        "value, dtype, precision", [
            (1, numpy.int8, None),
            (1, numpy.int16, None),
            (1, numpy.int32, None),
            (1, numpy.int64, None),
            (1, numpy.uint8, None),
            (1, numpy.uint16, None),
            (1, numpy.uint32, None),
            (1, numpy.uint64, None),
            (1.11111, numpy.float16, DataFrameModel._float_precisions[str('float16')]),
            (1.11111111, numpy.float32, DataFrameModel._float_precisions[str('float32')]),
            (1.11111111111111111, numpy.float64, DataFrameModel._float_precisions[str('float64')]),
            (1.11111111111111111111, numpy.float128, DataFrameModel._float_precisions[str('float128')]),
        ]
    )
    def test_numericalValues(self, model, index, value, dtype, precision):
        dataFrame = pandas.DataFrame([value], columns=['A'])
        dataFrame['A'] = dataFrame['A'].astype(dtype)
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()

        newValue = value + 1
        assert model.setData(index, newValue)

        if precision:
            modelValue = model.data(index, role=Qt.DisplayRole)
            #assert abs(decimal.Decimal(str(modelValue)).as_tuple().exponent) == precision
            assert model.data(index) == round(newValue, precision)
            assert model.data(index, role=Qt.DisplayRole) == round(newValue, precision)
            assert model.data(index, role=Qt.EditRole) == round(newValue, precision)
        else:
            assert model.data(index) == newValue
            assert model.data(index, role=Qt.DisplayRole) == newValue
            assert model.data(index, role=Qt.EditRole) == newValue
        assert model.data(index, role=Qt.CheckStateRole) == None
        assert isinstance(model.data(index, role=Qt.UserRole), dtype)
        assert model.data(index, role=Qt.UserRole).dtype == dtype

    @pytest.mark.parametrize(
        "border, modifier, dtype", [
            ("min", -1, numpy.uint8),
            ("max", +1, numpy.uint8),
            ("min", -1, numpy.uint16),
            ("max", +1, numpy.uint16),
            ("min", -1, numpy.uint32),
            ("max", +1, numpy.uint32),
            ("min", -1, numpy.uint64),
            ("max", +1, numpy.uint64),
            ("min", -1, numpy.int8),
            ("max", +1, numpy.int8),
            ("min", -1, numpy.int16),
            ("max", +1, numpy.int16),
            ("min", -1, numpy.int32),
            ("max", +1, numpy.int32),
            ("min", -1, numpy.int64),
            ("max", +1, numpy.int64),
        ]
    )
    def test_integerBorderValues(self, model, index, border, modifier, dtype):
        ii = numpy.iinfo(dtype)
        value = getattr(ii, border) + modifier
        dataFrame = pandas.DataFrame([getattr(ii, border)], columns=['A'])
        dataFrame['A'] = dataFrame['A'].astype(dtype)
        model.setDataFrame(dataFrame)
        assert not model.dataFrame().empty
        assert model.dataFrame() is dataFrame

        assert index.isValid()
        assert model.setData(index, value)
        assert model.data(index) == getattr(ii, border)

if __name__ == '__main__':
    pytest.main()