import logging, sys

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
logger = None

from PyQt5.QtWidgets import QApplication

from UI.mainwindow import MainWindow

def showiu():
    app = QApplication(sys.argv)
    mainwindow = MainWindow() # noqa: F841
    setup_logging()
    global logger
    logger = logging.getLogger(__name__)
    logger.info("Program starting")
    return app.exec()

if __name__ == "__main__":
    showiu()