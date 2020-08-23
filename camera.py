import numpy as np

import cv2


class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.last_frame = np.zeros((1,1))

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)

    def get_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            self.last_frame = self.get_frame()
            movie.append(self.last_frame)
        return movie

    def detect_in_movie(self, num_frames, net):
        for _ in range(num_frames):
            self.last_frame = net.detect_people(self.get_frame())

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def close_camera(self):
        self.cap.release()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)


if __name__ == '__main__':
    cam = Camera(0)
    cam.initialize()
    print(cam)
    frame = cam.get_frame()
    print(frame)
    cam.set_brightness(1)
    print(cam.get_brightness())
    cam.set_brightness(0.5)
    print(cam.get_brightness())
    cam.close_camera()
