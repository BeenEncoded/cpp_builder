import logging

from data import ProjectInformation, SupportedCmakeGenerators

logger = logging.getLogger("TEST: " + __name__)

def actual_project_information() -> ProjectInformation:
    testinfo = ProjectInformation()
    testinfo.project_directory = r"D:\beene\Documents\coding\C++\Current_projects\test_2019"
    testinfo.source_directory = r""
    testinfo.build_directory = r"build"
    testinfo.cpp_compiler = r"C:\Program Files\LLVM\bin\clang++.exe"
    testinfo.c_compiler = r"C:\Program Files\LLVM\bin\clang.exe"
    testinfo.generator_type = SupportedCmakeGenerators.NMAKE_MAKEFILE
    testinfo.cmake_cmd = "cmake.exe"
    testinfo.build_targets = ["debug"]
    testinfo.cmake_include_path = [r"D:\beene\Documents\coding\C++\Current_projects\test_2019\src\main"]
    testinfo.cmake_library_path = [r"C:\Program Files\LLVM\lib\clang\9.0.0\include"]
    return testinfo

