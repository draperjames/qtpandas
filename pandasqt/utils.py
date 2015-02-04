from random import randint
from pandas import Timestamp, to_datetime
import numpy as np

def fillNoneValues(column):
    if column.dtype == object:
        column.fillna('', inplace=True)
    return column

def convertTimestamps(column):
    tempColumn = column
    try:
        # try to convert the first row and a random row instead of the complete column, might be faster
        tempValue = np.datetime64(column[0])
        tempValue = np.datetime64(column[randint(0, len(column.index) - 1)])
        tempColumn = column.apply(to_datetime)
    except:
        pass
    return tempColumn