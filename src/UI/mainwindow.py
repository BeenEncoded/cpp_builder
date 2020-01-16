import logging

from PyQt5.QtWidgets import QMainWindow

logger = logging.getLogger("mainwindow")

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("C++ Build Assistant")
        self.show()