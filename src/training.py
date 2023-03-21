from __future__ import annotations

import sys

import cv2
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


class TrainingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi('ui/training.ui', self)

        self.cancel_QPB.clicked.connect(self.CancelFeed)

        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.show()

    def ImageUpdateSlot(self, Image):
        self.camera_QL.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(
                    FlippedImage.data,
                    FlippedImage.shape[1],
                    FlippedImage.shape[0],
                    QImage.Format_RGB888
                )
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        Capture.release()

    def stop(self):
        self.ThreadActive = False
        self.wait()  # Wait for the thread to finish
        self.quit()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = TrainingWindow()
    sys.exit(App.exec())
