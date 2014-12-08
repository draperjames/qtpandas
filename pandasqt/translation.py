            #!/usr/bin/env python
# -*- coding: utf-8 -*-

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import os

from PyQt4 import QtCore
import numpy as np

class DTypeTranslator(object):

    def __init__(self, language='en'):
        super(DTypeTranslator, self).__init__()

        self._language = 'en'
        self.language = language

        self._dtypes = {
            np.dtype(object): {
                'python': 'object',
                'de': 'Text',
                'en': 'text'
            },

            # integers
            np.dtype(np.int8): {
                'python': 'int8',
                'de': 'kleine ganze Zahl (8 Bit)',
                'en': 'small integer (8 bit)'
            },
            np.dtype(np.int16): {
                'python': 'int16',
                'de': 'kleine ganze Zahl (16 Bit)',
                'en': 'small integer (16 bit)'
            },
            np.dtype(np.int32): {
                'python': 'int32',
                'de': 'ganze Zahl (32 Bit)',
                'en': 'integer (32 bit)'
            },
            np.dtype(np.int64): {
                'python': 'int64',
                'de': 'ganze Zahl (64 Bit)',
                'en': 'integer (64 bit)'
            },

            # unsigned integers
            np.dtype(np.uint8): {
                'python': 'uint8',
                'de': 'positive kleine ganze Zahl (8 Bit)',
                'en': 'unsigned small integer (8 bit)'
            },
            np.dtype(np.uint16): {
                'python': 'uint16',
                'de': 'positive kleine ganze Zahl (16 Bit)',
                'en': 'unsigned small integer (16 bit)'
            },
            np.dtype(np.uint32): {
                'python': 'uint32',
                'de': 'positive ganze Zahl (32 Bit)',
                'en': 'unsigned integer (32 bit)'
            },
            np.dtype(np.uint64): {
                'python': 'uint64',
                'de': 'positive ganze Zahl (64 Bit)',
                'en': 'unsigned integer (64 bit)'
            },

            # floating points
            np.dtype(np.float16): {
                'python': 'float16',
                'de': 'Gleitkommazahl (1 Stelle genau)',
                'en': 'floating point number (1 digit)'
            },
            np.dtype(np.float32): {
                'python': 'float32',
                'de': 'Gleitkommazahl (5 Stellen genau)',
                'en': 'floating point number (5 digits)'
            },
            np.dtype(np.float64): {
                'python': 'float64',
                'de': 'Gleitkommazahl (14 Stelle genau)',
                'en': 'floating point number (14 digits)'
            },
            np.dtype(np.float128): {
                'python': 'float128',
                'de': 'Gleitkommazahl (17 Stelle genau)',
                'en': 'floating point number (17 digits)'
            },

            # datetimes
            # np.datetime64
            #np.dtype('<M8'): {
            #np.dtype(np.datetime64): {
                #'python': 'datetime64',
                #'de': 'Datum mit Zeit',
                #'en': 'date and time'
            #},
            # np.datetime64 inside pandas dataframe
            np.dtype('<M8[ns]'): {
                'python': 'datetime64',
                'de': 'Datum mit Zeit',
                'en': 'date and time'
            },

            # bools
            np.dtype(bool): {
                'python': 'bool',
                'de': 'Ja/Nein Wert', #'Boolescher Wert',
                'en': 'true/false value', #'boolean'
            },
        }

    def tr(self, dtype):
        dtype = np.dtype(dtype)
        if dtype in self._dtypes.keys():
            dtypeTranslation = self._dtypes[dtype]
            if self.language not in dtypeTranslation.keys():
                self.language = 'python'
            return dtypeTranslation[self.language]
        else:
            return dtype

    def lookup(self, translation):
        """convert a translation back to a data type

        Returns:
            dtype, language if found
            None, None if not found
        """
        for dtype in self._dtypes.keys():
            for language in self._dtypes[dtype].keys():
                if translation == self._dtypes[dtype][language]:
                    return dtype, language
                    break
        return None, None

    @property
    def language(self):
        return self._language
    @language.setter
    def language(self, language):
        if language in ['python', 'en', 'de']:
            self._language = language
        else:
            self._language = 'en'

    def translationTuple(self):
        translations = []
        for dtype in self._dtypes.keys():
            translations.append(self.tr(dtype))
        return tuple(translations)