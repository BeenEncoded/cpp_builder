import logging

from data import ProjectInformation, CMAKE_GENERATOR_TYPES

logger = logging.getLogger("TEST: " + __name__)

def actual_project_information() -> ProjectInformation:
    testinfo = ProjectInformation()
    testinfo.project_directory = "C:\\Users\\beene.DESKTOP-NGBJDSG\\Documents\\coding\\C++\\Current_projects\\test_2019"
    testinfo.source_directory = "C:\\Users\\beene.DESKTOP-NGBJDSG\\Documents\\coding\\C++\\Current_projects\\test_2019"
    testinfo.build_directory = "C:\\Users\\beene.DESKTOP-NGBJDSG\\Documents\\coding\\C++\\Current_projects\\test_2019\\build"
    testinfo.cpp_compiler = "C:\\LLVM\\bin\\clang++.exe"
    testinfo.c_compiler = "C:\\LLVM\\bin\\clang.exe"
    testinfo.generator_type = CMAKE_GENERATOR_TYPES[14]
    testinfo.make_cmd = "nmake.exe"
    testinfo.cmake_cmd = "cmake.exe"
    testinfo.build_targets = ["debug"]
    testinfo.cmake_include_path = ["C:\\Users\\beene.DESKTOP-NGBJDSG\\Documents\\coding\\C++\\Current_projects\\test_2019\\src\\main"]
    testinfo.cmake_library_path = ["C:\\Users\\lib",
                                    "C:\\LLVM\\lib\\clang\\9.0.0\\include"]
    return testinfo

