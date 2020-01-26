from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QPlainTextEdit
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from quithread import ThreadData, WindowUpdateThread

import logging, threading, io

logger = logging.getLogger("widgets")

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

class UIStream(QtCore.QObject):
    '''
    Can be used to redirect stdout and stderr from the console to 
    a UI element.
    '''

    _stdout = None
    _stderr = None
    messageWritten = pyqtSignal(str)

    def flush( self ):
        pass
    
    def fileno( self ):
        return -1
    
    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(unicode(msg))

    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if ( not XStream._stderr ):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr