import logging, sys, re

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
    '''
    Basically a QPlainTextEdit but it shows the stdout.
    '''

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

    def __init__(self, original_stream=None):
        super(UIStream, self).__init__(None)
        self.original = original_stream

    def flush(self):
        pass
    
    def fileno(self):
        return -1
    
    def write(self, msg):
        if(not self.signalsBlocked()):
            if msg != "\n":
                self.messageWritten.emit(self.uiformatted(msg))
            self.original.write(msg)

    def uiformatted(self, message: str="") -> str:
        '''
        Some messages look goofy (added newlines, whatever).
        We have to try to grab them and make them not fucked up.
        '''
        chars = [
            ("\n", "\\n"), 
            ("\r", "\\r")]
        if self.islogmessage(message):
            for c in chars:
                message = message.replace(c[0], "")
        
        #now we will replace all the newlines and returns with actual newlines and returns
        for c in chars:
            message = message.replace(c[0], c[1])
        return message

    def islogmessage(self, message="") -> bool:
        '''
        Matches a log message specific to my personal formatting.
        If you don't use my formatting, you're wrong.  :D

        But in all seriousness, log messages were getting an extra newline appended in the UI, so
        it became necessary to intercept and strip those newlines.  This is 
        the resulting solution.
        '''
        if not hasattr(self, "logregex"):
            self.logregex = re.compile(r"(\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2},\d{1,3} \[[A-Za-z0-9_\.]+\] \[[A-Za-z]+\] \->)")
        return (self.logregex.match(message) is not None)

    @staticmethod
    def stdout():
        if(not UIStream._stdout):
            UIStream._stdout = UIStream(original_stream=sys.stdout)
            sys.stdout = UIStream._stdout
            logger.debug("stdout redirected!")
        return UIStream._stdout

    @staticmethod
    def stderr():
        if(not UIStream._stderr):
            UIStream._stderr = UIStream(original_stream=sys.stderr)
            UIStream._origstderr = sys.stderr
            sys.stderr = UIStream._stderr
            logger.debug("stderr redirected!")
        return UIStream._stderr