import numpy as np
from pandasqt.compat import QtCore

class SupportedDtypesTranslator(QtCore.QObject):
    _instance = None
    def __init__(self, parent=None):
        super(SupportedDtypesTranslator, self).__init__(parent)

        self._strs = [(np.dtype(object), self.tr('text'))]

        self._ints = [(np.dtype(np.int8), self.tr('small integer (8 bit)')),
                      (np.dtype(np.int16), self.tr('small integer (16 bit)')),
                      (np.dtype(np.int32), self.tr('integer (32 bit)')),
                      (np.dtype(np.int64), self.tr('integer (64 bit)'))]

        self._uints = [(np.dtype(np.uint8), self.tr('unsigned small integer (8 bit)')),
                       (np.dtype(np.uint16), self.tr('unsigned small integer (16 bit)')),
                       (np.dtype(np.uint32), self.tr('unsigned integer (32 bit)')),
                       (np.dtype(np.uint64), self.tr('unsigned integer (64 bit)'))]

        self._floats = [(np.dtype(np.float16), self.tr('floating point number (16 bit)')),
                      (np.dtype(np.float32), self.tr('floating point number (32 bit)')),
                      (np.dtype(np.float64), self.tr('floating point number (64 bit)'))]

        self._datetime = [(np.dtype('<M8[ns]'), self.tr('date and time'))]

        self._bools = [(np.dtype(bool), self.tr('true/false value'))]

        self._all = self._strs + self._ints + self._uints + self._floats + self._bools + self._datetime

    def strTypes(self):
        return [dtype for (dtype, _) in self._strs]

    def intTypes(self):
        return [dtype for (dtype, _) in self._ints]

    def uintTypes(self):
        return [dtype for (dtype, _) in self._uints]

    def floatTypes(self):
        return [dtype for (dtype, _) in self._floats]

    def boolTypes(self):
        return [dtype for (dtype, _) in self._bools]

    def datetimeTypes(self):
        return [dtype for (dtype, _) in self._datetime]


    def description(self, value):
        value = np.dtype(value)
        for (dtype, string) in self._all:
            if dtype == value:
                return string

        # no match found return given value
        return value

    def dtype(self, value):
        for (dtype, string) in self._all:
            if string == value:
                return dtype

        return None

    def names(self):
        return [string for (_, string) in self._all]

    def tupleAt(self, index):
        try:
            return self._all[index]
        except IndexError, e:
            return ()


SupportedDtypes = SupportedDtypesTranslator()