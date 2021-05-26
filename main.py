import sys
from Gui.gui import MainWindow, QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow(1280, 720)

    window.show()

    
    app.exec()