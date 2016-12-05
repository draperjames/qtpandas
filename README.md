# QtPandas

### Utilities to use pandas (the data analysis/manipulation library for Python) with Qt.

Requirements;
> Python 3.x    
> Pandas 20.0   
> PyQt 4.7.8

To install run the following in the command prompt;
```
pip install git+https://github.com/drapja/QtPandas.git
pip install --upgrade git+https://github.com/robertlugg/easygui.git
```

To use, create a new Python script containing the following:
```
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pandasqt.views.CSVDialogs import CSVImportDialog

if __name__ == "__main__":
    from sys import argv, exit

    app = QApplication(argv)
    dialog = CSVImportDialog()
    dialog.show()
    app.exec_()
```
Several examples can also be found in the exmples directory.

## TO DO:
- [ ] Add documentation.
- [ ] Add screen shots
- [ ] Create Wiki
- [ ] Make verison agnostic.
- [ ] Create specific Python version tests.
- [ ] Add Windows, Apple, and Linux tests.
- [ ] Consider adding functions seen in [Spyder IDE's dataframeeditor](https://github.com/spyder-ide/spyder/blob/f2b36f00f873cf4080087bfb529e6256b3e24792/spyder/widgets/variableexplorer/dataframeeditor.py)
    - [ ] Sort
    - [ ] Color coding
Forked from @zbarge's fork of @datalyze-solutions's [master](https://github.com/datalyze-solutions/pandas-qt).
