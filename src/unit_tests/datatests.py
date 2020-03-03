import unittest, logging

from data import ProjectInformation, CMAKE_GENERATOR_TYPES
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
    
    def test_command_execution(self) -> None:
        info = testdata.actual_project_information()
        self.assertEqual(info.execute(), True)