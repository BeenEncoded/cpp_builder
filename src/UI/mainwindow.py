import logging, io

from PyQt5.QtWidgets import QMainWindow
from UI.widgets import MainBuildMenu

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("C++ Build Assistant")

        logger.info("setting central widget")
        self.setCentralWidget(MainBuildMenu(self))
        self.show()