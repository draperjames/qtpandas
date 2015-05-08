# -*- coding: utf-8 -*-
import sys

from pandasqt.excepthook import excepthook
sys.excepthook = excepthook

from pandasqt.compat import QtCore, QtGui, Qt, Slot, Signal

import pandas
import numpy

from pandasqt.models.DataFrameModel import DataFrameModel
from pandasqt.models.DataSearch import DataSearch
from pandasqt.views.CSVDialogs import CSVImportDialog, CSVExportDialog
from pandasqt.views._ui import icons_rc
from pandasqt.views.DataTableView import DataTableWidget
from pandasqt.views.CustomDelegates import DtypeComboDelegate
from pandasqt.models.mime import PandasCellMimeType, PandasCellPayload
from util import getCsvData, getRandomData

class DropLineEdit(QtGui.QLineEdit):
    
    def __init__(self, text, parent=None):
        super(DropLineEdit, self).__init__(text, parent)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        """recieve a drag event and check if we want to accept or reject

        Args:
            event (QDragEnterEvent)
        """
        if event.mimeData().hasFormat(PandasCellMimeType):
            if event.mimeData().data().isValid():
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        """process the dragged data

        Args:
            event (QDragEnterEvent)
        """
        super(DropLineEdit, self).dropEvent(event)
        mimeDataPayload = event.mimeData().data()
        self.setText(u"dropped column: {0}".format(mimeDataPayload.column))
        
class ComplexDropWidget(QtGui.QLineEdit):
    
    dropRecieved = Signal(QtCore.QMimeData)

    def __init__(self, parent=None):
        super(ComplexDropWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        """recieve a drag event and check if we want to accept or reject

        Args:
            event (QDragEnterEvent)
        """
        if event.mimeData().hasFormat(PandasCellMimeType):
            if event.mimeData().data().isValid():
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        """process the dragged data

        Args:
            event (QDragEnterEvent)
        """
        self.dropRecieved.emit(event.mimeData())
    
class TestWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(TestWidget, self).__init__(parent)
        self.resize(1680, 756)
        self.move(0, 0)

        self.df = pandas.DataFrame()
        self.dataModel = None

        #  init the data view's
        self.dataTableView = DataTableWidget(self)
        # self.dataTableView.setSortingEnabled(True)
        # self.dataTableView.setAlternatingRowColors(True)

        self.dataListView = QtGui.QListView(self)
        self.dataListView.setAlternatingRowColors(True)

        self.dataComboBox = QtGui.QComboBox(self)

        # make combobox to choose the model column for dataComboBox and dataListView
        self.chooseColumnComboBox = QtGui.QComboBox(self)

        self.buttonCsvData = QtGui.QPushButton("load csv data")
        self.buttonRandomData = QtGui.QPushButton("load random data")
        importDialog = CSVImportDialog(self)
        importDialog.load.connect(self.updateModel)
        self.buttonCsvData.clicked.connect(lambda: importDialog.show())
        self.buttonRandomData.clicked.connect(lambda: self.setDataFrame( getRandomData(rows=100, columns=100) ))

        self.exportDialog = CSVExportDialog(self)

        self.buttonCSVExport = QtGui.QPushButton("export to csv")
        self.buttonCSVExport.clicked.connect(self._exportModel)
        self.buttonLayout = QtGui.QHBoxLayout()
        self.buttonLayout.addWidget(self.buttonCsvData)
        self.buttonLayout.addWidget(self.buttonCSVExport)
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
        
        self.dropLineEdit = DropLineEdit("drop data from table here", self)
        self.rightLayout.addWidget(self.dropLineEdit)
        
        self.dropWidget = ComplexDropWidget(self)
        self.dropWidget.dropRecieved.connect(self.processDataDrops)
        self.rightLayout.addWidget(self.dropWidget)
        
    @Slot('QMimeData')
    def processDataDrops(self, mimeData):
        """if you have more complicated stuff to do and you want to match some models, might be possible like that"""
        mimeDataPayload = mimeData.data()
        if isinstance(mimeDataPayload, PandasCellPayload):
            if self.dataModel is not None:
                if hex(id(self.dataModel)) == mimeDataPayload.parentId:
                    self.dropWidget.setText("complex stuff done after drop event. {0}".format(mimeDataPayload.column))

    def setDataFrame(self, dataFrame):
        self.df = dataFrame
        dataModel = DataFrameModel()
        dataModel.setDataFrame(self.df)
        
        self.dataModel = dataModel

        self.dataListView.setModel(dataModel)
        self.dataTableView.setViewModel(dataModel)
        self.dataComboBox.setModel(dataModel)

        # self.dataTableView.resizeColumnsToContents()

        # create a simple item model for our choosing combobox
        columnModel = QtGui.QStandardItemModel()
        for column in self.df.columns:
            columnModel.appendRow(QtGui.QStandardItem(column))
        self.chooseColumnComboBox.setModel(columnModel)

        self.tableViewColumnDtypes.setModel(dataModel.columnDtypeModel())
        self.tableViewColumnDtypes.horizontalHeader().setDefaultSectionSize(200)
        self.tableViewColumnDtypes.setItemDelegateForColumn(1, DtypeComboDelegate(self.tableViewColumnDtypes))
        dataModel.changingDtypeFailed.connect(self.changeColumnValue)

    @Slot()
    def _exportModel(self):
        model = self.dataTableView.view().model()
        self.exportDialog.setExportModel(model)
        self.exportDialog.show()

    @Slot('QAbstractItemModel')
    def updateModel(self, model):
        self.dataModel = model
        self.dataListView.setModel(model)
        self.dataTableView.setViewModel(model)
        self.dataComboBox.setModel(model)

        self.tableViewColumnDtypes.setModel(model.columnDtypeModel())

    def setModelColumn(self, index):
        self.dataListView.setModelColumn(index)
        self.dataComboBox.setModelColumn(index)

    def goToColumn(self):
        print "go to column 7"
        index = self.dataTableView.view().model().index(7, 0)
        self.dataTableView.view().setCurrentIndex(index)

    def changeColumnValue(self, columnName, index, dtype):
        print "failed to change", columnName, "to", dtype
        print index.data(), index.isValid()
        self.dataTableView.view().setCurrentIndex(index)

    def setFilter(self):
        #filterIndex = eval(self.lineEditFilterCondition.text())
        search = DataSearch("Test", self.lineEditFilterCondition.text())
        self.dataTableView.view().model().setFilter(search)
        #raise NotImplementedError

    def clearFilter(self):
        self.dataTableView.view().model().clearFilter()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    widget = TestWidget()
    widget.show()

    widget.setDataFrame( getCsvData() )

    #widget.setDataFrame( getRandomData(2, 2) )

    app.exec_()