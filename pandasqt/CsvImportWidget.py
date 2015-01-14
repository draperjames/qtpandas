# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

import os

from ui.ui_CsvImportWidget import Ui_CsvImportWidget
import io
import pandasqt as pdqt
import pandas as pd

class CsvImportWidget(QtGui.QDialog, Ui_CsvImportWidget):

    def __init__(self, parent=None):
        super(CsvImportWidget, self).__init__(parent)
        self.setupUi(self)

        self._csvPath = ""
        self._dataFrame = pd.DataFrame()
        self._dataFrameModel = pdqt.DataFrameModel()

        self.toolButtonUpdate.clicked.connect(self.updateData)
        self.toolButtonImport.clicked.connect(self.importData)
        self.toolButtonOpen.clicked.connect(self.openFile)
        self.toolButtonCancel.clicked.connect(self.close)

        self.buttonGroup.buttonClicked.connect(self.setDelimiter)

    @property
    def _config(self):
        app = QtGui.QApplication.instance()
        if hasattr(app, 'config'):
            return app.config

    @property
    def csvPath(self):
        if os.path.exists(self._csvPath):
            return self._csvPath
    @csvPath.setter
    def csvPath(self, csvPath):
        if os.path.exists(csvPath):
            self._csvPath = csvPath

    @property
    def dataFrame(self):
        return self._dataFrame
    @dataFrame.setter
    def dataFrame(self, dataFrame):
        if dataFrame:
            self._dataFrame = dataFrame

    @property
    def dataFrameModel(self):
        return self._dataFrameModel
    @dataFrameModel.setter
    def dataFrameModel(self, dataFrameModel):
        if dataFrameModel:
            self._dataFrameModel = dataFrameModel

    def setDelimiter(self, button):
        if button.objectName() in ['checkBoxDelimiterComma', 'checkBoxDelimiterSemicolon']:
            self._config.set('import_delimiter', button.text())
        elif button.objectName() == 'checkBoxDelimiterCustom':
            delimiter, ok = QtGui.QInputDialog.getText(
                self, 
                self.tr("enter a delimiter"), 
                self.tr("delimiter:"), 
                QtGui.QLineEdit.Normal, 
                self.lineEditDelimiterCustom.text()
            )
            if ok and delimiter:
                self.lineEditDelimiterCustom.setText(delimiter)
                self._config.set('import_delimiter', delimiter)
        else:
            self._config.set('import_delimiter', ';')
        self.updateData()

    def getValues(self):
        return self.csvPath

    def importData(self):
        return self.accept()

    def openFile(self):
        self.csvPath = QtGui.QFileDialog.getOpenFileName(
            self,
            self.tr('open file'),
            self._config.get('scenarioDir'),
            self.tr("CSV Files (*.csv)")
        )
        if self.csvPath:
            self.lineEditFileName.setText(self.csvPath)
            self.updateData()
            return self.csvPath
        else:
            return None

    def updateData(self):
        if self.csvPath:
            dataFrame = io.dataframeFromCsv(
                self.csvPath, 
                self._config.get('import_delimiter', ';'),
                self._config,
                error_bad_lines=self.checkBoxSkipFaultyLines.isChecked(),
            )
            self.dataFrameModel = pdqt.DataFrameModel(dataFrame)
            self.tableViewData.setModel(self.dataFrameModel)

            self.tableViewColumns.setModel(self.dataFrameModel.columnDtypeModel())
            self.tableViewColumns.horizontalHeader().setDefaultSectionSize(200)
            self.tableViewColumns.setItemDelegateForColumn(1, pdqt.DtypeComboDelegate(self.tableViewColumns))