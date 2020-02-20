from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

import logging

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
        self.setLayout(mainlayout)
    
    def _connect_handlers(self):
        pass
