# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from pandasqt.compat import QtCore, QtGui, Qt, Slot, Signal

import sys
import pandas
import numpy

from pandasqt import DataFrameModel, setDelegatesFromDtype, DtypeComboDelegate, DataSearch
from pandasqt.views.CSVDialogs import CSVImportDialog, CSVExportDialog
from pandasqt.views._ui import icons_rc
from pandasqt.views.DataTableView import DataTableWidget
from pandasqt.views.CustomDelegates import createDelegate
from util import getCsvData, getRandomData

class TestWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(TestWidget, self).__init__(parent)
        self.resize(1680, 756)
        self.move(0, 0)

        self.language = 'en'
        self.delegates = None

        self.df = pandas.DataFrame()

        #  init the data view's
        self.dataTableView = DataTableWidget(self)
        # self.dataTableView.setSortingEnabled(True)
        # self.dataTableView.setAlternatingRowColors(True)

        # self.dataListView = QtGui.QListView(self)
        # self.dataListView.setAlternatingRowColors(True)

        # self.dataComboBox = QtGui.QComboBox(self)

        # # make combobox to choose the model column for dataComboBox and dataListView
        # self.chooseColumnComboBox = QtGui.QComboBox(self)

        # self.buttonCsvData = QtGui.QPushButton("load csv data")
        # self.buttonRandomData = QtGui.QPushButton("load random data")
        # importDialog = CSVImportDialog(self)
        # importDialog.load.connect(self.updateModel)
        # self.buttonCsvData.clicked.connect(lambda: importDialog.show())
        # self.buttonRandomData.clicked.connect(lambda: self.setDataFrame( getRandomData(rows=100, columns=100) ))

        # self.exportDialog = CSVExportDialog(self)

        # self.buttonCSVExport = QtGui.QPushButton("export to csv")
        # self.buttonCSVExport.clicked.connect(self._exportModel)
        # self.buttonLayout = QtGui.QHBoxLayout()
        # self.buttonLayout.addWidget(self.buttonCsvData)
        # self.buttonLayout.addWidget(self.buttonCSVExport)
        # self.buttonLayout.addWidget(self.buttonRandomData)

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        # self.mainLayout.addLayout(self.buttonLayout)

        # self.toolBar = QtGui.QToolBar(self)
        # self.editAction = QtGui.QAction(QtGui.QIcon(':/icons/document-edit.png'), self.tr('Edit Data'), self.toolBar)

        # self.addColumnAction = QtGui.QAction(QtGui.QIcon(':/icons/edit-table-insert-column-right.png'), self.tr('Add Column'), self.toolBar)
        # self.removeColumnAction = QtGui.QAction(QtGui.QIcon(':/icons/edit-table-delete-column.png'), self.tr('Delete Column'), self.toolBar)
        # self.addRowAction = QtGui.QAction(QtGui.QIcon(':/icons/edit-table-insert-row-below.png'), self.tr('Add Row'), self.toolBar)
        # self.removeRowAction = QtGui.QAction(QtGui.QIcon(':/icons/edit-table-delete-row.png'), self.tr('Delete Row'), self.toolBar)

        # self.dataEditable = False
        # self.addColumnAction.setEnabled(self.dataEditable)
        # self.removeColumnAction.setEnabled(self.dataEditable)
        # self.addRowAction.setEnabled(self.dataEditable)
        # self.removeRowAction.setEnabled(self.dataEditable)

        # self.editAction.triggered.connect(self._toggleEditing)

        # self.toolBar.addAction(self.editAction)
        # self.toolBar.addAction(self.addColumnAction)
        # self.toolBar.addAction(self.removeColumnAction)
        # self.toolBar.addAction(self.addRowAction)
        # self.toolBar.addAction(self.removeRowAction)

        # self.mainLayout.addWidget(self.toolBar)

        self.mainLayout.addWidget(self.dataTableView)

        # self.spinbox = QtGui.QSpinBox()
        # self.mainLayout.addWidget(self.spinbox)
        # self.spinbox.setMaximum(99999999999)
        # self.spinbox.setValue(99999999999)

        # self.rightLayout = QtGui.QVBoxLayout()
        # self.chooseColumLayout = QtGui.QHBoxLayout()
        # self.mainLayout.addLayout(self.rightLayout)
        # self.rightLayout.addLayout(self.chooseColumLayout)
        # self.chooseColumLayout.addWidget(QtGui.QLabel("Choose column:"))
        # self.chooseColumLayout.addWidget(self.chooseColumnComboBox)
        # self.rightLayout.addWidget(self.dataListView)
        # self.rightLayout.addWidget(self.dataComboBox)

        self.tableViewColumnDtypes = QtGui.QTableView(self)
        self.mainLayout.addWidget(QtGui.QLabel('dtypes'))
        self.mainLayout.addWidget(self.tableViewColumnDtypes)
        # self.buttonGoToColumn = QtGui.QPushButton("go to column")
        # self.rightLayout.addWidget(self.buttonGoToColumn)
        # self.buttonGoToColumn.clicked.connect(self.goToColumn)

        # self.buttonSetFilter = QtGui.QPushButton("set filter")
        # self.rightLayout.addWidget(self.buttonSetFilter)
        # self.buttonSetFilter.clicked.connect(self.setFilter)
        # self.buttonClearFilter = QtGui.QPushButton("clear filter")
        # self.rightLayout.addWidget(self.buttonClearFilter)
        # self.buttonClearFilter.clicked.connect(self.clearFilter)
        # self.lineEditFilterCondition = QtGui.QLineEdit("freeSearch('am')")
        # self.rightLayout.addWidget(self.lineEditFilterCondition)

        # self.chooseColumnComboBox.currentIndexChanged.connect(self.setModelColumn)

        # self.dataListView.mouseReleaseEvent = self.mouseReleaseEvent

    @Slot('bool')
    def _toggleEditing(self):
        self.dataEditable = not self.dataEditable

        # maybe use a button to change the style to indicate the editing state
        self.addColumnAction.setEnabled(self.dataEditable)
        self.removeColumnAction.setEnabled(self.dataEditable)
        self.addRowAction.setEnabled(self.dataEditable)
        self.removeRowAction.setEnabled(self.dataEditable)


    @Slot()
    def _addColumn(self):
        pass


    @Slot()
    def _removeColumn(self):
        pass


    @Slot()
    def _addRow(self):
        pass


    @Slot()
    def _removeRow(self):
        pass




    def setDataFrame(self, dataFrame):
        self.df = dataFrame
        dataModel = DataFrameModel()
        dataModel.setDataFrame(self.df)
        self.dataTableView.setViewModel(dataModel)
        # self.dataTableView.setModel(dataModel)
        # self.dataComboBox.setModel(dataModel)

        # self.updateDelegates()

        # self.dataTableView.resizeColumnsToContents()

        # # create a simple item model for our choosing combobox
        # columnModel = QtGui.QStandardItemModel()
        # for column in self.df.columns:
        #     columnModel.appendRow(QtGui.QStandardItem(column))
        # self.chooseColumnComboBox.setModel(columnModel)

        self.tableViewColumnDtypes.setModel(dataModel.columnDtypeModel())
        self.tableViewColumnDtypes.horizontalHeader().setDefaultSectionSize(200)
        self.tableViewColumnDtypes.setItemDelegateForColumn(1, DtypeComboDelegate(self.tableViewColumnDtypes))
        dataModel.dtypeChanged.connect(self.updateDelegates)
        # dataModel.changingDtypeFailed.connect(self.changeColumnValue)

    @Slot()
    def _exportModel(self):
        model = self.dataTableView.model()
        self.exportDialog.setExportModel(model)
        self.exportDialog.show()

    @Slot('QAbstractItemModel')
    def updateModel(self, model):
        self.dataListView.setModel(model)
        self.dataTableView.setModel(model)
        self.dataComboBox.setModel(model)

        self.tableViewColumnDtypes.setModel(model.columnDtypeModel())

    def setModelColumn(self, index):
        self.dataListView.setModelColumn(index)
        self.dataComboBox.setModelColumn(index)

    @Slot(int, object)
    def updateDelegates(self, column, dtype):
        print "update delegate for column", column, dtype
        # as documented in the setDelegatesFromDtype function
        # we need to store all delegates, so going from
        # type A -> type B -> type A
        # would cause a segfault if not stored.
        view = self.dataTableView.tableView
        createDelegate(dtype, column, view)
        # dlg = self.delegates or {}
        # self.delegates = setDelegatesFromDtype(self.dataTableView.tableView, dlg)
        # print dlg

    def goToColumn(self):
        print "go to column 7"
        index = self.dataTableView.model().index(7, 0)
        self.dataTableView.setCurrentIndex(index)

    def changeColumnValue(self, columnName, index, dtype):
        print "failed to change", columnName, "to", dtype
        print index.data(), index.isValid()
        self.dataTableView.setCurrentIndex(index)

    def setFilter(self):
        #filterIndex = eval(self.lineEditFilterCondition.text())
        search = DataSearch("Test", self.lineEditFilterCondition.text())
        self.dataTableView.model().setFilter(search)
        #raise NotImplementedError

    def clearFilter(self):
        self.dataTableView.model().clearFilter()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    widget = TestWidget()
    widget.show()

    widget.setDataFrame( getCsvData() )

    #widget.setDataFrame( getRandomData(2, 2) )

    app.exec_()