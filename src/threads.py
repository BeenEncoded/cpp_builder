import threading, time, logging

logger = logging.getLogger(__name__)

class Worker(threading.Thread):
    '''
    An arbitrary worker thread.
    '''
    def __init__(self, functor):
        '''
        functor: the function to execute on each iteration.  Takes no arguments.

        If the functor is None, Worker.doWork will be the function used for implimentation,
        allowing for polymorphic implimentation much like threading.Thread, where doWork is the
        implemented function instead of run.
        '''
        super(Worker, self).__init__()
        self.throttle = 30 #iterates 30 times per second
        self._running = False #True when the thread is running
        self._stopthread = False #True when the caller wants the thread to stop
        self._functor = functor
    
    def halt_thread(self) -> None:
        '''
        Stops this worker thread.
        '''
        if not self.isAlive():
            return
        self._stopthread = True
        self.join()
        if self._running:
            raise RuntimeError("Failed to stop thread")
    
    def doWork(self) -> None:
        raise NotImplementedError(Worker.doWork.__qualname__ + ": Not implemented.")

    def tryLog(self, message) -> bool:
        try:
            logger.debug(message)
            return True
        except:
            return False

    def run(self):
        self._running = True
        while(not self._stopthread):
            if self._functor is not None:
                self._functor()
            else:
                self.doWork()
            time.sleep(1 / self.throttle)
        self._running = False