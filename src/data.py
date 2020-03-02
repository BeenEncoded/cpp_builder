import configparser, dataclasses, logging, os, typing

logger = logging.getLogger(__name__)

CMAKE_GENERATOR_TYPES: list = ["Visual Studio 16 2019",
    "Visual Studio 15 2017 x86",
    "Visual Studio 15 2017 x64",
    "Visual Studio 14 2015 x86",
    "Visual Studio 14 2015 x64",
    "Visual Studio 12 2013 x86",
    "Visual Studio 12 2013 x64",
    "Visual Studio 11 2012 x86",
    "Visual Studio 11 2012 x64",
    "Visual Studio 10 2010 x86",
    "Visual Studio 10 2010 x64",
    "Visual Studio 9 2008 x86",
    "Visual Studio 9 2008 x64",
    "Borland Makefiles",
    "NMake Makefiles",
    "NMake Makefiles JOM",
    "MSYS Makefiles",
    "MinGW Makefiles",
    "Unix Makefiles",
    "Green Hills MULTI",
    "Ninja",
    "Watcom WMake",
    "CodeBlocks - MinGW Makefiles",
    "CodeBlocks - NMake Makefiles",
    "CodeBlocks - NMake Makefiles JOM",
    "CodeBlocks - Ninja",
    "CodeBlocks - Unix Makefiles",
    "CodeLite - MinGW Makefiles",
    "CodeLite - NMake Makefiles",
    "CodeLite - Ninja",
    "CodeLite - Unix Makefiles",
    "Sublime Text 2 - MinGW Makefiles",
    "Sublime Text 2 - NMake Makefiles",
    "Sublime Text 2 - Ninja",
    "Sublime Text 2 - Unix Makefiles",
    "Kate - MinGW Makefiles",
    "Kate - NMake Makefiles",
    "Kate - Ninja",
    "Kate - Unix Makefiles",
    "Eclipse CDT4 - NMake Makefiles",
    "Eclipse CDT4 - MinGW Makefiles",
    "Eclipse CDT4 - Ninja",
    "Eclipse CDT4 - Unix Makefiles"]

class Configuration:
    '''
    This helps to centralize all code relating to saving, storing, getting, and 
    initializing global program configuration.
    '''

    def __init__(self):
        logger.debug("Configuration instantiated.")

        # set up the configuration, initializing it with some sane defaults
        self.config = self._default_config()

        # here we make sure that we search for a config file, and
        # if none is loaded we write it.
        if len(self.config.read(["backup.conf"])) == 0:
            logger.warning("Configuration file not found, saving to " +
                           (os.path.abspath(".") + os.path.sep + "backup.conf"))
            self.save()

    # This function returns a default configuration.
    def _default_config(self):
        '''
        Returns the a default configuration for the entire program.
        '''
        c = configparser.ConfigParser()

        #set default key-value pairs here
        c['DEFAULT'] = {
        }

        return c

    def save(self):
        logger.info("Saving configuration")
        with open("backup.conf", 'w') as config_file:
            self.config.write(config_file)

@dataclasses.dataclass
class ProjectInformation:
    '''
    All data a CMake project needs.  Essentially these variables
    will be passed as arguments if set.
    '''

    #general settings:
    project_directory: str = os.getcwd()
    source_directory: str = os.getcwd()

    #cmake arguments and specifiers
    generator_type: str = CMAKE_GENERATOR_TYPES[14] #default to NMake

    #cmake system-dependent arguments that persist between different projects:
    cpp_compiler: str = ""
    c_compiler: str = ""
    make_cmd: str = "nmake" #the system's make command.  nmake on windows, make on Linux.

    '''
    CMAKE_LIBRARY_PATH (per the cmake documentation, V3.17.0):
    Semicolon-separated list of directories specifying a search path 
    for the find_library() command. By default it is empty, it is intended
    to be set by the project. See also CMAKE_SYSTEM_LIBRARY_PATH and CMAKE_PREFIX_PATH.
    Passed on the command line via -D
    only set this if you need to.
    '''
    cmake_library_path: typing.List[str] = dataclasses.field(default_factory=list)

    '''
    CMAKE_INCLUDE_PATH (per the cmake documentation V3.17.0):
    Semicolon-separated list of directories specifying a search path 
    for the find_file() and find_path() commands. By default it is empty,
    it is intended to be set by the project. See also CMAKE_SYSTEM_INCLUDE_PATH and CMAKE_PREFIX_PATH.
    Passed on the command line via -D
    Only set this if you need to.
    '''
    cmake_include_path: typing.List[str] = dataclasses.field(default_factory=list)
    
    # nmake arguments and specifiers
    build_targets: typing.List[str] = dataclasses.field(default_factory=list)
    make_arguments: typing.List[str] = dataclasses.field(default_factory=list)

    def isvalid(self) -> bool:
        '''
        Returns true if the data is valid to be passed to cmake.  This means that the 
        compilers should represent the absolute path to their respective compilers, the
        project directory should exist, and the generator type must be one of the types offered
        by cmake.

        This may return true even with invalid nmake aruments.  There are too many arguments that
        can be passed to make, and through make to the compiler -- and every combination thereof -- to
        support validation of so early in development.
        '''
        return ((self.generator_type in CMAKE_GENERATOR_TYPES) and 
            os.path.isfile(self.cpp_compiler) and os.path.isfile(self.c_compiler) and
            os.path.isdir(self.project_directory))
    
    def cmake(self) -> str:
        '''
        Returns the cmake command for this configuration.
        '''
        command = ["cmake"]
        if(len(self.generator_type) > 0):
            command.append("-G")
            command.append("\"" + self._sanitize_argument(self.generator_type) + "\"")
        
        if(len(self.c_compiler) > 0):
            command.append("-DCMAKE_C_COMPILER=\"" + self._sanitize_argument(os.path.abspath(self.c_compiler)) + "\"")

        if(len(self.cpp_compiler) > 0):
            command.append("-DCMAKE_CXX_COMPILER:Path=\"" + self._sanitize_argument(os.path.abspath(self.cpp_compiler)) + "\"")
        
        if(len(self.cmake_include_path) > 0):
            command.append("-DCMAKE_INCLUDE_PATH=\"" + self._sanitize_argument(';'.join(self.cmake_include_path)) + "\"")
        
        if(len(self.cmake_library_path) > 0):
            command.append("-DCMAKE_LIBRARY_PATH=\"" + self._sanitize_argument(';'.join(self.cmake_library_path)) + "\"")

        if(len(self.source_directory) > 0):
            command.append("\"" + self._sanitize_argument(os.path.abspath(self.source_directory)) + "\"")
        
        return ' '.join(command)
    
    def make(self) -> str:
        '''
        Returns the make command for this configuration.
        '''
        command = [self.make_cmd]

        if len(self.make_arguments) > 0:
            command.append(self._sanitize_argument(' '.join(self.make_arguments)))
        
        if len(self.build_targets) > 0:
            command.append(self._sanitize_argument(' '.join(self.build_targets)))
        
        return ' '.join(command)

    def _sanitize_argument(self, argument) -> str:
        '''
        Replaces invalid characters with their escaped equivilants.
        '''
        invalids = [("\"", "\\\""), 
            ("\'", "\\\'"),
            ("\\", "/")]
        
        for i in invalids:
            if i[0] in argument:
                argument = argument.replace(i[0], i[1])
        return argument

