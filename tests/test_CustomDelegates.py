# -*- coding: utf-8 -*-

from pandasqt.compat import Qt, QtCore, QtGui


import pytest
import pytestqt

import numpy
import pandas

from pandasqt.views.CustomDelegates import BigIntSpinboxDelegate, CustomDoubleSpinboxDelegate, TextDelegate, createDelegate
from pandasqt.models.DataFrameModel import DataFrameModel

class DemoTableView(QtGui.QTableView):

    def __init__(self, parent=None):
        super(DemoTableView, self).__init__(parent)
        self.resize(800, 600)
        self.move(0, 0)

class TestCustomDelegates(object):

    @pytest.fixture
    def emptyTableView(self, qtbot):
        widget = DemoTableView()
        qtbot.addWidget(widget)
        return widget

    @pytest.fixture
    def dataFrame(self):
        return pandas.DataFrame(['abc'], columns=['A'])

    @pytest.fixture
    def model(self, dataFrame):
        return DataFrameModel(dataFrame)

    @pytest.fixture
    def tableView(self, model, emptyTableView):
        emptyTableView.setModel(model)
        return emptyTableView

    @pytest.fixture
    def index(self, model):
        index = model.index(0, 0)
        assert index.isValid()
        return index

    @pytest.mark.parametrize(
        "widgetClass, model, exception, exceptionContains", [
            (QtGui.QWidget, None, AttributeError, "has no attribute 'model'"),
            (DemoTableView, None, ValueError, "no model set for the current view"),
            (DemoTableView, QtGui.QStandardItemModel(), TypeError, 'model is not of type DataFrameModel'),
        ]
    )
    def test_tableViewMissing(self, widgetClass, qtbot, model, exception, exceptionContains):
        widget = widgetClass()
        qtbot.addWidget(widget)
        with pytest.raises(exception) as excinfo:
            if model:
                widget.setModel(QtGui.QStandardItemModel())
            createDelegate('foo', 'bar', widget)
        assert exceptionContains in str(excinfo.value)

    @pytest.mark.parametrize(
        "value, singleStep", [
            (numpy.int8(1), 1),
            (numpy.int16(1), 1),
            (numpy.int32(1), 1),
            (numpy.int64(1), 1),
            (numpy.uint8(1), 1),
            (numpy.uint16(1), 1),
            (numpy.uint32(1), 1),
            (numpy.uint64(1), 1),
            (numpy.float16(1.11111), 0.1),
            (numpy.float32(1.11111111), 0.1),
            (numpy.float64(1.1111111111111111), 0.1),
            #(numpy.float128(1.11111111111111111111), 0.1),
        ]
    )
    def test_setDelegates(self, qtbot, tableView, index, value, singleStep):
        dlg = createDelegate(numpy.dtype(value), 0, tableView)
        assert dlg is not None

        data = pandas.DataFrame([value], columns=['A'])
        data['A'] = data['A'].astype(value.dtype)
        model = tableView.model()
        model.setDataFrame(data)
        for i, delegate in enumerate([dlg]):
            assert tableView.itemDelegateForColumn(i) == delegate

            option = QtGui.QStyleOptionViewItem()
            option.rect = QtCore.QRect(0, 0, 100, 100)
            editor = delegate.createEditor(tableView, option, index)
            delegate.setEditorData(editor, index)
            assert editor.value() == index.data()
            delegate.setModelData(editor, model, index)

            delegate.updateEditorGeometry(editor, option, index)

            dtype = value.dtype
            if dtype in DataFrameModel._intDtypes:
                info = numpy.iinfo(dtype)
                assert isinstance(delegate, BigIntSpinboxDelegate)
            elif dtype in DataFrameModel._floatDtypes:
                info = numpy.finfo(dtype)
                assert isinstance(delegate, CustomDoubleSpinboxDelegate)
                assert delegate.decimals == DataFrameModel._float_precisions[str(value.dtype)]
            assert delegate.maximum == info.max
            assert editor.maximum() == info.max
            assert delegate.minimum == info.min
            assert editor.minimum() == info.min
            assert delegate.singleStep == singleStep
            assert editor.singleStep() == singleStep


        def clickEvent(index):
            assert index.isValid()

        tableView.clicked.connect(clickEvent)
        with qtbot.waitSignal(tableView.clicked) as blocker:
            qtbot.mouseClick(tableView.viewport(), QtCore.Qt.LeftButton, pos=QtCore.QPoint(10, 10))
        assert blocker.signal_triggered

class TestTextDelegate(object):

    @pytest.fixture
    def dataFrame(self):
        data = [
            ['zero', 1, 2, 3, 4],
            ['five', 6, 7, 8, 9],
            ['ten', 11, 12, 13, 14]
        ]
        columns = ['Foo', 'Bar', 'Spam', 'Eggs', 'Baz']
        dataFrame = pandas.DataFrame(data, columns=columns)
        return dataFrame

    def test_editing(self, dataFrame, qtbot):
        model = DataFrameModel(dataFrame)

        tableView = QtGui.QTableView()

        qtbot.addWidget(tableView)
        tableView.setModel(model)

        delegate = TextDelegate(tableView)
        createDelegate(numpy.dtype('O'), 0, tableView)
        tableView.show()

        index = model.index(0, 0)
        preedit_data = index.data()

        assert not model.editable
        model.enableEditing(True)
        tableView.edit(index)
        editor = tableView.findChildren(QtGui.QLineEdit)[0]
        qtbot.keyPress(editor, QtCore.Qt.Key_F)
        qtbot.keyPress(editor, QtCore.Qt.Key_Enter)
        QtGui.QApplication.processEvents()
        with qtbot.waitSignal(timeout=100):
            assert index.data(QtCore.Qt.DisplayRole) == 'f'
