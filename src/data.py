import configparser, dataclasses, logging, os, typing

logger = logging.getLogger("data")

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
    #general settings:
    project_directory: str = os.getcwd()

    #cmake arguments and specifiers
    cpp_compiler: str = ""
    c_compiler: str = ""
    generator_type: str = ""
    
    # nmake arguments and specifiers
    build_targets: typing.List[str] = dataclasses.field(default_factory=list)
    nmake_arguments: typing.List[str] = dataclasses.field(default_factory=list)

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
        return ((self.generator_type in CMAKE_GENERATOR_TYPE) and 
            os.path.isfile(self.cpp_compiler) and os.path.isfile(self.c_compiler) and
            os.path.isdir(self.project_directory))

CMAKE_GENERATOR_TYPE: list = ["Visual Studio 16 2019",
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