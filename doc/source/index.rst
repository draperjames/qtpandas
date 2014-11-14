.. pandas-qt documentation master file, created by
   sphinx-quickstart on Fri Nov 14 15:32:14 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=========
pandas-qt
=========

:Repository: `GitHub <https://github.com/datalyze-solutions/pandas-qt>`_
:Version: |version|
:License: `MIT <http://opensource.org/licenses/MIT>`_
:Author: Matthias Ludwig - Datalyze Solutions

Requirements
============

* Pandas 0.15.1 or later (might work with lower versions, but this is untested)
* Python 2.6 or later, including Python 3+.

    * Tested with pytest version 2.7.6 and pandas 0.15.1

* Works with either *PyQt* or *PySide*, picking one that is available giving preference to *PyQt* if both are installed.

Installation
============

Download the source from git ``git clone https://github.com/datalyze-solutions/pandas-qt`` or as zip.

Install it with ``python setup.py install``


Examples
========
You can find some examples in the *examples* folder of the source. Simply run them with ``python TestApp.py``.

A very simple example::  

    """set the sip version, cause pandas-qt uses version 2 by default"""
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtGui

    import pandas
    import pandasqt
    import numpy

    """setup a new empty model"""
    model = pandasqt.DataFrameModel()

    """setup an application and create a table view widget"""
    app = QtGui.QApplication([])
    widget = QtGui.QTableView()
    widget.resize(800, 600)
    widget.show()
    """asign the created model"""
    widget.setModel(model)

    """create some test data"""
    data = pandas.DataFrame([10], columns=['A'])
    """convert the column to the numpy.int8 datatype to test limitation in the table
    int8 is limited to -128-127
    """
    data['A'] = data['A'].astype(numpy.int8)
    """fill the model with data"""
    model.setDataFrame(data)

    """assign new delegates, only useful for big int or float values"""
    pandasqt.setDelegatesFromDtype(widget)

    """start the app"""
    app.exec_()

Modules
=======

.. toctree::
   :maxdepth: 2

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`