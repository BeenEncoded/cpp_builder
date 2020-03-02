from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot

import logging, threads

from UI.stdredirect import STDOutWidget
from data import ProjectInformation, CMAKE_GENERATOR_TYPES

logger = logging.getLogger(__name__)

class MainBuildMenu(QWidget):
    def __init__(self, parent):
        super(MainBuildMenu, self).__init__(parent)

        self._init_layout()
        self._connect_handlers()
    
    def __del__(self):
        pass # CLEANUP

    def _init_layout(self):
        mainlayout = QVBoxLayout()
        self.test_button = QPushButton("Test")
        
        mainlayout.addWidget(self.test_button)
        mainlayout.addWidget(STDOutWidget(self))
        self.setLayout(mainlayout)
    
    def _connect_handlers(self):
        self.test_button.clicked.connect(self.dataTest)

    @pyqtSlot()
    def printtest(self) -> None:
        logger.debug("Test log message")
        print("Print test message\nmultiline test")
        print("a seperate print line")

    @pyqtSlot()
    def dataTest(self) -> None:
        testinfo = ProjectInformation()
        testinfo.project_directory = "C:\\Users\\beene.DESKTOP-NGBJDSG\\Documents\\coding\\C++\\Current_projects\\test_2019"
        testinfo.source_directory = "C:\\Users\\beene.DESKTOP-NGBJDSG\\Documents\\coding\\C++\\Current_projects\\test_2019\\src"
        testinfo.cpp_compiler = "C:\\LLVM\\bin\\clang++.exe"
        testinfo.c_compiler = "C:\\LLVM\\bin\\clang.exe"
        testinfo.generator_type = CMAKE_GENERATOR_TYPES[14]
        testinfo.make_cmd = "nmake"
        testinfo.build_targets = ["release", "debug"]
        testinfo.cmake_include_path = ["C:\\Users\\beene.DESKTOP-NGBJDSG\\Documents\\coding\\C++\\Current_projects\\test_2019\\src\\main"]
        testinfo.cmake_library_path = ["C:\\Users\\lib",
                                        "C:\\LLVM\\lib\\clang\\9.0.0\\include"]
        logger.debug("Testinfo: ")
        logger.debug(testinfo.cmake())
        logger.debug(testinfo.make())