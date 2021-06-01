from time import sleep
from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal
import numpy as np


class WorkerSignals(QObject):

    result = pyqtSignal(np.ndarray)


class Worker(QRunnable):

    def __init__(self, network, image_data: np.ndarray, iterations: int = 100, threshold: float = 0.5):
        super().__init__()
        self._network: Hopfield = network
        self._image_data: np.ndarray = image_data
        self.iterations: int = iterations
        self.threshold: float = threshold
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self._network.init_test_image_to_data(self._image_data)
        result = self._network.recognize(self.iterations, self.threshold)
        self.signals.result.emit(result)
        


class Hopfield:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self._train_vector: np.ndarray = np.zeros((0))
        self.weights: np.ndarray = np.zeros((self.width * self.height, self.height * self.height), dtype=np.int8)
        self.iter: int = 0
        self.end: bool = False

    @property
    def train_vector(self):
        return self._train_vector

    @train_vector.setter
    def train_vector(self, vector):
        self._train_vector = vector
        self._train_len = vector.shape[0]

    def train_weights(self) -> None:
        self.iter += 1
        vector_full = np.tile(self._train_vector, (self._train_len, 1))
        w = vector_full * vector_full.T
        i_0 = 1 - np.identity(self._train_len)
        self.weights = (self.weights + w * i_0)

        del vector_full, w, i_0

    def init_test_image_to_data(self, image: np.ndarray) -> None:
        self.image = image
        self.data = np.zeros((self.width, self.height), dtype=np.int8)
        self.data = np.where(image > 0, 1, 0)

    def recognize(self, times=50, theta=0.5) -> np.ndarray:
        self.end = False
        flatten_image = self.image.flatten()

        for _ in range(times):
            update_number = np.random.randint(0, self._train_len)
            u = np.dot(self.weights[update_number][:], flatten_image) - theta
            if u > 0:
                flatten_image[update_number] = 1
            else:
                flatten_image[update_number] = -1
            
            if self.end:
                break



                
        new_data = np.zeros(flatten_image.shape)
        new_data[flatten_image == 1] = 255
        new_data[flatten_image == -1] = 0

        return new_data.reshape((self.width, self.height))


    def reset_weights(self):
        self.weights = np.zeros((self.width * self.height, self.height * self.height), dtype=np.int8)
