import threading, time, logging
from PyQt5.QtCore import pyqtSignal, QObject

logger = logging.getLogger(__name__)

class WindowUpdateThread(QObject, threading.Thread):
    '''
    Represents a general worker thread for the UI (based on Qt5).
    This worker thread initializes data from a passed ThreadData object 
    when the thread of execution is initialized.

    WindowUpdateThread.abort can be set to false to make the thread stop
    on the next iteration.
    '''

    update = pyqtSignal(tuple)
    started = pyqtSignal(tuple)
    finished = pyqtSignal(tuple)

    def __init__(self):
        '''
        __init__(threaddata)
            initializes this object with threaddata.  the threaddata object also contains
            the action the thread is to perform.  This allows the 'thread function' to
            have access to all the data.
        '''
        super().__init__()
        self.abort = False
        self.finished = False
        self.local = None
        self.windowdata = None

    def run(self) -> None:
        if not self.local:
            self.locals()
        
        self.started.emit(self.threaddata)
        while not self.abort and not self.finished:
            time.sleep(1 / 60)
            if self.doAction():
                self.update.emit(self.windowdata)
        self.finished.emit(self.windowdata)

    def doAction(self) -> bool:
        '''
        When you inherit from this object, implement this function.  This
        is the thread.

        self.windowdata should store data the will be used to update the UI, and 
            should be set if not set.

        Return true to update the UI with whatever info you need.
        '''
        raise NotImplementedError(WindowUpdateThread.doAction.__qualname__ + ": Not implemented!")

    def locals(self) -> None:
        raise NotImplementedError(WindowUpdateThread.locals.__qualname__ + ": Not implemented!")