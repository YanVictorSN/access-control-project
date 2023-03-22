from __future__ import annotations

import os
import subprocess
import sys

import cv2
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QWidget

UI_PATH = 'ui/training.ui'
TRAINING_GALLERY = 'training_gallery.py'
DATASET_FOLDER = 'training_dataset'


class TrainingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.initUI()
        self.buttonClickedEvent()
        self.setWorker()
        self.show()

    def initUI(self):
        self.setStartingPosition()
        self.createDatasetFolder()
        self.counter = 0
        self.student_name = self.student_name_LE.text().lower().strip()
        self.student_name_LE.editingFinished.connect(self.resetCounter)

    def buttonClickedEvent(self):
        self.gallery_QPB.clicked.connect(self.goToGallery)
        self.save_image_QPB.clicked.connect(self.validateName)
        self.cancel_QPB.clicked.connect(self.cancel)

    def setWorker(self):
        self.Worker1 = Worker()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.getImage)

    def goToGallery(self):
        subprocess.Popen(['python', TRAINING_GALLERY, f'{self.student_name}'])

    def getImage(self, Image):
        self.camera_QL.setPixmap(QPixmap.fromImage(Image))

    def cancel(self):
        self.Worker1.stop()

    def setStartingPosition(self):
        desktop = QDesktopWidget().availableGeometry()
        center = desktop.center()
        x = center.x() + 120
        y = center.y() - (self.height() // 2) - 50
        self.move(x, y)

    def resetCounter(self):
        self.counter = 0
        self.student_name = self.student_name_LE.text()

    def createDatasetFolder(self):
        if not os.path.exists(DATASET_FOLDER):
            os.makedirs(DATASET_FOLDER, exist_ok=True)

    def validateName(self):
        if not self.student_name:
            self.message_QL.setText(
                'O campo está vazio. Digite um nome válido.')
        elif any(char.isdigit() for char in self.student_name):
            self.message_QL.setText(
                'O nome não pode conter números. Digite um nome válido.')
        elif not all(char.isalpha() or char.isspace() for char in self.student_name):
            self.message_QL.setText(
                'O nome não pode conter caracteres especiais. Digite um nome válido.')
        else:
            self.message_QL.setText('Aluno(a) cadastrado com sucesso!')
            self.takePicture()

    def takePicture(self):
        Picture = self.camera_QL.pixmap()
        if Picture is not None:
            self.student_name = self.student_name_LE.text()
            if self.student_name != self.student_name:
                self.counter = 0
                self.student_name = self.student_name
            self.counter += 1
            filename = f'{self.student_name}_{self.counter}.jpg'
            if not os.path.exists(DATASET_FOLDER):
                os.makedirs(DATASET_FOLDER)
            path_data = os.path.join(DATASET_FOLDER, filename)
            Picture.save(path_data)
            self.message_QL.setText(
                f'Imagem {self.counter} salva com sucesso para {self.student_name}.')
        else:
            self.message_QL.setText('Nenhuma imagem para salvar.')


class Worker(QThread):
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
        self.wait()
        self.quit()


if __name__ == '__main__':
    App = QApplication([])
    Home = TrainingWindow()
    sys.exit(App.exec())
