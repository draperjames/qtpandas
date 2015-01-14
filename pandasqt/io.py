# -*- coding: utf-8 -*-

import os
import pandas as pd
import pandasqt as pdqt
import numpy as np
import json
from hachoir_core.i18n import guessBytesCharset
from PyQt4.QtCore import QCoreApplication, QObject

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_rna

def dataframeFromCsv(path, delimiter, config, error_bad_lines=False):
    if os.path.exists(path):
        try:
            delimiter = delimiter
            encoding = guessBytesCharset(open(path, "r").read())

            dataFrame = pd.read_csv(
                path,
                delimiter=delimiter,
                encoding=encoding,
                error_bad_lines=error_bad_lines,
            )

            dataFrame = fillNoneValues(dataFrame)
            dataFrame = parseTimestamps(dataFrame)

            return dataFrame

        except pd.parser.CParserError:
            tempObject = QObject()
            raise IOError, "Wrong delimiter"
            return pd.DataFrame()
        except:
            raise
    else:
        return pd.DataFrame()

def fillNoneValues(dataFrame):
    for columnName in dataFrame.columns:
        column = dataFrame[columnName]
        if column.dtype == object:
            column.fillna("", inplace=True)
        #elif column.dtype in pdqt.DataFrameModel._intDtypes:
            #column.fillna(None, inplace=True)
        #elif dataFrame[column].dtype in pdqt.DataFrameModel._floatDtypes:
            #pass
        #elif dataFrame[column].dtype in pdqt.DataFrameModel._intDtypes:
            #pass
        #else:
            #pass
    return dataFrame

def parseTimestamps(dataFrame):
    # try to convert date columns automatically
    for columnName in dataFrame.columns:
        try:
            # try to convert the first row and a random row instead of the complete column, might be faster
            tempValue = np.datetime64(dataFrame[columnName][0])
            tempValue = np.datetime64(dataFrame[columnName][np.random.randint(len(dataFrame.index))])

            # just convert the rest if we can convert the sample rows
            tempColumn = dataFrame[columnName].astype(np.datetime64)
            dataFrame[columnName] = tempColumn
        except:
            pass
    return dataFrame

def saveFile(path, dataFrame, delimiter=";", encoding="utf-8", fileFormat="csv"):
    if fileFormat == "csv":
        dataFrame.to_csv(path, sep=delimiter, encoding=encoding, index=False)
        return True
    elif fileFormat == "fasta":
        if "dna" in dataFrame.columns and "dna_name" in dataFrame.columns:
            tempDf = pd.DataFrame()
            tempDf['dna'] = dataFrame['dna']
            tempDf['dna_name'] = dataFrame['dna_name']
            groups = tempDf.groupby(['dna', 'dna_name']).groups

            sequences = []
            for index in groups:
                dna = unicode(index[0]).replace('U', 'T')
                ids = u"biomap|{0}|".format(json.dumps(groups[index]).replace(' ', ''))
                if dna is not u"":
                    sequence = SeqRecord(
                        Seq(dna, generic_rna),
                        id=ids,
                        name="HokC",
                        description=unicode(index[1])
                    )
                    #sequence = SeqRecord(
                        #Seq("MKQHKAMIVALIVICITAVVAALVTRKDLCEVHIRTGQTEVAVF", generic_rna),
                        #id="YP_025292.1",
                        #name="HokC",
                        #description="toxic membrane protein"
                    #)
                    sequences.append(sequence)

            output_handle = open(path, "w")
            SeqIO.write(sequences, output_handle, "fasta")
            output_handle.close()
            del tempDf
    else:
        raise NotImplementedError, "unsupported file format"