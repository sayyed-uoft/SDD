from PyQt5.QtWidgets import QApplication

from camera import Camera
from network import Yolo3
from view import StartWindow
import cv2

# Initiliaze camera
print("Initialize Camera ...")
camera = Camera('example2.mp4')
camera.initialize()

# Initialize network
print("Initialize Network ...")
net = Yolo3()
net.initialize("yolo3/")

# Start the application
print("Start Application ...")
app = QApplication([])
start_window = StartWindow(camera, net)
start_window.show()
app.exit(app.exec_())
