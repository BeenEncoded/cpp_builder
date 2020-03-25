from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot

import logging
from pathlib import Path

from UI.stdredirect import STDOutWidget

logger = logging.getLogger(__name__)

class ProjectSelectionMenu(QWidget):
    def __init__(self, parent):
        super(ProjectSelectionMenu, self).__init__(parent)
        self._layout()
        self._handlers()
    
    def _layout(self):
        mainlayout = QVBoxLayout()



    def _handlers(self):
        pass



class MainBuildMenu(QWidget):
    def __init__(self, parent):
        super(MainBuildMenu, self).__init__(parent)

        self._init_layout()
        self._connect_handlers()
    
    def __del__(self):
        pass # CLEANUP

    def _init_layout(self):
        mainlayout = QVBoxLayout()

        mainlayout.addWidget(STDOutWidget(self))
        self.setLayout(mainlayout)
    
    def _connect_handlers(self):
        pass

    @pyqtSlot()
    def printtest(self) -> None:
        '''
        UI print test
        '''
        logger.debug("Test log message")
        print("Print test message\nmultiline test")
        print("a seperate print line")

