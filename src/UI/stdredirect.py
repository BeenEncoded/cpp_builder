import logging, sys, re

from PyQt5.QtWidgets import QVBoxLayout, QPlainTextEdit, QWidget
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

logger = logging.getLogger(__name__)

class OutputWindow(QWidget):
    '''
    A window that can be used instead of the widget.

    For imbedding a widget that redirects stdio into another window
    (for instance, adding stdio redirect to a QMainWindow, or
    adding it to a widget or window you've already created)
    see STDOutWidget.
    '''
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

    Operates like std::shared_ptr<T>; using a static instance of a member variable
    it tracks its instances.
    When the last instance is deleted the stdout and stderr streams are reset to the
    original objects.
    '''
    _instance_count = 0

    def __init__(self, parent):
        super(STDOutWidget, self).__init__(parent)
        self._init_layout()
        self._connect_handlers()
        STDOutWidget._instance_count += 1
    
    def __del__(self):
        STDOutWidget._instance_count -= 1
        if STDOutWidget._instance_count == 0:
            UIStream.reset_streams()

    def _init_layout(self):
        mainlayout = QVBoxLayout()
        self.output_box = QPlainTextEdit()

        #set up the output box configuration
        self.output_box.setReadOnly(True)
        self.output_box.setBackgroundVisible(False)
        self.output_box.setStyleSheet(r"QPlainTextEdit {color: white; " + 
            r"background-color: black; font-family: consolas, monospace; font-size: 11pt;}")

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
    A singleton that serves to redirect stdio to a UI element.

    WARNING: This object takes advantage of the Qt5 library's UI event handling.
        Because of this, all messages are sent as print events to
        the event handler thread (along with ALL OTHER UI EVENTS), so
        if you tear your arm off with a tree pruner because you don't
        know what you're doing: you know who to blame.
        Also you deserve it.
    '''
    _streamsdifferent = False
    _stdout = None
    _stderr = None
    messageWritten = pyqtSignal(str)

    def __init__(self, original_stream=None, set_back=None):
        super(UIStream, self).__init__(None)
        self.original = original_stream
        self._set_back = set_back

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
    def _setbackstdout(ob):
        sys.stdout = ob.original

    @staticmethod
    def _setbackstderr(ob):
        sys.stderr = ob.original

    @staticmethod
    def stdout():
        if(not UIStream._stdout):
            UIStream._stdout = UIStream(original_stream=sys.stdout, set_back=UIStream._setbackstdout)
            sys.stdout = UIStream._stdout
            UIStream._streamsdifferent = True
            logger.debug("stdout redirected!")
        return UIStream._stdout

    @staticmethod
    def stderr():
        if(not UIStream._stderr):
            UIStream._stderr = UIStream(original_stream=sys.stderr, set_back=UIStream._setbackstderr)
            sys.stderr = UIStream._stderr
            UIStream._streamsdifferent = True
            logger.debug("stderr redirected!")
        return UIStream._stderr
    
    @staticmethod
    def reset_streams():
        '''
        Resets the streams to their original values.  This can be used
        to preserve stdout and stderr when the ui is destroyed.
        '''
        if UIStream._streamsdifferent:
            UIStream.stdout()._set_back(UIStream.stdout())
            UIStream.stderr()._set_back(UIStream.stderr())
            UIStream._streamsdifferent = False
            print("streams reset")
