from pandasqt.compat import QtCore, QtGui, Qt, Signal, Slot


class ProgressWorker(QtCore.QObject):
    progressChanged = Signal(int)
    finished = Signal()

    def __init__(self, name):
        super(ProgressWorker, self).__init__()
        self.name = name

    @Slot()
    def doWork(self):
        self.run()
        # emit the result of the operation?
        self.finished.emit()

    def run(self):
        raise NotImplemented



def createThread(parent, worker):
    thread = QtCore.QThread(parent)
    thread.started.connect(worker.doWork)
    thread.finished.connect(worker.deleteLater)

    worker.moveToThread(thread)
    return thread
