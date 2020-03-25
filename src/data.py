import configparser, dataclasses, logging, os, typing, subprocess, shutil, enum, sys
import re, json

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
    "Visual Studio 10 2010 x64", #10
    "Visual Studio 9 2008 x86",
    "Visual Studio 9 2008 x64",
    "Borland Makefiles",
    "NMake Makefiles", #14
    "NMake Makefiles JOM",
    "MSYS Makefiles",
    "MinGW Makefiles",
    "Unix Makefiles", #18
    "Green Hills MULTI",
    "Ninja", #20
    "Watcom WMake",
    "CodeBlocks - MinGW Makefiles",
    "CodeBlocks - NMake Makefiles",
    "CodeBlocks - NMake Makefiles JOM",
    "CodeBlocks - Ninja",
    "CodeBlocks - Unix Makefiles",
    "CodeLite - MinGW Makefiles",
    "CodeLite - NMake Makefiles",
    "CodeLite - Ninja",
    "CodeLite - Unix Makefiles",#30
    "Sublime Text 2 - MinGW Makefiles",
    "Sublime Text 2 - NMake Makefiles",
    "Sublime Text 2 - Ninja",
    "Sublime Text 2 - Unix Makefiles",
    "Kate - MinGW Makefiles",
    "Kate - NMake Makefiles",
    "Kate - Ninja",
    "Kate - Unix Makefiles",
    "Eclipse CDT4 - NMake Makefiles",
    "Eclipse CDT4 - MinGW Makefiles",#40
    "Eclipse CDT4 - Ninja",
    "Eclipse CDT4 - Unix Makefiles"]

class OsType(enum.IntFlag):
    '''
    Operating system support bitmask.
    '''
    NO_SUPPORT = 0
    WINDOWS = enum.auto()
    LINUX = enum.auto()
    OSX = enum.auto()

class ProjectCommands(enum.IntFlag):
    '''
    Project command bitmask.  This is used in the execution process to
    determine which commands to execute.
    '''
    NO_COMMAND = 0
    MAKE = enum.auto()
    CMAKE = enum.auto()
    CLEAN = enum.auto()

def current_os() -> OsType:
    '''
    Returns the OsType corresponding to the platform currently being used.
    '''
    systems = { #expressions paired with each platform type
        r"([Ww][Ii][Nn])": OsType.WINDOWS,
        r"([Ll]inux)": OsType.LINUX,
        r"([Dd]arwin)|(osx)|(OSX)": OsType.OSX
    }
    plat = sys.platform

    for expression in systems:
        if re.match(expression, plat):
            return systems[expression]
    return OsType.NO_SUPPORT

class SupportedCmakeGenerators(enum.Enum):
    '''
    This enum is an enumeration of metadata associated with each makefile
    generation type.  Unsupported (by this software) makefile types are not included.

    Each value includes a bitmask indicating what operating systems are
    supported by the value in question.  For instance, nmake is not
    supported on linux, and make is not supported on windows.
    '''
    NMAKE_MAKEFILE = (CMAKE_GENERATOR_TYPES[14], "nmake", OsType.WINDOWS) #not supported on linux
    UNIX_MAKEFILE = (CMAKE_GENERATOR_TYPES[18], "make", OsType.LINUX)   #not supported on windows

    def __init__(self, generatorname: str="", makecommand: str="", operating_system: OsType=OsType.NO_SUPPORT):
        self.generator_name = generatorname
        self.make_command = makecommand
        self.support = operating_system

class Configuration:
    '''
    This helps to centralize all code relating to saving, storing, getting, and 
    initializing global program configuration.
    '''
    filename: str = "cppbuilder.conf"

    def __init__(self):
        logger.debug("Configuration instantiated.")

        # set up the configuration, initializing it with some sane defaults
        self.config = self._default_config()

        # here we make sure that we search for a config file, and
        # if none is loaded we write it.
        if len(self.config.read([Configuration.filename])) == 0:
            logger.warning("Configuration file not found, saving to " +
                           (os.path.abspath(".") + os.path.sep + Configuration.filename))
            self.save()

    # This function returns a default configuration.
    def _default_config(self):
        '''
        Returns the a default configuration for the entire program.
        '''
        c = configparser.ConfigParser()

        #set default key-value pairs here
        c['DEFAULT'] = {
            'projects': []
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
        with open(Configuration.filename, 'w') as config_file:
            self.config.write(config_file)

    def __repr__(self):
        some_stuff = []
        for key in self.config:
            some_stuff.append(f"SECTION[{key}]")
            some_stuff += [f"{x}: {self.config[key][x]}" for x in self.config[key]]
        return os.linesep.join(some_stuff)

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

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
    generator_type: SupportedCmakeGenerators=SupportedCmakeGenerators.NMAKE_MAKEFILE

    #cmake system-dependent arguments that persist between different projects:
    cpp_compiler: str = ""
    c_compiler: str = ""
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

    def tojson(self) -> str:
        '''
        Returns this object as a json string.
        '''
        thisobject = {
            "projectdir": self.project_directory,
            "sourcedir": self.source_directory,
            "builddir": self.build_directory,
            "distdir": self.dist_directory,
            "cmakegenerator": self.generator_type.name,
            "cppcompiler": self.cpp_compiler,
            "ccompiler": self.c_compiler,
            "cmakecmd": self.cmake_cmd,
            "cmakelibpaths": self.cmake_library_path,
            "cmakeincludepaths": self.cmake_include_path,
            "buildtargets": self.build_targets,
            "makeargs": self.make_arguments
        }
        return json.dumps(thisobject, sort_keys=True, indent=4)

    def fromjson(self, data: str="") -> None:
        '''
        Takes a string representing json stuff and loads it into this 
        object.
        '''
        loadeddata = json.loads(data)
        self.project_directory = loadeddata["projectdir"]
        self.source_directory = loadeddata["sourcedir"]
        self.build_directory = loadeddata["builddir"]
        self.dist_directory = loadeddata["distdir"]
        for g in SupportedCmakeGenerators:
            if g.name == loadeddata["cmakegenerator"]:
                self.generator_type = g
                break
        self.cpp_compiler = loadeddata["cppcompiler"]
        self.c_compiler = loadeddata["ccompiler"]
        self.cmake_cmd = loadeddata["cmakecmd"]
        self.cmake_library_path = loadeddata["cmakelibpaths"]
        self.cmake_include_path = loadeddata["cmakeincludepaths"]
        self.build_targets = loadeddata["buildtargets"]
        self.make_arguments = loadeddata["makeargs"]

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
        return (os.path.isfile(self.cpp_compiler) and os.path.isfile(self.c_compiler) and
            os.path.isdir(self.project_directory) and os.path.isdir(self.source_directory) and 
            ((self.generator_type.support & current_os()) == current_os()))
    
    def applyconfig(self, config: Configuration=None) -> None:
        '''
        Applies configuration to this object.  This can be used to store some settings
        that are system-wide in configuration instead of as a project-depenedent file and
        then apply them as 'defaults'.
        '''
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

        command.append("-G")
        command.append(self._sanitize_argument(self.generator_type.generator_name))
        
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
        command = [self.generator_type.make_command]

        if len(self.make_arguments) > 0:
            for arg in self.make_arguments:
                command.append(self._sanitize_argument(arg))
        
        if len(self.build_targets) > 0:
            for target in self.build_targets:
                command.append(self._sanitize_argument(target))
        
        return command

    def execute(self, 
        commands: ProjectCommands=(ProjectCommands.CMAKE | ProjectCommands.MAKE)) -> bool:
        '''
        Executes the build process on this project.  If cleanbuild is True,
        then the build directory will be deleted and recreated.
        '''
        if not self.isvalid():
            logger.warning("Attempted to execute invald project.  " + repr(self))
            return False
        
        #make the build directory if it does not yet exist.
        if not os.path.isdir(self.build_directory):
            try:
                os.makedirs(self.build_directory)
            except OSError:
                logger.error(ProjectInformation.execute.__qualname__ + ": what??")
            if not os.path.isdir(self.build_directory):
                logger.error("Could not create the build directory!!")
                return False

        #I will make no attempt to explain this.
        #It was non-trivial to write.  Have fun reading.
        success = False
        doclean = ((commands & ProjectCommands.CLEAN) == ProjectCommands.CLEAN)
        docmake = ((commands & ProjectCommands.CMAKE) == ProjectCommands.CMAKE)
        if doclean:
            success = True # TODO: implement
        if docmake and (success == doclean):
            success = self._run_command(self.cmake(), new_cwd=self.build_directory)
        if((commands & ProjectCommands.MAKE) == ProjectCommands.MAKE) and (success == docmake):
            success = self._run_command(self.make(), new_cwd=self.build_directory)
        return success
    
    def _run_command(self, command: list=[], new_cwd: str="") -> bool:
        if len(command) == 0:
            return True #the command is to do nothing, right?  We are successful!
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
        except FileNotFoundError as e: #on windows, command not found
            logger.error(repr(e) + os.linesep + "Command: " + ' '.join(command))
            if ((current_os() & OsType.WINDOWS) == OsType.WINDOWS):
                #if windows, usually you need to run the stoopehd vcvars cmd thing, and launch the build proc
                #off of that.  if linux, then a hole in space and time is probably distracting you from this...
                logger.info(os.linesep + os.linesep + "You likely need to run vcvars64 or vcvars32 to set the environment " + 
                    "variables that this process must inherit for the appropriate commands to be " + 
                    "successfully called." + os.linesep)
        except subprocess.CalledProcessError as e: #execution return value != 0
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

