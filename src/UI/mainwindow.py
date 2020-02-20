import logging

from PyQt5.QtWidgets import QMainWindow
from PyQt5.Qt import * # noqa: F403
from UI.widgets import MainBuildMenu
from UI.stdredirect import OutputWindow

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("C++ Build Assistant")

        logger.info("setting central widget")

        self.owind = OutputWindow(parent=None)
        self.toggle_output_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_L), self) # noqa: F405
        self.toggle_output_shortcut.activated.connect(self.toggleoutput)

        self.setCentralWidget(MainBuildMenu(self))
        self.show()
    
    def closeEvent(self, event) -> None:
        logger.debug(MainWindow.closeEvent.__qualname__ + ": Triggered")
        self.owind.doclose = True
        self.owind.close()
    
    @pyqtSlot() # noqa: F405
    def toggleoutput(self) -> None:
        logger.debug(self.toggleoutput.__qualname__ + ": tiggered")
        if not self.owind.isVisible():
            print("qwdkjwkjnwdqknqwdlnqwdlknqwdlk\n\nthis is test text\n\nI hope this works!!")
            logger.debug("Showing output window")
            self.owind.show()
        else:
            logger.debug("Hiding output window")
            self.owind.hide()