from PyQt6 import QtWidgets
from PyQt6.QtCore import QThreadPool
from Gui.Paint_widget import PaintWidget

from Hopfield_nn.Hopfield import Worker

class MainWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle("Main Widget")
        # get threads
        self.threadpool = QThreadPool()

        # canvas for user image
        self.user_canvas = PaintWidget(self, parent.width() // 2, parent.height()//2, False)
        # canvas for resulted image
        self.resulted_canvas = PaintWidget(self,parent.width() // 2, parent.height()//2, True)


        # buttons
        self.clear_button = QtWidgets.QPushButton('Clear')
        self.save_button = QtWidgets.QPushButton('Save')
        self.train_button = QtWidgets.QPushButton('Train')
        self.recognize_button = QtWidgets.QPushButton('Recognize')

        self.clear_button.clicked.connect(lambda: self.user_canvas.clear())
        self.save_button.clicked.connect(lambda: self.user_canvas.save_pixmap_data())
        self.train_button.clicked.connect(lambda: print('train'))
        self.recognize_button.clicked.connect(lambda: self.recognize())


        # buttons layout
        vboxlayout = QtWidgets.QVBoxLayout()

        vboxlayout.addWidget(self.clear_button)
        vboxlayout.addWidget(QtWidgets.QLabel(""))
        vboxlayout.addWidget(self.save_button)
        vboxlayout.addWidget(QtWidgets.QLabel(""))
        vboxlayout.addWidget(self.train_button)
        vboxlayout.addWidget(QtWidgets.QLabel(""))
        vboxlayout.addWidget(self.recognize_button)

        # layout
        layout = QtWidgets.QGridLayout(self)


        layout.addWidget(self.user_canvas, 0, 0, 5, 1)
        layout.addWidget(self.resulted_canvas, 0, 2, 5, 1)
        layout.addLayout(vboxlayout, 0, 1)

        
        self.setLayout(layout)



        del vboxlayout
        del layout


    def recognize(self):
        if self.threadpool.activeThreadCount() > 0:
            print('Wait until process end.')
            return None

        worker = Worker(self.user_canvas.get_pixmap_data())
        self.threadpool.start(worker)




    

        



