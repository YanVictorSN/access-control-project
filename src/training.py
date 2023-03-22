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
        self.init_ui()
        self.button_clicked_event()
        self.set_worker()
        self.show()

    def init_ui(self):
        self.set_starting_position()
        self.create_dataset_folder()
        self.student_name = ''
        self.student_name_LE.editingFinished.connect(self.reset_counter)

    def button_clicked_event(self):
        self.gallery_QPB.clicked.connect(self.go_to_gallery)
        self.save_image_QPB.clicked.connect(self.validate_name)
        self.cancel_QPB.clicked.connect(self.cancel)

    def set_worker(self):
        self.worker = Worker()
        self.worker.start()
        self.worker.ImageUpdate.connect(self.get_image)

    def go_to_gallery(self):
        subprocess.Popen(['python', TRAINING_GALLERY, f'{self.student_name}'])

    def get_image(self, image):
        self.camera_QL.setPixmap(QPixmap.fromImage(image))

    def cancel(self):
        self.worker.stop()

    def set_starting_position(self):
        desktop = QDesktopWidget().availableGeometry()
        center = desktop.center()
        x = center.x() + 120
        y = center.y() - (self.height() // 2) - 50
        self.move(x, y)

    def reset_counter(self):
        self.counter = 0
        self.student_name = self.student_name_LE.text().lower().strip()

    def create_dataset_folder(self):
        os.makedirs(DATASET_FOLDER, exist_ok=True)

    def validate_name(self):
        if not self.student_name:
            self.message_QL.setText('O campo está vazio. Digite um nome válido.')
        elif any(char.isdigit() for char in self.student_name):
            self.message_QL.setText('O nome não pode conter números. Digite um nome válido.')
        elif not all(char.isalpha() or char.isspace() for char in self.student_name):
            self.message_QL.setText('O nome não pode conter caracteres especiais. Digite um nome válido.')
        else:
            self.message_QL.setText('Aluno(a) cadastrado com sucesso!')
            self.get_student_image_count()
            self.take_picture()

    def get_student_image_count(self):
        filenames = os.listdir(DATASET_FOLDER)
        student_filenames = [f for f in filenames if f.startswith(self.student_name)]
        self.counter = len(student_filenames)

    def take_picture(self):
        picture = self.camera_QL.pixmap()
        if picture is not None:
            filename = f'{self.student_name}_{self.counter + 1}.jpg'
            path_data = os.path.join(DATASET_FOLDER, filename)
            picture.save(path_data)
            self.counter += 1
            self.message_QL.setText(f'Imagem {self.counter} salva com sucesso para {self.student_name}.')
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
