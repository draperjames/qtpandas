# -*- coding: utf-8 -*-
import os
# import numpy
import pytest
# import pytestqt
import tempfile

from qtpandas.compat import QtCore, QtGui  # ,Qt

from qtpandas.views.CSVDialogs import (
    DelimiterValidator, DelimiterSelectionWidget,
    CSVImportDialog, CSVExportDialog
)

from qtpandas.models.DataFrameModel import DataFrameModel

FIXTUREDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'fixtures')


@pytest.fixture()
def csv_file():
    return os.path.join(FIXTUREDIR, 'csv_file.csv')


@pytest.fixture()
def tmp(request):
    handle, name = tempfile.mkstemp(suffix='.csv')

    def _teardown():
        os.close(handle)
        os.remove(name)
    request.addfinalizer(_teardown)
    return name


class TestValidator(object):

    @pytest.fixture()
    @classmethod
    def test_input(cls, qtbot):
        widget = QtGui.QLineEdit()
        widget.setValidator(DelimiterValidator())
        qtbot.addWidget(widget)
        widget.show()

        qtbot.keyPress(widget, ' ')
        assert widget.text() == ''
        qtbot.keyPress(widget, 'a')
        assert widget.text() == 'a'


class TestDelimiterBox(object):
    @pytest.fixture()
    @classmethod
    def test_selections_and_signals(cls, qtbot):
        box = DelimiterSelectionWidget()
        qtbot.addWidget(box)
        box.show()

        buttons = box.findChildren(QtGui.QRadioButton)
        lineedit = box.findChildren(QtGui.QLineEdit)[0]

        delimiters = []
        for button in buttons:
            with qtbot.waitSignal(box.delimiter, 1000):
                qtbot.mouseClick(button, QtCore.Qt.LeftButton)
                if lineedit.isEnabled():
                    qtbot.keyPress(lineedit, 'a')
                delimiters.append(box.currentSelected())

        assert len(delimiters) == 4

        for char in [',', ';', '\t', 'a']:
            assert char in delimiters

    @pytest.fixture()
    @classmethod
    def test_reset(cls, qtbot):
        box = DelimiterSelectionWidget()
        qtbot.addWidget(box)
        box.show()

        buttons = box.findChildren(QtGui.QRadioButton)
        lineedit = box.findChildren(QtGui.QLineEdit)[0]

        delimiters = []
        for button in buttons:
            with qtbot.waitSignal(box.delimiter, 1000):
                qtbot.mouseClick(button, QtCore.Qt.LeftButton)
                if lineedit.isEnabled():
                    qtbot.keyPress(lineedit, 'a')
                delimiters.append(box.currentSelected())

        box.reset()
        assert not lineedit.isEnabled()


class TestCSVImportWidget(object):

    @pytest.fixture()
    @classmethod
    def test_init(cls, qtbot):
        csvwidget = CSVImportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()
        assert csvwidget.isModal()
        assert csvwidget.windowTitle() == 'Import CSV'

    @pytest.fixture()
    @classmethod
    def test_fileinput(cls, qtbot, csv_file):
        csvwidget = CSVImportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()
        labels = csvwidget.findChildren(QtGui.QLabel)
        assert labels[0].text() == 'Choose File'
        lineedits = csvwidget.findChildren(QtGui.QLineEdit)
        qtbot.keyClicks(lineedits[0], csv_file)
        assert csvwidget._previewTableView.model() is not None
        assert csvwidget._delimiter == ';'
        assert csvwidget._header is None

    @pytest.fixture()
    @classmethod
    def test_header(cls, qtbot):
        csvwidget = CSVImportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()

        assert csvwidget._header == None
        checkboxes = csvwidget.findChildren(QtGui.QCheckBox)
        checkboxes[0].toggle()
        assert csvwidget._header == 0

    @classmethod
    def test_encoding(cls, qtbot):
        csvwidget = CSVImportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()

        comboboxes = csvwidget.findChildren(QtGui.QComboBox)
        # comboboxes[0]
        assert comboboxes[0].itemText(comboboxes[0].currentIndex()) == 'ASCII'
        qtbot.mouseClick(comboboxes[0], QtCore.Qt.LeftButton)
        qtbot.keyPress(comboboxes[0], QtCore.Qt.Key_Down)
        assert csvwidget._encodingKey != 'iso_ir_6'

    @pytest.fixture()
    @classmethod
    def test_delimiter(cls, qtbot):
        csvwidget = CSVImportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()

        groupboxes = csvwidget.findChildren(QtGui.QGroupBox)
        radiobuttons = groupboxes[0].findChildren(QtGui.QRadioButton)
        lineedits = groupboxes[0].findChildren(QtGui.QLineEdit)

        for button in radiobuttons:
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)
            if lineedits[0].isEnabled():
                qtbot.keyPress(lineedits[0], ' ')
                assert lineedits[0].text() == ''
                qtbot.keyPress(lineedits[0], 'a')
                assert lineedits[0].text() == 'a'
            assert csvwidget._delimiter == groupboxes[0].currentSelected()

    @pytest.fixture()
    @classmethod
    def test_accept_reject(cls, qtbot):
        csvwidget = CSVImportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()

        buttons = csvwidget.findChildren(QtGui.QPushButton)
        for button in buttons:
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)
            if not csvwidget.isVisible():
                csvwidget.show()

    @classmethod
    def test_preview(cls, qtbot, csv_file):
        csvwidget = CSVImportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()
        # labels = csvwidget.findChildren(QtGui.QLabel)
        lineedits = csvwidget.findChildren(QtGui.QLineEdit)
        qtbot.keyClicks(lineedits[0], csv_file)

        groupboxes = csvwidget.findChildren(QtGui.QGroupBox)
        radiobuttons = groupboxes[0].findChildren(QtGui.QRadioButton)
        lineedits = groupboxes[0].findChildren(QtGui.QLineEdit)

        for button in radiobuttons:
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)
            if lineedits[0].isEnabled():
                qtbot.keyPress(lineedits[0], ';')

        assert csvwidget._previewTableView.model() is not None

        def _assert(x, path):
            assert x
            assert isinstance(x, DataFrameModel)
            assert path
            assert isinstance(path, str)

        csvwidget.load.connect(_assert)
        with qtbot.waitSignal(csvwidget.load):
            csvwidget.accepted()


class TestCSVExportWidget(object):

    def test_init(self, qtbot):
        csvwidget = CSVExportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()
        assert csvwidget.isModal()
        assert csvwidget.windowTitle() == 'Export to CSV'

    @classmethod
    def test_fileoutput(cls, qtbot, csv_file):
        csvwidget = CSVExportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()
        labels = csvwidget.findChildren(QtGui.QLabel)
        assert labels[0].text() == 'Output File'
        lineedits = csvwidget.findChildren(QtGui.QLineEdit)
        qtbot.keyClicks(lineedits[0], csv_file)
        assert csvwidget._filenameLineEdit.text() == csv_file

    def test_header(self, qtbot):
        csvwidget = CSVExportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()

        checkboxes = csvwidget.findChildren(QtGui.QCheckBox)
        checkboxes[0].toggle()
        assert csvwidget._headerCheckBox.isChecked()

    def test_encoding(self, qtbot):
        csvwidget = CSVExportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()

        comboboxes = csvwidget.findChildren(QtGui.QComboBox)
        # comboboxes[0]
        assert comboboxes[0].itemText(comboboxes[0].currentIndex()) == 'UTF_8'

    def test_delimiter(self, qtbot):
        csvwidget = CSVExportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()

        groupboxes = csvwidget.findChildren(QtGui.QGroupBox)
        radiobuttons = groupboxes[0].findChildren(QtGui.QRadioButton)
        lineedits = groupboxes[0].findChildren(QtGui.QLineEdit)

        delimiter = None
        for button in radiobuttons:
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)
            if lineedits[0].isEnabled():
                qtbot.keyPress(lineedits[0], ' ')
                assert lineedits[0].text() == ''
                qtbot.keyPress(lineedits[0], 'a')
                assert lineedits[0].text() == 'a'

            assert delimiter != groupboxes[0].currentSelected()
            delimiter = groupboxes[0].currentSelected()

    def test_accept_reject(self, qtbot):
        csvwidget = CSVExportDialog()
        qtbot.addWidget(csvwidget)
        csvwidget.show()

        buttons = csvwidget.findChildren(QtGui.QPushButton)
        for button in buttons:
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)
            if button.text() == 'Export Data':
                assert csvwidget.isVisible() is True
            else:
                assert csvwidget.isVisible() is False


class TestDateTimeConversion(object):

    @classmethod
    def test_read_write(cls, qtbot, csv_file, tmp):
        importWidget = CSVImportDialog()

        qtbot.addWidget(importWidget)
        importWidget.show()

        import_lineedits = importWidget.findChildren(QtGui.QLineEdit)
        qtbot.keyClicks(import_lineedits[0], csv_file)

        groupboxes = importWidget.findChildren(QtGui.QGroupBox)
        radiobuttons = groupboxes[0].findChildren(QtGui.QRadioButton)

        for button in radiobuttons:
            if button.text() == 'Semicolon':
                qtbot.mouseClick(button, QtCore.Qt.LeftButton)
                break

        checkboxes = importWidget.findChildren(QtGui.QCheckBox)
        checkboxes[0].toggle()

        model_in = importWidget._previewTableView.model()

        # convert critical datetime column:
        column_model = model_in.columnDtypeModel()
        index = column_model.index(4, 1)
        column_model.setData(index, 'date and time')

        ##
        # now we export the data and load it again
        ##
        exportWidget = CSVExportDialog(model_in)

        qtbot.addWidget(exportWidget)
        exportWidget.show()

        lineedits = exportWidget.findChildren(QtGui.QLineEdit)
        qtbot.keyClicks(lineedits[0], tmp)

        groupboxes = exportWidget.findChildren(QtGui.QGroupBox)
        radiobuttons = groupboxes[0].findChildren(QtGui.QRadioButton)

        for button in radiobuttons:
            if button.text() == 'Semicolon':
                qtbot.mouseClick(button, QtCore.Qt.LeftButton)
                break

        checkboxes = exportWidget.findChildren(QtGui.QCheckBox)
        checkboxes[0].toggle()

        buttons = exportWidget.findChildren(QtGui.QPushButton)

        with qtbot.waitSignal(exportWidget.exported, timeout=3000):
            for button in buttons:
                if button.text() == 'Export Data':
                    qtbot.mouseClick(button, QtCore.Qt.LeftButton)
                    break

        import_lineedits[0].clear()
        qtbot.keyClicks(import_lineedits[0], tmp)
        buttons = importWidget.findChildren(QtGui.QPushButton)
        with qtbot.waitSignal(importWidget.load, timeout=3000):
            for button in buttons:
                if button.text() == 'Load Data':
                    model_out_in = importWidget._previewTableView.model()
                    qtbot.mouseClick(button, QtCore.Qt.LeftButton)
                    break

        column_model = model_out_in.columnDtypeModel()
        index = column_model.index(4, 1)
        column_model.setData(index, 'date and time')

        comparator = model_in.dataFrame() == model_out_in.dataFrame()
        assert all(comparator)

        # df = model_out_in.dataFrame()
