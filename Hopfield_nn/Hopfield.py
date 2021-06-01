import numpy as np


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
        self.flatten_image = image.flatten()

    def update(self, vector, threshold=0.5, synchronous = False) -> np.ndarray:
        if synchronous:
            return vector
        else:
            update_number = np.random.randint(0, self._train_len)
            u = np.dot(self.weights[update_number][:], vector) - threshold
            if u > 0:
                vector[update_number] = 1
            else:
                vector[update_number] = -1
            return vector

    def recognize(self, iterations=50, threshold=0.5, synchronous=False) -> np.ndarray:
        self.end = False

        for _ in range(iterations):
            self.flatten_image = self.update(self.flatten_image, threshold, synchronous)

            if self.end:
                break

        return np.where(self.flatten_image == 1, 255, 0).reshape((self.width, self.height))


    def reset_weights(self):
        self.weights = np.zeros((self.width * self.height, self.height * self.height), dtype=np.int8)
