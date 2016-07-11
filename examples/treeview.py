# coding = utf-8
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterUncreatableType
from PyQt5.QtWidgets import QFileSystemModel, QApplication, QFileSystemModel, QTreeView
import sys
import pdb

class FileSystemModel(QFileSystemModel):

    def __init__(self, parent=None):
        super(FileSystemModel, self).__init__(parent)

    def roleNames(self):
        roles = {
            Qt.UserRole + 4: b"SizeRole",
            Qt.UserRole + 5: b"DisplayableFilePermissionsRole",
            Qt.UserRole + 6: b"LastModifiedRole",
            Qt.UserRole + 7: b"UrlStringRole"
        }
        return roles

    def data(self, index, role=Qt.DisplayRole):
        role = Qt.DisplayRole
        return super(FileSystemModel, self).data(index, role)

    def columnCount(self, index):
        return super(FileSystemModel, self).columnCount()

if __name__ == '__main__':
    if "-qml-quick" in sys.argv:
        app = QGuiApplication(sys.argv)
        view = QQuickView()
        fsmodel = FileSystemModel()
        root_context = view.rootContext().setContextProperty("fsmodel", fsmodel)
        view.setSource(QUrl.fromLocalFile('simple_treeview.qml'))
        view.show()
        sys.exit(app.exec_())
    elif "-qml" in sys.argv:
        app = QGuiApplication(sys.argv)
        #engine = QQmlApplicationEngine()
        ##qmlRegisterUncreatableType(FileSystemModel, "io.qt.examples.quick.controls.filesystembrowser", 1, 0,
                                ##"FileSystemModel", "Cannot create a FileSystemModel instance.")
        #context = engine.rootContext()

        fsmodel = FileSystemModel()
        fsmodel.setRootPath('/')

        #root_context = view.rootContext().setContextProperty("fsmodel", fsmodel)
        #view.setSource(QUrl.fromLocalFile('simple_treeview.qml'))
        #view.show()
        #sys.exit(app.exec_())

        #engine.rootContext().setContextProperty("fileSystemModel", fsmodel)
        #context.setContextProperty("main", engine)
        #engine.load(QUrl.fromLocalFile('treeview.qml'))
        #mainWin = engine.rootObjects()[0]

        #mainWin.show()
        #sys.exit(app.exec_())

    else:
        app = QApplication(sys.argv)

        model = FileSystemModel()
        model.setRootPath('')
        tree = QTreeView()
        tree.setModel(model)

        tree.setAnimated(False)
        tree.setIndentation(20)
        tree.setSortingEnabled(True)

        tree.setWindowTitle("Dir View")
        tree.resize(640, 480)
        tree.show()

        sys.exit(app.exec_())