'''
This file serves as an alternate main that runs unit tests for this software.
By no means should this file, or any modules under the unit_tests package be
included in a release build of this software.
'''
import unittest, logging, sys

from unit_tests.datatests import ProjectInformationTestCase # noqa: F401

def setup_logging():
    root = logging.getLogger()
    f = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] -> %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    # fh = logging.FileHandler(LOGFILE)
    # fh = RotatingFileHandler(
    #     LOGFILE,
    #     mode='a',
    #     maxBytes=((2**20) * 2.5),
    #     backupCount=2,
    #     encoding=None,
    #     delay=False)

    sh.setFormatter(f)
    # fh.setFormatter(f)

    root.addHandler(sh)
    # root.addHandler(fh)
    root.setLevel(logging.DEBUG)

setup_logging()
logger = logging.getLogger("TEST: test.main")

if __name__ == "__main__":
    unittest.main()