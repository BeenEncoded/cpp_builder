from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot

import logging, threads

from UI.stdredirect import STDOutWidget

logger = logging.getLogger(__name__)

class MainBuildMenu(QWidget):
    def __init__(self, parent):
        super(MainBuildMenu, self).__init__(parent)
        self.tthread = TestThread()

        self._init_layout()
        self._connect_handlers()
        self.tthread.start()
    
    def __del__(self):
        self.tthread.halt_thread()

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

class TestThread(threads.Worker):
    def __init__(self):
        super(TestThread, self).__init__(None)
        self.throttle = 1
        self.count = 0

    def doWork(self):
        self.count += 1
        print(TestThread.doWork.__qualname__ + ": testprint iteration " + str(self.count))