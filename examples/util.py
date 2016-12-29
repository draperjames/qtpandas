# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import range
from future import standard_library
standard_library.install_aliases()
import os
import pandas
import numpy


def getCsvData():
    dtypes = {
        "int8_value": numpy.int8,
        "int16_value": numpy.int16,
        "int32_value": numpy.int32,
        # "int64_value": numpy.int64, # OverFlowError
        "uint8_value": numpy.uint8,
        "uint16_value": numpy.uint16,
        "uint32_value": numpy.uint32,
        # "uint64_value": numpy.uint64, # OverFlowError
        "float16_value": numpy.float16,
        "float32_value": numpy.float32,
        "float64_value": numpy.float64,
        # "float128_value": numpy.float128,
        "bool_value": numpy.bool_
    }
    delimiter = ","
    encoding = "utf-8"
    parse_dates = ["timestamp_value"]

    path = os.path.join(os.getcwdu(), "examples/testData/test1.csv")
    if not os.path.exists(path):
        path = os.path.join(os.getcwdu(), "testData/test1.csv")

    df = pandas.read_csv(
        path,
        dtype=dtypes,
        delimiter=delimiter,
        encoding=encoding,
        parse_dates=parse_dates
    )

    try:
        df["int64_value"] = df["int64_value"].astype(numpy.int64)
        df["uint64_value"] = df["uint64_value"].astype(numpy.uint64)
    except:
        raise

    return df

def getRandomData(rows=100, columns=20):
    columns = ["column {}".format(column) for column in range(columns)]
    data = {}
    for column in columns:
        data[column] = numpy.random.rand(rows)
    return pandas.DataFrame(data, columns=columns)
