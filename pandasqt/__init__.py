# -*- coding: utf-8 -*-
__import__('pkg_resources').declare_namespace(__name__)
__version__ = '0.1.1'

#__all__ = ["DataFrameModel", "CustomDelegates", "DtypeComboDelegate"]
from DataFrameModel import DataFrameModel
from ColumnDtypeModel import DtypeComboDelegate
from CustomDelegates import setDelegatesFromDtype, BigIntSpinboxDelegate, CustomDoubleSpinboxDelegate