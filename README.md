# QtPandas

### Utilities to use pandas (the data analysis/manipulation library for Python) with Qt.

## Project Information

[![Join the chat at https://gitter.im/qtpandas/Lobby#](https://badges.gitter.im/qtpandas/lobby.svg)](https://gitter.im/qtpandas/Lobby#)

## Build Status

[![Travis status](https://travis-ci.org/draperjames/QtPandas.svg?branch=master)](https://travis-ci.org/draperjames/QtPandas)

Requirements;
> Python 3.x    
> Pandas 20.0   
> PyQt 4.7.8

To install run the following in the command prompt;
```
pip install qtpandas
pip install --upgrade git+https://github.com/robertlugg/easygui.git
```

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

Join us on [gitter](https://gitter.im/qtpandas/Lobby#)

Forked from @datalyze-solutions's [master](https://github.com/datalyze-solutions/qtpandas).
