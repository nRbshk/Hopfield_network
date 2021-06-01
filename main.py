import sys

from PyQt6.QtWidgets import QApplication
from Gui.Main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow(1280, 720)
    
    window.move(0, 0)

    window.show()

    app.exec()
