# Utilities to use pandas (the data analysis / manipulation library for Python) with Qt.

I forked this library because I liked the great detail and effort datalyze-solutions put into this package.
I have converted some of this to Python 3+ so it will at least install, but more work is needed.
I think it would be fun to bring this package back to life and get some upgrades put into it.


To install:

pip install git+https://github.com/zbarge/QtPandas.git


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

There are many more features but I don't have documentation. Maybe I'll add it sometime.

