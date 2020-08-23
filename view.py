import numpy as np

from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QApplication, QLabel
from pyqtgraph import ImageView, PlotWidget, GraphicsView, ImageItem


class StartWindow(QMainWindow):
    def __init__(self, camera = None, net = None):
        super().__init__()
        self.camera = camera
        self.net = net

        self.setFixedWidth(1145)
        self.setFixedHeight(800)
        
        self.central_widget = QWidget(self)

        self.label_logo = QLabel(self.central_widget)
        logo = QPixmap("logo.png")
        self.label_logo.setPixmap(logo)
        self.label_logo.setGeometry(20,20,181,81)
        self.label_logo.setScaledContents(True)
        
        self.button_config = QPushButton('Configuration', self.central_widget)
        self.button_config.setGeometry(240,30,191,61)
        font = QFont()
        font.setPointSize(24)
        self.button_config.setFont(font)
        self.button_config.clicked.connect(self.update_image)
        
        self.button_detection = QPushButton('Start Detection', self.central_widget)
        self.button_detection.setGeometry(450,30,191,61)
        font = QFont()
        font.setPointSize(24)
        self.button_detection.setFont(font)
        self.button_detection.clicked.connect(self.start_movie)

        #self.label_image = QLabel(self.central_widget)
        self.image_view = GraphicsView(self.central_widget)
        self.image_view.setGeometry(40,110,1067,600)
        #self.image_view.hideAxis('left')
        #self.image_view.hideAxis('bottom')
        self.image_view.setStyleSheet("border :1px solid black;")
        #self.label_image.setGeometry(40,110,1067,600)
        #self.label_image.setScaledContents(True)
        #self.label_image.setStyleSheet("border :1px solid black;")

        self.setCentralWidget(self.central_widget)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_movie)

    def update_image(self):
        frame = self.camera.get_frame()
        #self.image_view.setImage(frame.T)
        image_item = ImageItem(frame)
        self.image_view.addItem(image_item)
        #height, width, channel = frame.shape
        #bytesPerLine = 3 * width
        #qimg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        #self.label_image.setPixmap(QPixmap(qimg))
        #self.update()
        #print(height, width)

        
    def update_movie(self):
        image_item = ImageItem(self.camera.last_frame)
        self.image_view.addItem(image_item)
        #self.image_view.setImage(self.camera.last_frame.T)

    def update_brightness(self, value):
        value /= 10
        self.camera.set_brightness(value)

    def start_movie(self):
        self.movie_thread = MovieThread(self.camera, self.net)
        self.movie_thread.start()
        self.update_timer.start(30)


class MovieThread(QThread):
    def __init__(self, camera, net):
        super().__init__()
        self.camera = camera
        self.net = net

    def run(self):
        #self.camera.acquire_movie(500)
        self.camera.detect_in_movie(500,self.net)

if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())
