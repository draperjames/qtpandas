# coding = utf-8
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
import sys
from pandasqt.models.DataFrameModel import DataFrameModel
import pandas as pd
import pdb
from util import getCsvData, getRandomData

if __name__ == '__main__':

    data = {
        'A': [10, 11, 12],
        'B': [20.1, 21.2, 22.3],
        'C': ['Peter Pan', 'Cpt. Hook', 'Tinkerbell']
    }
    df = pd.DataFrame(data)
    df = getRandomData(100)
    #df = getCsvData()
    model = DataFrameModel()
    model.setDataFrame(df)
    #pdb.set_trace()

    app = QGuiApplication(sys.argv)
    view = QQuickView() 
    root_context = view.rootContext().setContextProperty('dataFrameModel', model)
    view.setSource(QUrl.fromLocalFile('BasicExample.qml'))
    view.show()
    sys.exit(app.exec_())