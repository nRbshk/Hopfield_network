from time import sleep
from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal
import numpy as np


class WorkerSignals(QObject):

    result = pyqtSignal(np.ndarray)


class Worker(QRunnable):

    def __init__(self, network, image_data):
        super().__init__()
        self._network: Hopfield = network
        self._image_data: np.ndarray = image_data
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self._network.init_test_image_to_data(self._image_data)
        result = self._network.recognize(10, 0.5)
        self.signals.result.emit(result)


class Hopfield:
    def __init__(self, width: int, height: int, load=False):
        if load:
            self.load_from_json()
        else:
            self.width = width
            self.height = height
            self._train_vector = np.zeros((0))
            self.weights = np.zeros((self.width * self.height, self.height * self.height))
            self.iter = 0

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
        # self.weights = (self.weights + w * i_0) / self.iter
        self.weights = (self.weights + w * i_0)

        del vector_full, w, i_0

    def init_test_image_to_data(self, image: np.ndarray) -> None:
        self.image = image
        self.data = np.zeros((self.width, self.height), dtype=np.int8)
        self.data = np.where(image > 0, 1, 0)

    def recognize(self, times=1000, theta=0.5) -> np.ndarray:
        flatten_image = self.image.flatten()

        for _ in range(times):
            update_number = np.random.randint(0, self._train_len - 1)
            u = np.dot(self.weights[update_number][:], flatten_image) - theta
            if u > 0:
                flatten_image[update_number] = 1
            else:
                flatten_image[update_number] = -1
                
        new_data = np.zeros(flatten_image.shape)
        new_data[flatten_image == 1] = 255
        new_data[flatten_image == -1] = 0

        return new_data.reshape((self.width, self.height))

    def load_from_json(self):
        pass
