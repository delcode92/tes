import sys
import cv2
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout


class DisplayWidget(QWidget):
    def __init__(self, parent=None):
        super(DisplayWidget, self).__init__(parent)
        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

    def set_image(self, image):
        self.image_label.setPixmap(QPixmap.fromImage(image))


class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.setWindowTitle("IP Camera Video Player")

        self.stream_url_1 = "rtsp://admin:admin@192.168.100.121"
        self.stream_url_2 = "rtsp://admin:admin@192.168.100.121"

        self.display_widget_1 = DisplayWidget()
        self.display_widget_2 = DisplayWidget()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.display_widget_1)
        self.layout.addWidget(self.display_widget_2)
        self.setLayout(self.layout)

        self.cap_1 = cv2.VideoCapture(self.stream_url_1)
        self.cap_2 = cv2.VideoCapture(self.stream_url_2)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play)
        self.timer.start(30)

    def play(self):
        ret_1, frame_1 = self.cap_1.read()
        ret_2, frame_2 = self.cap_2.read()

        if ret_1:
            frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)
            image_1 = QImage(frame_1, frame_1.shape[1], frame_1.shape[0], frame_1.strides[0], QImage.Format_RGB888)
            self.display_widget_1.set_image(image_1)

        if ret_2:
            frame_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2RGB)
            image_2 = QImage(frame_2, frame_2.shape[1], frame_2.shape[0], frame_2.strides[0], QImage.Format_RGB888)
            self.display_widget_2.set_image(image_2)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
