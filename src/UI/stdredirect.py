import logging, sys

from PyQt5.QtWidgets import QVBoxLayout, QPlainTextEdit, QWidget
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

logger = logging.getLogger(__name__)

class OutputWindow(QWidget):
    def __init__(self, parent=None):
        super(OutputWindow, self).__init__(None)
        self._init_layout()
        logger.debug("Created output window")
        self.doclose = False #this allows for hiding and showing while disabling closing
    
    def _init_layout(self):
        mainlayout = QVBoxLayout()
        self.outputpane = STDOutWidget(self)
        mainlayout.addWidget(self.outputpane)

        self.setLayout(mainlayout)

    def closeEvent(self, event) -> None:
        logger.debug(OutputWindow.closeEvent.__qualname__ + ": triggered")
        if not self.doclose:
            if self.isVisible():
                self.hide()
                logger.debug("Hiding output window")
        else:
            if not self.close():
                logger.debug("failed to close window")
                raise RuntimeError("Unable to close " + OutputWindow.__qualname__)

class STDOutWidget(QWidget):
    def __init__(self, parent):
        super(STDOutWidget, self).__init__(parent)
        self._init_layout()
        self._connect_handlers()
    
    def _init_layout(self):
        mainlayout = QVBoxLayout()
        self.output_box = QPlainTextEdit()
        mainlayout.addWidget(self.output_box)

        self.setLayout(mainlayout)
    
    def _connect_handlers(self):
        UIStream.stdout().messageWritten.connect(self.write_message)
        UIStream.stderr().messageWritten.connect(self.write_message)
    
    @pyqtSlot(str)
    def write_message(self, message: str="") -> None:
        self.output_box.appendPlainText(message)

class UIStream(QObject):
    '''
    Can be used to redirect stdout and stderr from the console to 
    a UI element.
    '''

    _stdout = None
    _stderr = None
    messageWritten = pyqtSignal(str)

    def flush(self):
        pass
    
    def fileno(self):
        return -1
    
    def write(self, msg):
        if(not self.signalsBlocked()):
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        if(not UIStream._stdout):
            UIStream._stdout = UIStream()
            sys.stdout = UIStream._stdout
        return UIStream._stdout

    @staticmethod
    def stderr():
        if(not UIStream._stderr):
            UIStream._stderr = UIStream()
            sys.stderr = UIStream._stderr
        return UIStream._stderr