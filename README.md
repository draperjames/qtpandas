# QtPandas

### Utilities to use [pandas](https://github.com/pandas-dev/pandas)  (the data analysis/manipulation library for Python) with Qt.

## Project Information

<table>
    <tr>
        <td>Latest Release</td>
        <td><img src="https://img.shields.io/pypi/v/qtpandas.svg" alt="latest release" /></td>
    </tr>
    <tr>
        <td>Package Status</td>
        <td><img src="https://img.shields.io/pypi/status/qtpandas.svg" alt="status" /></td>
    </tr>
    <tr>
    <tr>
        <td>Build Status</td>
        <td>
            <a href="https://travis-ci.org/draperjames/qtpandas">
            <img src="https://travis-ci.org/draperjames/qtpandas.svg?branch=master" alt="travis build status" />
            </a>
        </td>
    </tr>
<!--     <tr> -->
  <td>PyPI</td>
  <td>
    <a href="https://pypi.python.org/pypi/qtpandas/">
    <img src="https://img.shields.io/pypi/dm/qtpandas.svg" alt="pypi downloads" />
    </a>
  </td>
</tr>
</table>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/795dad8f6dfd4697ab8474265c4d47cb)](https://www.codacy.com/app/james-draper/qtpandas?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=draperjames/qtpandas&amp;utm_campaign=Badge_Grade)
[![Join the chat at https://gitter.im/qtpandas/Lobby#](https://badges.gitter.im/qtpandas/lobby.svg)](https://gitter.im/qtpandas/Lobby#)
[![open issues](https://img.shields.io/github/issues-raw/draperjames/qtpandas.svg)](https://github.com/draperjames/qtpandas/issues)
[![closed issues](https://img.shields.io/github/issues-closed/draperjames/qtpandas.svg)](https://github.com/draperjames/qtpandas/issues)

## Requirements;
> Python 3.4 or greater    
> Pthon 2.7 or greater     
> PyQt4

## Install
To install run the following in the command prompt;
```
pip install qtpandas
```
If that doesn't work try installing the lastest version of easy gui;
```
pip install --upgrade git+https://github.com/robertlugg/easygui.git
```
If that doesn't work then please [report an issue](https://github.com/draperjames/qtpandas/issues)

To use, create a new Python script containing the following:
```
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qtpandas.views.CSVDialogs import CSVImportDialog

if __name__ == "__main__":
    from sys import argv, exit

    app = QApplication(argv)
    dialog = CSVImportDialog()
    dialog.show()
    app.exec_()
```
# Examples

These can be found in QtPandas/examples.

- BasicExmple.py

![basic](images/BasicExample_screen_shot.PNG)

- Here is TestApp.py

![testapp](images/TestApp_screen_shot.PNG)

# Development

## Wanna contribute?
Any feedback is apprecaited.
- Report an issue
- Check out the wiki for development info (coming soon!)
- Fork us.

Forked from @datalyze-solutions's [master](https://github.com/datalyze-solutions/pandas-qt).
