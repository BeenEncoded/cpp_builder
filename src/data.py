import configparser, dataclasses, logging, os, typing, subprocess, shutil

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
        self.filename = "cppbuilder.conf"

        # here we make sure that we search for a config file, and
        # if none is loaded we write it.
        if len(self.config.read([self.filename])) == 0:
            logger.warning("Configuration file not found, saving to " +
                           (os.path.abspath(".") + os.path.sep + self.filename))
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

        c['SYSTEMCONFIG'] = {
            "cppcompiler": "g++",
            "ccompiler": "gcc",
            "makecmd": "make",
            "cmakecmd": "cmake",
            "generator": CMAKE_GENERATOR_TYPES[18],
            "libfolders": [],
            "includefolders": []
        }

        return c

    def save(self) -> None:
        logger.info("Saving configuration")
        with open(self.filename, 'w') as config_file:
            self.config.write(config_file)

@dataclasses.dataclass
class ProjectInformation:
    '''
    All data a CMake project needs.  Essentially these variables
    will be passed as arguments if set.
    '''
    #project-specific settings:
    project_directory: str = os.getcwd()
    source_directory: str = (os.getcwd() + os.path.sep + "src")
    build_directory: str = (os.getcwd() + os.path.sep + "build")
    dist_directory: str = (os.getcwd() + os.path.sep + "dist")

    #cmake arguments and specifiers
    generator_type: str = CMAKE_GENERATOR_TYPES[14] #default to NMake

    #cmake system-dependent arguments that persist between different projects:
    cpp_compiler: str = ""
    c_compiler: str = ""
    make_cmd: str = "nmake" #the system's make command.  nmake on windows, make on Linux.
    cmake_cmd: str = "cmake"

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
    
    # nmake arguments and target specifiers
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
    
    def applyconfig(self, config: Configuration=None) -> None:
        sconfig = config.config["SYSTEMCONFIG"]
        self.cpp_compiler = sconfig["cppcompiler"]
        self.c_compiler = sconfig["ccompiler"]
        self.make_cmd = sconfig["makecmd"]
        self.cmake_cmd = sconfig["cmakecmd"]
        self.cmake_library_path = sconfig["libfolders"]
        self.cmake_include_path = sconfig["includefolders"]

    def cmake(self) -> list:
        '''
        Returns the cmake command for this configuration.
        '''
        command = [self.cmake_cmd]
        if(len(self.generator_type) > 0):
            command.append("-G")
            command.append(self._sanitize_argument(self.generator_type))
        
        if(len(self.c_compiler) > 0):
            command.append("-DCMAKE_C_COMPILER=" + self._sanitize_argument(os.path.abspath(self.c_compiler)))

        if(len(self.cpp_compiler) > 0):
            command.append("-DCMAKE_CXX_COMPILER=" + self._sanitize_argument(os.path.abspath(self.cpp_compiler)))
        
        if(len(self.cmake_include_path) > 0):
            command.append("-DCMAKE_INCLUDE_PATH=" + self._sanitize_argument(';'.join(self.cmake_include_path)))
        
        if(len(self.cmake_library_path) > 0):
            command.append("-DCMAKE_LIBRARY_PATH=" + self._sanitize_argument(';'.join(self.cmake_library_path)))

        if(len(self.source_directory) > 0):
            command.append(self._sanitize_argument(os.path.abspath(self.source_directory)))
        
        return command
    
    def make(self) -> list:
        '''
        Returns the make command for this configuration.
        '''
        command = [self.make_cmd]

        if len(self.make_arguments) > 0:
            for arg in self.make_arguments:
                command.append(self._sanitize_argument(arg))
        
        if len(self.build_targets) > 0:
            for target in self.build_targets:
                command.append(self._sanitize_argument(target))
        
        return command

    def execute(self, cleanbuild: bool=False) -> bool:
        '''
        Executes the build process on this project.  If cleanbuild is True,
        then the build directory will be deleted and recreated.
        '''
        if not os.path.isdir(self.build_directory):
            try:
                os.makedirs(self.build_directory)
            except OSError as e:
                logger.error(ProjectInformation.execute.__qualname__ + ": what??")
            if not os.path.isdir(self.build_directory):
                logger.error("Could not create the build directory!!")
                return False
        return (self._run_command(self.cmake(), new_cwd=self.build_directory) and self._run_command(self.make(), new_cwd=self.build_directory))
    
    def _run_command(self, command: list=[], new_cwd: str="") -> bool:
        if len(command) == 0:
            return True
        currentdir = os.getcwd()
        if len(new_cwd) > 0:
            if os.path.isdir(new_cwd):
                os.chdir(new_cwd)
                logger.debug("Changing into directory: \"" + new_cwd + "\"")
            else:
                logger.error(ProjectInformation._run_command.__qualname__ + 
                    ": new_cwd specified but the directory does not exist!")
                raise NotADirectoryError(ProjectInformation._run_command.__qualname__ + 
                    ": new_cwd specified but the directory does not exist!")

        success = False
        try:
            result = subprocess.run(command)
            success = (result.returncode == 0)
            if not success:
                logger.error("process failed: " + repr(result))
        except subprocess.CalledProcessError as e:
            logger.error("Command: " + str(e.cmd) + "\n" + 
                "OUTPUT: " + str(e.output) + "\n" + 
                "RETURN CODE: " + str(e.returncode))
        
        if os.getcwd() != currentdir:
            logger.debug("changing back into directory: \"" + currentdir + "\"")
            os.chdir(currentdir)
        return success

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

