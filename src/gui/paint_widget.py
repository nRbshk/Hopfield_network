from PyQt6 import QtWidgets
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QColor, QPen, QPixmap, QMouseEvent, QImage
from numpy import zeros



class PaintWidget(QtWidgets.QWidget):

    def __init__(self, parent, w: int, h: int, lock_user_paint=False):
        super().__init__()
        self.main_widget = parent


        self.lock_user_paint = lock_user_paint
        self.grid_points = 10

        self.pixmaps, self.labels = self._init_canvas(w, h)

        self.grid_layout = QtWidgets.QGridLayout(self)

        for i in range(self.grid_points):
            for j in range(self.grid_points):
                self.grid_layout.addWidget(self.labels[i][j], i, j)

        self.grid_layout.setSpacing(1)
        self.setLayout(self.grid_layout)

        self.pen = QPen()
        self.pen.setWidth(w // self.grid_points * 2)


    def _init_canvas(self, w: int, h: int):
        pixmaps: list[list[QPixmap]] = []
        labels: list[list[QtWidgets.QLabel]] = [] 

        self.pixmap_width: int = w // self.grid_points
        self.pixmap_height: int = h // self.grid_points

        for i in range(self.grid_points):
            temp_labels: list[QtWidgets.QLabel] = []
            temp_pixmaps: list[QPixmap] = []
            for j in range(self.grid_points):
                pixmap = QPixmap(self.pixmap_width, self.pixmap_height)
                pixmap.fill(QColor(255, 255, 255, 255))
                
                label = QtWidgets.QLabel()
                label.setPixmap(pixmap)

                temp_pixmaps.append(pixmap)
                temp_labels.append(label)

            pixmaps.append(temp_pixmaps)
            labels.append(temp_labels)

        return [pixmaps, labels]

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.lock_user_paint:
            return None
        x, y = int(e.position().x()), int(e.position().y())
        index_of_pixmap = self._get_index_of_pixmap_rectangle(x, y)
        if index_of_pixmap is None:
            return None
        pixmap = self.pixmaps[index_of_pixmap[0]][index_of_pixmap[1]]
        pixmap.fill(QColor(0, 0, 0, 255))
        label = self.labels[index_of_pixmap[0]][index_of_pixmap[1]]
        label.setPixmap(pixmap)

    def _get_index_of_pixmap_rectangle(self, x: int, y: int):
        for i in range(self.grid_points):
            for j in range(self.grid_points):
                if self.grid_layout.cellRect(i, j).contains(x, y):
                    return i, j
        return None

    def clear(self):
        for i in range(self.grid_points):
            for j in range(self.grid_points):
                self.pixmaps[i][j].fill(QColor(255, 255, 255, 255))
                self.labels[i][j].setPixmap(self.pixmaps[i][j])
    
    def get_pixmap_data(self):
        arr = zeros((self.grid_points, self.grid_points))
        middle_point = QPoint(self.pixmap_width // 2, self.pixmap_height // 2)
        for i in range(self.grid_points):
            row = zeros((self.grid_points))
            for j in range(self.grid_points):
                image = self.pixmaps[i][j].toImage().convertToFormat(QImage.Format.Format_Grayscale8)
                row[j] = 1 if QColor(image.pixel(middle_point)).red() == 0 else -1
            arr[i] = row
        return arr

    def set_pixmap_data(self, data):
        if not self.lock_user_paint:
            return None
        for i in range(self.grid_points):
            for j in range(self.grid_points):
                if data[i][j] > 0:
                    self.pixmaps[i][j].fill(QColor(0, 0, 0, 255))
                else:
                    self.pixmaps[i][j].fill(QColor(255, 255, 255, 255))
                self.labels[i][j].setPixmap(self.pixmaps[i][j])
    


        
