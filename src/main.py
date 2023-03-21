from __future__ import annotations

import os
import re
import sys

import cv2
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.VBL = QVBoxLayout()

        self.setWindowTitle('Treinamento')

        self.title_training = QLabel('Treinamento', self)
        self.title_training.setGeometry(50, 50, 200, 50)
        self.title_training.setStyleSheet(
            'font-size: 16pt; font-family: Robot;',
        )
        self.title_training.setAlignment(Qt.AlignCenter)
        self.VBL.addWidget(self.title_training)

        self.box_input = QHBoxLayout()
        self.label_input = QLabel('Nome do aluno(a):', self)
        self.line_edit = QLineEdit(self)
        self.box_input.addWidget(self.label_input)
        self.box_input.addWidget(self.line_edit)
        self.VBL.addLayout(self.box_input)

        self.msg_error = QLabel()
        self.msg_error.move(50, 100)
        self.msg_error.resize(200, 20)
        self.VBL.addWidget(self.msg_error)

        self.training_cam_img = QLabel()
        self.training_cam_img.setGeometry(0, 0, 640, 480)
        self.VBL.addWidget(self.training_cam_img)
        self.training_cam_img.setAlignment(Qt.AlignCenter)

        self.init_trainingBTN = QPushButton('Iniciar Treinamento')
        self.init_trainingBTN.clicked.connect(self.start_training_video)
        self.VBL.addWidget(self.init_trainingBTN)

        self.take_pictureBTN = QPushButton('Capturar Imagem')
        self.take_pictureBTN.clicked.connect(self.validate_name)
        self.VBL.addWidget(self.take_pictureBTN)

        self.stop_trainingBTN = QPushButton('Parar Treinamento')
        self.stop_trainingBTN.clicked.connect(self.stop_training_video)
        self.VBL.addWidget(self.stop_trainingBTN)

        self.setLayout(self.VBL)

    def start_training_video(self):
        self.RealTimeCam = RealTimeCam()
        self.RealTimeCam.start()
        self.RealTimeCam.ImageUpdate.connect(self.image_update)

    def image_update(self, image):
        self.training_cam_img.setPixmap(QPixmap.fromImage(image))

    def stop_training_video(self):
        self.RealTimeCam.stop()

    def validate_name(self):
        try:
            student_name = self.line_edit.text()
            default_name_regx = re.findall('[^a-zA-Z]', student_name)
            if not student_name:
                raise Exception('O campo está vazio, digite um nome válido.')
            elif student_name.isnumeric() is True:
                raise Exception(
                    'Não aceitamos números, digite um nome válido.',
                )
            elif default_name_regx:
                raise Exception(
                    'Não aceitamos caracteres especiais, digite um nome válido.',
                )
        except Exception as e:
            self.msg_error.setText(str(e))
        else:
            self.msg_error.setText('Aluno(a) cadastrado com sucesso!')
            self.take_pictures(student_name)

    def take_pictures(self, student_name):

        picture = self.training_cam_img.pixmap()
        if picture is not None:
            filename = f'{student_name}.jpg'
            path_data = os.path.join('data_photos', filename)
            picture.save(path_data)


class RealTimeCam(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        capture_cam = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = capture_cam.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(
                    FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888,
                )
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        capture_cam.release()

    def stop(self):
        self.ThreadActive = False
        self.quit()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
