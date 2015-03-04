from pandasqt.compat import QtCore, QtGui, Qt
from pandasqt.views._ui import AddAttrDialog
from pandasqt.translation import DTypeTranslator


class AddAttributesDialog(QtGui.QDialog, AddAttrDialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(AddAttrDialog, self).__init__(parent)
        self.setupUi(self)