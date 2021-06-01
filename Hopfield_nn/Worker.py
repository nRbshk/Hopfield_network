from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal

from numpy import ndarray
from Hopfield_nn.Hopfield import Hopfield

class WorkerSignals(QObject):

    result = pyqtSignal(ndarray)


class Worker(QRunnable):

    def __init__(self, network, image_data: ndarray, iterations: int = 100, threshold: float = 0.5):
        super().__init__()
        self._network: Hopfield = network
        self._image_data: ndarray = image_data
        self.iterations: int = iterations
        self.threshold: float = threshold
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self._network.init_test_image_to_data(self._image_data)
        result = self._network.recognize(self.iterations, self.threshold)
        self.signals.result.emit(result)