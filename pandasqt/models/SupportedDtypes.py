import numpy as np
from pandasqt.compat import QtCore

class SupportedDtypesTranslator(QtCore.QObject):
    _instance = None
    def __init__(self, parent=None):
        super(SupportedDtypesTranslator, self).__init__(parent)

        self._ints = [(np.int8, self.tr('small integer (8 bit)')),
                      (np.int16, self.tr('small integer (16 bit)')),
                      (np.int32, self.tr('integer (32 bit)')),
                      (np.int64, self.tr('integer (64 bit)'))]

        self._uints = [(np.uint8, self.tr('unsigned small integer (8 bit)')),
                       (np.uint16, self.tr('unsigned small integer (16 bit)')),
                       (np.uint32, self.tr('unsigned integer (32 bit)')),
                       (np.uint64, self.tr('unsigned integer (64 bit)'))]

        self._floats = [(np.float16, self.tr('floating point number (1 digit)')),
                      (np.float32, self.tr('floating point number (5 digits)')),
                      (np.float64, self.tr('floating point number (14 digits)'))]

        self._datetime = [(np.dtype('<M8[ns]'), self.tr('date and time'))]

        self._bools = [(np.dtype(bool), self.tr('true/false value'))]

        self._all = self._ints + self._uints + self._floats + self._bools

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

SupportedDtypes = SupportedDtypesTranslator()