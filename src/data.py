import configparser, dataclasses

class Configuration:
    '''
    This helps to centralize all code relating to saving, storing, getting, and 
    initializing global program configuration.
    '''

    def __init__(self):
        logger.debug("Configuration instantiated.")
        super(Configuration, self).__init__()

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
    cpp_compiler: str
    c_compiler: str
    project_directory: str
    generator_type: str
    