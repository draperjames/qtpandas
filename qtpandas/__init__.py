# -*- coding: utf-8 -*-
# __import__('pkg_resources').declare_namespace(__name__)
__version__ = '1.0.3'
from qtpandas.models.DataFrameModel import DataFrameModel, read_file, read_sql
from qtpandas.models.ColumnDtypeModel import ColumnDtypeModel
from qtpandas.models.DataSearch import DataSearch
from qtpandas.views.CSVDialogs import CSVExportDialog, CSVImportDialog
from qtpandas.views.EditDialogs import AddAttributesDialog, RemoveAttributesDialog
