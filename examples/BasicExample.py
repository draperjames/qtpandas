import sys

import numpy
import pandas

from qtpandas.excepthook import excepthook
<<<<<<< HEAD

sys.excepthook = excepthook
=======
>>>>>>> 225a08219f27df88419afd4a0ad5ed9786df1b4d

# Use QtGui from the compat module to take care if correct sip version, etc.
from qtpandas.compat import QtGui
from qtpandas.models.DataFrameModel import DataFrameModel
from qtpandas.views.DataTableView import DataTableWidget

sys.excepthook = excepthook

# Setup a new empty model
model = DataFrameModel()

# Setup an application and create a table view widget
app = QtGui.QApplication([])
widget = DataTableWidget()
widget.resize(800, 600)
widget.show()
# Asign the created model"""
widget.setViewModel(model)

# Create some test data
data = {
    'A': [10, 11, 12],
    'B': [20, 21, 22],
    'C': ['Peter Pan', 'Cpt. Hook', 'Tinkerbell']
}
df = pandas.DataFrame(data)
# Convert the column to the numpy.int8 datatype to test the delegates in the
# table int8 is limited to -128-127

df['A'] = df['A'].astype(numpy.int8)
df['B'] = df['B'].astype(numpy.float16)

# Fill the model with data
model.setDataFrame(df)

# start the app
app.exec_()
