from pylint import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic
from events import Events
import traceback, sys

class WorkerSignals(QObject):                                               # container for multiple worker signals, only one is used here
    message = pyqtSignal(str)                                               # the signal to send when a message is received

class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):                                # __init__ medthod gets called on creation of this class
        super(Worker, self).__init__()

        self.fn = fn                                                        # Store constructor arguments (re-used for processing)
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['progress_callback'] = self.signals.message             # Add the callback to our kwargs

    @pyqtSlot()
    def run(self):                                                          # run the given Function fn
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]