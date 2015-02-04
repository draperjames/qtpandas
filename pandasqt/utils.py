from random import randint
from pandas import to_datetime
import numpy as np

def fillNoneValues(column):
    """Fill all NaN/NaT values of a column with an empty string

    Args:
        column (pandas.Series): A Series object with all rows.

    Returns:
        column: Series with filled NaN values.
    """
    if column.dtype == object:
        column.fillna('', inplace=True)
    return column

def convertTimestamps(column):
    """Convert a dtype of a given column to a datetime.

    This method tries to do this by brute force.

    Args:
        column (pandas.Series): A Series object with all rows.

    Returns:
        column: Converted to datetime if no errors occured, else the
            original column will be returned.

    """
    tempColumn = column
    try:
        # try to convert the first row and a random row instead of the complete column, might be faster
        tempValue = np.datetime64(column[0])
        tempValue = np.datetime64(column[randint(0, len(column.index) - 1)])
        tempColumn = column.apply(to_datetime)
    except:
        pass
    return tempColumn