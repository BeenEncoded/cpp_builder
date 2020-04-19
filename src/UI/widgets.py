from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal

import logging, os

from UI.stdredirect import STDOutWidget
from data import Configuration
from globaldata import CONFIG

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

class ProjectSelectionMenu(HandyBaseWidget):
    def __init__(self, parent):
        super(ProjectSelectionMenu, self).__init__(parent)
        self._layout()
        self._handlers()
    
    def _layout(self):
        mainlayout = QVBoxLayout()

        self.pathTextBox = QLineEdit()
        self.pathTextBox.setPlaceholderText("The Path to your Project")
        self.submitbutton = QPushButton("Select Folder")

        mainlayout.addLayout(self.hLayout([self.pathTextBox, self.submitbutton]))
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
    pathEdited = pyqtSignal(str)

    def __init__(self, parent, dialogcaption: str=r"Open folder", placeholder: str=""):
        '''
        Creates a EditPathWidget.
        '''
        super(EditPathWidget, self).__init__(parent)
        self.placeholder = placeholder
        self.dialogcaption = dialogcaption
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
        self.selectFolderButton.clicked.connect(self._onFolderButtonClick)
    
    @pyqtSlot(str)
    def _onEdit(self, newtext: str="") -> None:
        '''
        Qt slot for the QLineEdit textEdited event.
        '''
        self._edited(newtext)
    
    @pyqtSlot()
    def _onFolderButtonClick(self) -> None:
        s = QFileDialog.getExistingDirectory(parent=Configuration.home_directory, caption=self.dialogcaption)
        logger.debug(f"Selected folder = \"{s}\"")
        if os.path.isdir(s):
            self.pathTextBox.setText(s)
            self._edited(s)

    def _edited(self, newpath: str = "") -> None:
        '''
        proxy function for the signal emmission.
        Should happen whenever the path has been edited by the user.  This means the 
        QlineEdit was modified or the user selected a folder from the dialog.
        '''
        self.onEdited.emit(newpath)

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

