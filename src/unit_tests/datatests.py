import unittest, logging

from data import ProjectInformation, CMAKE_GENERATOR_TYPES

logger = logging.getLogger(__name__)

class ProjectInformationTestCase(unittest.TestCase):
    def test_command_generation(self):
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