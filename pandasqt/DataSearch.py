# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import parser
import re

import numpy as np
import pandas as pd

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

class DataSearch(object):
    """object which provides parsing functionality for set DataFrame"""

    def __init__(self, name, filterString, dataFrame=None):
        self._filterString = ''
        self._dataFrame = pd.DataFrame()

        self.name = name
        self.filterString = filterString
        if dataFrame:
            self.dataFrame = dataFrame

    def __repr__(self):
        string = u"DataSearch({}): {} ({})".format(hex(id(self)), self.name, self.filterString)
        string = string.encode("utf-8")
        return string

    def dataFrame(self):
        return self._dataFrame

    def setDataFrame(self, dataFrame):
        self._dataFrame = dataFrame

    def filterString(self):
        return self._filterString

    def setFilterString(self, filterString):
        ## remove leading whitespaces, they will raise an identation error
        filterString = filterString.strip()
        self._filterString = filterString

    def isValid(self):
        try:
            self.search()
            return True
        except:
            return False

    def search(self):
        # add dataFrames columns as local variables
        for column in self._dataFrame.columns:
            globals()[column] = self._dataFrame[column]
        globals()["freeSearch"] = self.freeSearch
        globals()["extentSearch"] = self.extentSearch

        parsedSearch = parser.expr(self.filterString).compile()
        searchIndex = eval(parsedSearch)
        return searchIndex

    def searchIndex(self):
        if self.isValid():
            return self.search()

    def searchIndexList(self):
        if self.isValid():
            searchIndex = self.search()
            return searchIndex[searchIndex == True].index

    def freeSearch(self, searchString):
        #print "doing a __freeSearch, looking for '{}'".format(searchString)
        #searchString = unicode(searchString)

        if not self._dataFrame.empty:
            question = self._dataFrame.index == -9999
            for column in self._dataFrame.columns:
                #print "search in column", column
                #if column != self.uidColumn:
                dfColumn = self._dataFrame[column]
                #print dfColumn, dfColumn.dtype

                #if self.table.dataFrame[column].dtype != object:
                dfColumn = dfColumn.apply(unicode)
                #print dfColumn, dfColumn.dtype

                question2 = dfColumn.str.contains(searchString, flags=re.IGNORECASE, regex=True, na=False)
                question = np.logical_or(question, question2)

            return question
        else:
            return []

    def extentSearch(self, xmin, ymin, xmax, ymax):
        if not self._dataFrame.empty:
            try:
                #print "extentSearch"
                questionMin = (self._dataFrame.lat >= xmin) & (self._dataFrame.lng >= ymin)
                questionMax = (self._dataFrame.lat <= xmax) & (self._dataFrame.lng <= ymax)
                return np.logical_and(questionMin, questionMax)
            except:
                raise

    #def applySearch(self):
        #filterCondition = self.search()
        #resultingIndexes = self.table.dataFrame[filterCondition].index
        #resultingIndexesString = str(list(resultingIndexes)).replace('[', '(').replace(']', ')')
        #subsetString = u'"index" IN {0}'.format(resultingIndexesString)
        ##print subsetString

        ### apply filter if we have an active sql model
        ##print self.table.sqlDataFrameModel
        #if self.table.sqlDataFrameModel:
            #self.table.sqlDataFrameModel.setFilter(subsetString)

        ### apply filter to qgis vector layer, even if this is empty
        #if list(resultingIndexes) == []:
            #subsetString = u'"index" >= 0'
        #else:
            #subsetString = u'"index" IN {0}'.format(resultingIndexesString)
        #self.table.pointLayer.setSubsetString(subsetString)
        ##print "set filter to point layer", self.table.pointLayer, self.table.pointLayer.featureCount()
        ##print self.table.pointLayer.subsetString()

        #return filterCondition