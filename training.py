from __future__ import annotations

import json
import os
import sys

import cv2
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QWidget

from training_gallery import GalleryWindow
from ui.ui_training import Ui_Training_qW


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TRAINING_GALLERY = os.path.join(CURRENT_FILE_PATH, 'training_gallery.py')
TRAINING_DATASET = os.path.join(CURRENT_FILE_PATH, 'resources', 'training_dataset')
STUDENT_DB = os.path.join(CURRENT_FILE_PATH, 'database', 'Student.json')

MAX_IMAGES = 5
MS_IMAGE_DELAY = 400


class TrainingWindow(QWidget, Ui_Training_qW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.button_clicked_event()
        self.start_training_cam()
        self.student_DB = self.get_database(STUDENT_DB)
        self.show()

    def init_ui(self):
        self.set_starting_position()
        self.create_dataset_folder()
        self.student_name = self.student_name_LE.text().lower().strip().replace(' ', '.')
        self.student_name_LE.editingFinished.connect(self.reset_counter)

    def button_clicked_event(self):
        self.gallery_qPB.clicked.connect(self.go_to_gallery)
        self.save_images_qPB.clicked.connect(self.validate_name)
        self.close_qPB.clicked.connect(self.cancel)

    def start_training_cam(self):
        self.training_cam = TrainingCam()
        self.training_cam.start()
        self.training_cam.ImageUpdate.connect(self.get_image)

    def go_to_gallery(self):
        self.training_galery = GalleryWindow()
        self.training_galery.show()

    def get_image(self, image):
        self.camera_qL.setPixmap(QPixmap.fromImage(image))

    def cancel(self):
        self.training_cam.stop()
        self.close()

    def set_starting_position(self):
        desktop = QDesktopWidget().availableGeometry()
        center = desktop.center()
        x = center.x() + 120
        y = center.y() - (self.height() // 2) - 50
        self.move(x, y)

    def reset_counter(self):
        self.counter = 0
        self.student_name = self.student_name_LE.text().lower().strip().replace(' ', '.')

    def create_dataset_folder(self):
        os.makedirs(TRAINING_DATASET, exist_ok=True)

    def validate_name(self):
        if not self.student_DB:
            self.message_qL.setText('O campo está vazio. Digite um nome válido.')
        elif any(char.isdigit() for char in self.student_name):
            self.message_qL.setText('O nome não pode conter números. Digite um nome válido.')
        elif not all(char.isalpha() or char.isspace() for char in self.student_name.replace('.', ' ')):
            self.message_qL.setText('O nome não pode conter caracteres especiais. Digite um nome válido.')
        else:
            self.message_qL.setText('Aluno(a) cadastrado com sucesso!')
            self.check_name_in_database()

    def get_database(self, path):
        with open(path, encoding='UTF-8') as f:
            return json.load(f)

    def check_name_in_database(self):
        data_students = self.student_DB['students']

        for student in data_students:
            if student['student_name'].lower().strip().replace(' ', '.') == self.student_name:
                self.get_student_image_count()
                self.take_picture()
                break
            else:
                self.message_qL.setText('O nome não está cadastrado no banco de dados. Digite um nome válido.')

    def get_student_image_count(self):
        filenames = os.listdir(TRAINING_DATASET)
        student_filenames = [f for f in filenames if f.startswith(self.student_name)]
        self.counter = len(student_filenames)

    def take_picture(self):
        self.saving_qPrB.setValue(0)
        self.saving_qPrB.setMaximum(MAX_IMAGES)
        self.take_picture_with_delay(0, MAX_IMAGES)

    def take_picture_with_delay(self, count, max_count):
        picture = self.camera_qL.pixmap()
        if picture is not None:
            self.save_image(picture, count)
        else:
            self.message_qL.setText('Nenhuma imagem para salvar.')

        if count + 1 < max_count:
            QTimer.singleShot(MS_IMAGE_DELAY, lambda: self.take_picture_with_delay(count + 1, max_count))
        else:
            self.message_qL.setText(f'{max_count} imagens salvas com sucesso.')
            self.saving_qPrB.reset()

    def save_image(self, picture, count):
        student_name = self.student_name.replace(' ', '.')
        filename = f'{student_name}_{self.counter + 1}.jpg'
        path_data = os.path.join(TRAINING_DATASET, filename)
        picture.save(path_data)
        self.counter += 1
        self.message_qL.setText(f'Imagem {self.counter}/{MAX_IMAGES}.')
        self.saving_qPrB.setValue(count + 1)


class TrainingCam(QThread):
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
