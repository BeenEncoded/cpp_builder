import unittest, logging, sys

from data import ProjectInformation, CMAKE_GENERATOR_TYPES, OsType, SupportedCmakeGenerators
import data
from unit_tests import testdata

logger = logging.getLogger("TEST: " + __name__)

class ProjectInformationTestCase(unittest.TestCase):

    @unittest.skip("Skipping test_command_generation")
    def test_command_generation(self) -> None:
        info = testdata.actual_project_information()
        logger.debug("Testinfo: ")
        logger.debug("build_directory: " + info.build_directory)
        logger.debug("source_directory: " + info.source_directory)
        logger.debug("project_directory: " + info.project_directory)
        logger.debug(info.cmake())
        logger.debug(info.make())
    
    # @unittest.skip("Skipping test_command_execution")
    def test_command_execution(self) -> None:
        try:
            info = testdata.actual_project_information()
            self.assertEqual(info.execute(), True)
        except Exception as e:
            logger.error(repr(e))
            self.assertTrue(False)
    
    @unittest.skip("Skipping test_ostype_enum")
    def test_ostype_enum(self) -> None:
        try:
            print(repr(list(OsType)))
            print(repr(list(SupportedCmakeGenerators)))
            print(sys.platform)
            print(repr(data.current_os()))
            self.assertTrue(True)
        except Exception as e:
            logger.error(repr(e))
            self.assertTrue(False)

