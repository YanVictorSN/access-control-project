from __future__ import annotations

import os
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


class TrainingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi('ui/training.ui', self)
        self.counter = 0
        self.current_name = ''

        self.student_name_LE.editingFinished.connect(self.reset_counter)

        self.cancel_QPB.clicked.connect(self.CancelFeed)
        self.save_image_QPB.clicked.connect(self.validate_name)

        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.show()

    def ImageUpdateSlot(self, Image):
        self.camera_QL.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()

    def setPosition(self):
        desktop = QDesktopWidget().availableGeometry()
        center = desktop.center()
        x = center.x() + 120
        y = center.y() - (self.height() // 2) - 50
        self.move(x, y)

    def reset_counter(self):
        self.counter = 0
        self.current_name = self.student_name_LE.text()

    def create_folder_if_not_exists(self):
        if not os.path.exists('training_dataset'):
            os.makedirs('training_dataset', exist_ok=True)

    def validate_name(self):
        student_name = self.student_name_LE.text()
        if not student_name:
            self.message_QL.setText(
                'O campo está vazio. Digite um nome válido.')
        elif any(char.isdigit() for char in student_name):
            self.message_QL.setText(
                'O nome não pode conter números. Digite um nome válido.')
        elif not all(char.isalpha() or char.isspace() for char in student_name):
            self.message_QL.setText(
                'O nome não pode conter caracteres especiais. Digite um nome válido.')
        else:
            self.message_QL.setText('Aluno(a) cadastrado com sucesso!')
            self.take_pictures(student_name)

    def take_pictures(self, student_name):
        picture = self.camera_QL.pixmap()
        if picture is not None:
            student_name = self.student_name_LE.text()
            if student_name != self.current_name:
                self.counter = 0
                self.current_name = student_name
            self.counter += 1
            filename = f'{student_name}_{self.counter}.jpg'
            folder_path = 'training_dataset'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            path_data = os.path.join(folder_path, filename)
            picture.save(path_data)
            self.message_QL.setText(
                f'Imagem {self.counter} salva com sucesso para {student_name}.')
        else:
            self.message_QL.setText('Nenhuma imagem para salvar.')


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
