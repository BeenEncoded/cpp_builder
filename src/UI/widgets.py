from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class MainBuildMenu(QWidget):
    def __init__(self, parent):
        super(MainBuildMenu, self).__init__(parent)

        self._init_layout()
    
    def _init_layout(self):
        mainlayout = QVBoxLayout()

        self.l = QLabel("Hello World")
        self.l.setAlignment(Qt.AlignCenter)

        mainlayout.addWidget(self.l)
        self.setLayout(mainlayout)