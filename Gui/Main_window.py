from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import  QGridLayout, QMainWindow, QLabel
from PyQt6.QtGui import QColor, QMouseEvent, QPainter, QPixmap, QPen

from Gui.Main_widget import MainWidget

class MainWindow(QMainWindow):

    def __init__(self, w: int = 1280, h: int = 720):
        super().__init__()

        self.setWindowTitle("Hopfield network")
        self.resize(w, h)
        
        self.main_widget = MainWidget(self)

        self.setCentralWidget(self.main_widget)

        self.main_widget.show()


