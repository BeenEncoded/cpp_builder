from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot

import logging

from UI.stdredirect import STDOutWidget

logger = logging.getLogger(__name__)

class MainBuildMenu(QWidget):
    def __init__(self, parent):
        super(MainBuildMenu, self).__init__(parent)

        self._init_layout()
        self._connect_handlers()
    
    def _init_layout(self):
        mainlayout = QVBoxLayout()

        self.l = QLabel("Hello World")
        self.l.setAlignment(Qt.AlignCenter)

        mainlayout.addWidget(self.l)
        mainlayout.addWidget(STDOutWidget(self))
        self.setLayout(mainlayout)
    
    def _connect_handlers(self):
        pass

    @pyqtSlot()
    def printtest(self) -> None:
        logger.debug("Test log message")
        print("Print test message\nmultiline test")
        print("a seperate print line")