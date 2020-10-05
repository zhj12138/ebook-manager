from PyQt5.QtCore import QThread, pyqtSignal


class EmailThread(QThread):
    finishSignal = pyqtSignal(bool)

    def __init__(self, func, args):
        super(EmailThread, self).__init__()
        self.func = func
        self.args = args
        self.ret = None

    def run(self):
        self.ret = self.func(*self.args)
        self.finishSignal.emit(self.ret)


class convertThread(QThread):
    finishSignal = pyqtSignal()

    def __init__(self, func, args):
        super(convertThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)
        self.finishSignal.emit()
