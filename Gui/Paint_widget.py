from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QPainter, QPen, QPixmap, QMouseEvent, QImage
from numpy import frombuffer, asarray, ubyte

import os

train_dir = 'train_images'
train_path = os.path.abspath(train_dir)


class PaintWidget(QtWidgets.QWidget):

    def __init__(self, parent, w: int, h: int, locked_user_paint: bool = False):
        super().__init__(parent)
        self.main_widget = parent
        
        self.locked_user_paint = locked_user_paint
        self.pixmap = QPixmap(w, h)


        self.label = QtWidgets.QLabel(self)

        self.clear()

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.locked_user_paint: 
            return
        x, y = int(e.position().x()), int(e.position().y())
        if self.pixmap.rect().contains(x, y):
           painter = QPainter(self.pixmap)
           pen = QPen()
           pen.setWidth(20)
           painter.setPen(pen)
           painter.drawPoint(x, y)
           painter.end()
           self.label.setPixmap(self.pixmap)
           

    def clear(self):
        self.pixmap.fill(QColor(255, 255, 255, 255))
        self.label.setPixmap(self.pixmap)

    def get_pixmap_data(self):
        image = self.pixmap.toImage().convertToFormat(QImage.Format.Format_Grayscale8)
        
        ptr = image.bits()
        ptr.setsize(image.sizeInBytes())
        str_data = ptr.asstring()

        arr = asarray(frombuffer(str_data, dtype=ubyte).reshape(image.height(), image.width(), ))
        return arr


    def save_pixmap_data(self):
        last_id = len(os.listdir(train_path))
        self.pixmap.save(f"{train_path}/{last_id}.png", None, 100)

        



        