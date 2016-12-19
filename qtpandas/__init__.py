# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from qtpandas.models.DataFrameModel import (DataFrameModel,
                                            read_file,
                                            read_sql)

from qtpandas.models.ColumnDtypeModel import ColumnDtypeModel

from qtpandas.models.DataSearch import DataSearch

from qtpandas.views.CSVDialogs import (CSVExportDialog,
                                       CSVImportDialog)

from qtpandas.views.EditDialogs import (AddAttributesDialog,
                                        RemoveAttributesDialog)

# __import__('pkg_resources').declare_namespace(__name__)

__version__ = '1.0.4'
