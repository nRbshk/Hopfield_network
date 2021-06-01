from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6.QtCore import QThreadPool
from Gui.Paint_widget import PaintWidget

from Hopfield_nn.Hopfield import Hopfield
from Hopfield_nn.Worker import Worker

class MainWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle("Main Widget")
        # get threads
        self.threadpool = QThreadPool()
        
        # canvas for user image
        self.user_canvas = PaintWidget(self, parent.height(), parent.height(), False)
        # canvas for resulted image
        self.resulted_canvas = PaintWidget(self,parent.height(), parent.height(), True)

        # network
        self.hopfield = Hopfield(self.user_canvas.grid_points, self.user_canvas.grid_points)

        # buttons
        self.clear_button = QtWidgets.QPushButton('Clear')
        self.reset_network_button = QtWidgets.QPushButton('Reset')
        self.train_button = QtWidgets.QPushButton('Train')
        self.recognize_button = QtWidgets.QPushButton('Recognize')

        self.clear_button.clicked.connect(lambda: self.clear())
        self.reset_network_button.clicked.connect(lambda: self.hopfield.reset_weights())
        self.train_button.clicked.connect(lambda: self.train())
        self.recognize_button.clicked.connect(lambda: self.recognize())


        # iteration text form
        self.form_iter = QtWidgets.QLineEdit(self)
        # threshold text form
        self.form_threshold = QtWidgets.QLineEdit(self)

        # buttons layout
        vboxlayout = QtWidgets.QVBoxLayout()

        vboxlayout.addWidget(self.clear_button)
        vboxlayout.addWidget(QtWidgets.QLabel(""))
        vboxlayout.addWidget(self.reset_network_button)
        vboxlayout.addWidget(QtWidgets.QLabel(""))
        vboxlayout.addWidget(self.train_button)
        vboxlayout.addWidget(QtWidgets.QLabel(""))
        vboxlayout.addWidget(self.recognize_button)
        vboxlayout.addWidget(QtWidgets.QLabel("Number of iterations:"))
        vboxlayout.addWidget(self.form_iter)
        vboxlayout.addWidget(QtWidgets.QLabel("Threshold:"))
        vboxlayout.addWidget(self.form_threshold)

        # layout
        layout = QtWidgets.QGridLayout(self)

        layout.addWidget(QtWidgets.QLabel("Draw some symbol in the area below."), 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QtWidgets.QLabel("This is an output for recognized image."), 0, 2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.user_canvas, 1, 0, 5, 1)
        layout.addWidget(self.resulted_canvas, 1, 2, 5, 1)
        layout.addLayout(vboxlayout, 1, 1)

        
        self.setLayout(layout)



        del vboxlayout
        del layout

    def train(self):

        self.hopfield.train_vector = self.user_canvas.get_pixmap_data().flatten()
        self.threadpool.start(self.hopfield.train_weights)


    def recognize(self):
        if self.threadpool.activeThreadCount() > 0:
            print('Wait until process end.')
            return None
        
        iterations = 100 if self.form_iter.text() == ""  else int(self.form_iter.text())
        threshold = 0.5 if self.form_threshold.text() == "" else float(self.form_threshold.text())

        worker = Worker(self.hopfield, self.user_canvas.get_pixmap_data(), iterations, threshold)
        worker.signals.result.connect(self.show_recognized_image)

        self.threadpool.start(worker)

    def show_recognized_image(self, image):
        self.resulted_canvas.clear()
        self.resulted_canvas.set_pixmap_data(image)

    def clear(self):
        self.user_canvas.clear()
        self.resulted_canvas.clear()


    

        



