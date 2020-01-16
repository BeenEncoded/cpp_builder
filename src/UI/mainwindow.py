import logging

from PyQt5.QtWidgets import QMainWindow
from UI.widgets import MainBuildMenu

logger = logging.getLogger("mainwindow")

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("C++ Build Assistant")

        logger.info("setting central widget")
        self.setCentralWidget(MainBuildMenu(self))
        self.show()