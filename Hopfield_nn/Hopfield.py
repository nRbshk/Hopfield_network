from time import sleep
from PyQt6.QtCore import QRunnable, pyqtSlot

class Worker(QRunnable):

    def __init__(self, image_data):
        super().__init__()
        self.image_data = image_data

    @pyqtSlot()
    def run(self):
        print(self.image_data)
        sleep(5)
        # self.parent_widget.update_status_bar_message("Succes recognize image.")

class Hopfield:

    def __init__(self, load=False):
        if load:
            pass
        else:
            pass

