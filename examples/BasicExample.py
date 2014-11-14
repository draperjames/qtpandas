"""set the sip version, cause pandas-qt uses version 2 by default"""
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui

import pandas
import pandasqt
import numpy

"""setup a new empty model"""
model = pandasqt.DataFrameModel()

"""setup an application and create a table view widget"""
app = QtGui.QApplication([])
widget = QtGui.QTableView()
widget.resize(800, 600)
widget.show()
"""asign the created model"""
widget.setModel(model)

"""create some test data"""
data = pandas.DataFrame([10], columns=['A'])
"""convert the column to the numpy.int8 datatype to test limitation in the table
int8 is limited to -128-127
"""
data['A'] = data['A'].astype(numpy.int8)
"""fill the model with data"""
model.setDataFrame(data)

"""assign new delegates, only useful for big int or float values"""
pandasqt.setDelegatesFromDtype(widget)

"""start the app"""
app.exec_()