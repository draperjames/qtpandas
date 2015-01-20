# -*- coding: utf-8 -*-

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

import sys
import pandas
from pandasqt import DataFrameModel, setDelegatesFromDtype, DtypeComboDelegate, DataSearch
from pandasqt.csvwidget import CSVImportDialog
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
        self.dataTableView = QtGui.QTableView(self)
        self.dataTableView.setSortingEnabled(True)
        self.dataTableView.setAlternatingRowColors(True)

        self.dataListView = QtGui.QListView(self)
        self.dataListView.setAlternatingRowColors(True)

        self.dataComboBox = QtGui.QComboBox(self)

        # make combobox to choose the model column for dataComboBox and dataListView
        self.chooseColumnComboBox = QtGui.QComboBox(self)

        self.buttonCsvData = QtGui.QPushButton("load csv data")
        self.buttonRandomData = QtGui.QPushButton("load random data")
        importDialog = CSVImportDialog()
        importDialog.load.connect(self.updateModel)
        self.buttonCsvData.clicked.connect(lambda: importDialog.show())
        self.buttonRandomData.clicked.connect(lambda: self.setDataFrame( getRandomData(rows=100, columns=100) ))

        self.buttonLayout = QtGui.QHBoxLayout()
        self.buttonLayout.addWidget(self.buttonCsvData)
        self.buttonLayout.addWidget(self.buttonRandomData)

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addWidget(self.dataTableView)

        self.spinbox = QtGui.QSpinBox()
        self.mainLayout.addWidget(self.spinbox)
        self.spinbox.setMaximum(99999999999)
        self.spinbox.setValue(99999999999)

        self.rightLayout = QtGui.QVBoxLayout()
        self.chooseColumLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.rightLayout)
        self.rightLayout.addLayout(self.chooseColumLayout)
        self.chooseColumLayout.addWidget(QtGui.QLabel("Choose column:"))
        self.chooseColumLayout.addWidget(self.chooseColumnComboBox)
        self.rightLayout.addWidget(self.dataListView)
        self.rightLayout.addWidget(self.dataComboBox)

        self.tableViewColumnDtypes = QtGui.QTableView(self)
        self.rightLayout.addWidget(QtGui.QLabel('dtypes'))
        self.rightLayout.addWidget(self.tableViewColumnDtypes)
        self.buttonGoToColumn = QtGui.QPushButton("go to column")
        self.rightLayout.addWidget(self.buttonGoToColumn)
        self.buttonGoToColumn.clicked.connect(self.goToColumn)

        self.buttonSetFilter = QtGui.QPushButton("set filter")
        self.rightLayout.addWidget(self.buttonSetFilter)
        self.buttonSetFilter.clicked.connect(self.setFilter)
        self.buttonClearFilter = QtGui.QPushButton("clear filter")
        self.rightLayout.addWidget(self.buttonClearFilter)
        self.buttonClearFilter.clicked.connect(self.clearFilter)
        self.lineEditFilterCondition = QtGui.QLineEdit("freeSearch('am')")
        self.rightLayout.addWidget(self.lineEditFilterCondition)

        self.chooseColumnComboBox.currentIndexChanged.connect(self.setModelColumn)

        self.dataListView.mouseReleaseEvent = self.mouseReleaseEvent

    def setDataFrame(self, dataFrame):
        self.df = dataFrame
        dataModel = DataFrameModel()
        dataModel.setDataFrame(self.df)
        self.dataListView.setModel(dataModel)
        self.dataTableView.setModel(dataModel)
        self.dataComboBox.setModel(dataModel)

        self.updateDelegates()

        self.dataTableView.resizeColumnsToContents()

        # create a simple item model for our choosing combobox
        columnModel = QtGui.QStandardItemModel()
        for column in self.df.columns:
            columnModel.appendRow(QtGui.QStandardItem(column))
        self.chooseColumnComboBox.setModel(columnModel)

        self.tableViewColumnDtypes.setModel(dataModel.columnDtypeModel())
        self.tableViewColumnDtypes.horizontalHeader().setDefaultSectionSize(200)
        self.tableViewColumnDtypes.setItemDelegateForColumn(1, DtypeComboDelegate(self.tableViewColumnDtypes))
        dataModel.dtypeChanged.connect(self.updateDelegates)
        dataModel.changingDtypeFailed.connect(self.changeColumnValue)

    @QtCore.pyqtSlot('QAbstractItemModel')
    def updateModel(self, model):
        self.dataListView.setModel(model)
        self.dataTableView.setModel(model)
        self.dataComboBox.setModel(model)

        self.tableViewColumnDtypes.setModel(model.columnDtypeModel())

    def setModelColumn(self, index):
        self.dataListView.setModelColumn(index)
        self.dataComboBox.setModelColumn(index)

    def updateDelegates(self, column=None):
        print "update delegate for column", column
        self.delegates = setDelegatesFromDtype(self.dataTableView)

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