import logging

from PyQt5.QtWidgets import QMainWindow
from PyQt5.Qt import * # noqa: F403
from UI.widgets import ProjectSelectionMenu
from UI.stdredirect import OutputWindow

from globaldata import CONFIG

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("C++ Build Assistant")

        logger.debug("setting central widget")

        #an aditional output window can be enabled by simply uncommenting the following line:
        #self._init_outputwindow()
        self.setCentralWidget(ProjectSelectionMenu(self))
        self.show()
    
    def closeEvent(self, event) -> None:
        logger.debug(MainWindow.closeEvent.__qualname__ + ": Triggered")
        self._close_outputwindow()
        CONFIG.save()
    
    def _init_outputwindow(self) -> None:
        self.owind = OutputWindow(parent=None)
        self.toggle_output_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_L), self) # noqa: F405
        self.toggle_output_shortcut.activated.connect(self.toggleoutput)
    
    def _close_outputwindow(self) -> None:
        if hasattr(self, "owind"):
            self.owind.doclose = True
            self.owind.close()

    @pyqtSlot() # noqa: F405
    def toggleoutput(self) -> None:
        logger.debug(self.toggleoutput.__qualname__ + ": tiggered")
        if not self.owind.isVisible():
            logger.info("Showing output window")
            self.owind.show()
        else:
            logger.info("Hiding output window")
            self.owind.hide()