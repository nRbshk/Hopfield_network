from PyQt6.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):

    def __init__(self, w: int = 12800, h: int = 720):
        super().__init__()

        self.setWindowTitle("Hopfield network")
        self.resize(w, h)

    def __setup_ui(self) -> None:
        self.__setup_draw_window()
        pass

    def __setup_draw_window(self) -> None:
        pass

