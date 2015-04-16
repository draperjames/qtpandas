import cPickle as pickle
from pandasqt.models.SupportedDtypes import SupportedDtypes

from qgisspaf.utils.compat import QtCore
import numpy as np

PandasColumnMimeType = "application/pandas-column"

class MimeData(QtCore.QMimeData):
    
    _mimeType = PandasColumnMimeType

    def __init__(self):
        """create a new MimeData object.
        
        """
        super(MimeData, self).__init__()
        
    def mimeType(self):
        """return mimeType
        
        Returns:
            str
        """
        return self._mimeType

    def setData(self, data):
        """Add some data.
        
        Args:
            data (object): Object to add as data. This object has to be pickable. 
                Qt objects don't work!
        
        Raises:
            TypeError if data is not pickable
        """
        try:
            bytestream = pickle.dumps(data)
            super(MimeData, self).setData(self._mimeType, bytestream)
        except TypeError:
            raise TypeError, self.tr("can not pickle added data")
        except:
            raise
        
    def data(self):
        """return stored data
        
        Returns:
            unpickled data
        """
        try:
            bytestream = super(MimeData, self).data(self._mimeType).data()
            return pickle.loads(bytestream)
        except:
            raise
        
class MimeDataPayload(object):
    
    def __init__(self):
        """
        
        """
        super(MimeDataPayload, self).__init__()
        
    def isValid(self):
        """Will be checked in the dragEnterEvent to check if our payload can be accepted.
           e.x. data is a filepath its valid if the file exists.
        
        Hint:
            Use this to implement your own dragable data.
            
        Returns:
            True if valid
            False if invalid
        """
        return False
    
    def processData(self, canvas):
        """Implement this to do what you want to do. e.x. add new data to canvas.
        Base implementation does nothing usefull.
        
        Args:
            canvas (QgsSpafCanvas): Canvas that recieved the drop event.

        """
        return True


class MimePayloadPandasColumn(MimeDataPayload):
    
    _allowedDtypes = SupportedDtypes.intTypes() + SupportedDtypes.uintTypes() + SupportedDtypes.floatTypes()

    def __init__(self, column, dtype):
        super(MimePayloadPandasColumn, self).__init__()
        self.column = column
        self.dtype = dtype
        
    def __repr__(self):
        return u"Column {0} of type {1}".format(self.column, self.dtype)
    
    def isValid(self):
        if self.dtype in self._allowedDtypes:
        #if self.dtype == np.int64 or self.dtype == np.float64:
            return True
        else:
            return False
        
    def processData(self, widget):
        print widget
        return True
        #if canvas.dataModel():
            #if isinstance(canvas.dataModel(), pdqt.models.DataFrameModel.DataFrameModel):
                #dataFrame = canvas.dataModel().dataFrame()
                #canvas.mapModel().addLayer(dataFrame.mapLayer("{0}".format(self.column)), visible=True)