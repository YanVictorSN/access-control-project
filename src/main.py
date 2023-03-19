from __future__ import annotations

import os
import re
import sys

import cv2
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
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

        self.training_cam_box = QHBoxLayout()

        self.training_cam_img = QLabel()
        self.training_cam_img.setLayout(self.training_cam_box)
        self.training_cam_img.setAlignment(Qt.AlignCenter)
        self.RealTimeCam = RealTimeCam()
        self.RealTimeCam.start()
        self.RealTimeCam.ImageUpdate.connect(self.ImageUpdateSlot)

        self.VBL.addWidget(self.training_cam_img)

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

        self.take_pictureBTN = QPushButton('Capturar')
        self.take_pictureBTN.clicked.connect(self.validate_name)
        self.VBL.addWidget(self.take_pictureBTN)

        self.CancelBTN = QPushButton('Cancelar')
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)

        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, Image):
        self.training_cam_img.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()

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

        self.RealTimeCam.stop()

        number_of_photos = 5

        for i in range(number_of_photos):
            capture = cv2.VideoCapture(0)
            ret, frame = capture.read()
            filename = f'{student_name}{i + 1}.jpg'
            path_data = os.path.join('data_photos', filename)
            cv2.imwrite(path_data, frame)

        capture.release()
        self.RealTimeCam.start()


class RealTimeCam(QThread):
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
                    FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888,
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
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
