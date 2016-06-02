import pandas
import numpy
import sys
from pandasqt.excepthook import excepthook
sys.excepthook = excepthook

# use QtGui from the compat module to take care if correct sip version, etc.
from pandasqt.compat import QtWidgets
from pandasqt.models.DataFrameModel import DataFrameModel
from pandasqt.views.DataTableView import DataTableWidget
from pandasqt.views._ui import icons_rc

"""setup a new empty model"""
model = DataFrameModel()

"""setup an application and create a table view widget"""
app = QtWidgets.QApplication([])
widget = DataTableWidget()
widget.resize(800, 600)
widget.show()
"""asign the created model"""
widget.setViewModel(model)

"""create some test data"""
data = {
    'A': [10, 11, 12], 
    'B': [20, 21, 22], 
    'C': ['Peter Pan', 'Cpt. Hook', 'Tinkerbell']
}
df = pandas.DataFrame(data)
"""convert the column to the numpy.int8 datatype to test the delegates in the table
int8 is limited to -128-127
"""
df['A'] = df['A'].astype(numpy.int8)
df['B'] = df['B'].astype(numpy.float16)

"""fill the model with data"""
model.setDataFrame(df)

"""start the app"""
app.exec_()