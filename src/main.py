import logging, sys

from globaldata import LOG_LEVEL, LOGFILE, CONFIG
from logging.handlers import RotatingFileHandler

def setup_logging():
    root = logging.getLogger()
    f = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] -> %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(f)
    root.addHandler(sh)

    if CONFIG['DEFAULT']['logfile'] == "on":
        fh = logging.FileHandler(LOGFILE)
        fh = RotatingFileHandler(
            LOGFILE,
            mode='a',
            maxBytes=((2**20) * 2.5),
            backupCount=2,
            encoding=None,
            delay=False)
        
        fh.setFormatter(f)
        root.addHandler(fh)

    root.setLevel(LOG_LEVEL)

setup_logging()
logger = logging.getLogger(__name__)

from PyQt5.QtWidgets import QApplication

from UI.mainwindow import MainWindow

def showiu():
    app = QApplication(sys.argv)
    mainwindow = MainWindow() # noqa: F841
    logger.info("Program starting")
    return app.exec()

if __name__ == "__main__":
    showiu()