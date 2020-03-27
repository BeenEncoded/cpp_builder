from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt

import logging, os

from UI.stdredirect import STDOutWidget
from data import Configuration

logger = logging.getLogger(__name__)

class HandyBaseWidget(QWidget):
    '''
    Just adds some nice functions to make things easier.
    '''
    def __init__(self, parent: any=None):
        super(HandyBaseWidget, self).__init__(parent)
    
    def hLayout(self, widgets: list=[]) -> QHBoxLayout:
        hl = QHBoxLayout()
        for w in widgets:
            hl.addWidget(w)
        return hl
    
    def vLayout(self, widgets: list=[]) -> QVBoxLayout:
        l = QVBoxLayout()
        for w in widgets:
            l.addWidget(w)
        return l

    

class ProjectSelectionMenu(QWidget):
    def __init__(self, parent):
        super(ProjectSelectionMenu, self).__init__(parent)
        self._layout()
        self._handlers()
    
    def _layout(self):
        mainlayout = QVBoxLayout()

        self.pathTextBox = QLineEdit()
        self.pathTextBox.setPlaceholderText("The Path to your Project")
        self.submitbutton = QPushButton("Select Folder")
        blahlayout = QHBoxLayout()
        blahlayout.addWidget(self.pathTextBox)
        blahlayout.addWidget(self.submitbutton)

        mainlayout.addLayout(blahlayout)
        self.setLayout(mainlayout)

    def _handlers(self):
        self.pathTextBox.textEdited.connect(self._updateButtonText)
        self.submitbutton.clicked.connect(self._submitButtonClicked)
        self.pathTextBox.returnPressed.connect(self._submitButtonClicked)
    
    @pyqtSlot(str)
    def _updateButtonText(self, nothing: any=None):
        self.submitbutton.setText("Open" if os.path.isdir(self.pathTextBox.text()) else "Select Folder")
    
    @pyqtSlot()
    def _submitButtonClicked(self):
        if os.path.isdir(self.pathTextBox.text()):
            self._openProject(self.pathTextBox.text())
        else:
            self._userSelectFolder()
    
    def _openProject(self, path: str="") -> None:
        if not os.path.isdir(path):
            raise Exception(f"{ProjectSelectionMenu._openProject.__qualname__}: path argument is not a folder!")
        logger.debug(f"{ProjectSelectionMenu._openProject.__qualname__}: Called")
    
    def _userSelectFolder(self) -> None:
        logger.debug(f"{ProjectSelectionMenu._userSelectFolder.__qualname__}: Called")
        folder = QFileDialog.getExistingDirectory(parent=self, 
            caption=r"Choose the folder of your project", directory=Configuration.home_directory)
        if os.path.isdir(folder):
            self.pathTextBox.setText(folder)
            self._updateButtonText()
            self._openProject(path=folder)

class BuildConfigurationMenu(HandyBaseWidget):
    def __init__(self, parent):
        super(BuildConfigurationMenu, self).__init__(parent)
        self._layout()
        self._handlers()
    
    def _layout(self) -> None:
        pass

    def _handlers(self) -> None:
        pass

class EditPathWidget(HandyBaseWidget):
    def __init__(self, parent, callback, placeholder: str=""):
        '''
        Creates a EditPathWidget.  When a callback is passed, when the 
        path is modified tyhe callback is called with the path (as a string) as the only argument.
        This can be used to write back the new path to the original object.
        '''
        super(EditPathWidget, self).__init__(parent)
        self.placeholder = placeholder
        self.callback = callback
        self._layout()
        self._handlers()
    
    def _layout(self) -> None:
        self.pathTextBox = QLineEdit()
        self.pathTextBox.setPlaceholderText(self.placeholder)
        self.selectFolderButton = QPushButton("Select Path")

        mainlayout = QVBoxLayout()
        mainlayout.addLayout(self.hLayout(widgets=[self.selectFolderButton, self.pathTextBox]))
        self.setLayout(mainlayout)

    def _handlers(self)->None:
        self.pathTextBox.textEdited.connect(self._onEdit)
    
    @pyqtSlot(str)
    def _onEdit(self, newtext: str="") -> None:
        self.callback(newtext)

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

