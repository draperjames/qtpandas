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
from pandasqt import DataFrameModel, setDelegatesFromDtype
from util import getCsvData, getRandomData

class TestWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(TestWidget, self).__init__(parent)
        self.resize(1680, 756)
        self.move(0, 0)

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
        self.buttonCsvData.clicked.connect(lambda: self.setDataFrame( getCsvData() ))
        self.buttonRandomData.clicked.connect(lambda: self.setDataFrame( getRandomData() ))

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

        self.chooseColumnComboBox.currentIndexChanged.connect(self.setModelColumn)

        self.dataListView.mouseReleaseEvent = self.mouseReleaseEvent

    def setDataFrame(self, dataFrame):
        self.df = dataFrame
        dataModel = DataFrameModel()
        dataModel.setDataFrame(self.df)
        self.dataListView.setModel(dataModel)
        self.dataTableView.setModel(dataModel)
        self.dataComboBox.setModel(dataModel)

        self.delegates = setDelegatesFromDtype(self.dataTableView)

        self.dataTableView.resizeColumnsToContents()

        # create a simple item model for our choosing combobox
        columnModel = QtGui.QStandardItemModel()
        for column in self.df.columns:
            columnModel.appendRow(QtGui.QStandardItem(column))
        self.chooseColumnComboBox.setModel(columnModel)

    def setModelColumn(self, index):
        self.dataListView.setModelColumn(index)
        self.dataComboBox.setModelColumn(index)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    widget = TestWidget()
    widget.show()

    widget.setDataFrame( getCsvData() )

    app.exec_()