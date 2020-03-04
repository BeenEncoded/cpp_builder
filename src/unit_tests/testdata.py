import logging

from data import ProjectInformation, SupportedCmakeGenerators

logger = logging.getLogger("TEST: " + __name__)

def actual_project_information() -> ProjectInformation:
    testinfo = ProjectInformation()
    testinfo.project_directory = r"C:\Users\beene.DESKTOP-NGBJDSG\Documents\coding\C++\Current_projects\test_2019"
    testinfo.source_directory = r"C:\Users\beene.DESKTOP-NGBJDSG\Documents\coding\C++\Current_projects\test_2019"
    testinfo.build_directory = r"C:\Users\beene.DESKTOP-NGBJDSG\Documents\coding\C++\Current_projects\test_2019\build"
    testinfo.cpp_compiler = r"C:\LLVM\bin\clang++.exe"
    testinfo.c_compiler = r"C:\LLVM\bin\clang.exe"
    testinfo.generator_type = SupportedCmakeGenerators.NMAKE_MAKEFILE
    testinfo.cmake_cmd = "cmake.exe"
    testinfo.build_targets = ["debug"]
    testinfo.cmake_include_path = [r"C:\Users\beene.DESKTOP-NGBJDSG\Documents\coding\C++\Current_projects\test_2019\src\main"]
    testinfo.cmake_library_path = [r"C:\Users\lib",
                                    r"C:\LLVM\lib\clang\9.0.0\include"]
    return testinfo

