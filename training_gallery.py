from __future__ import annotations

import os
import pickle
import sys

import cv2
import face_recognition
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

from ui.ui_training_gallery import Ui_Images_qW

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TRAINING_DATASET = os.path.join(
    CURRENT_FILE_PATH, 'resources', 'training_dataset')
EXTRACTED_DATASET = os.path.join(
    CURRENT_FILE_PATH, 'resources', 'extracted_dataset')
FACES_DAT = os.path.join(CURRENT_FILE_PATH, 'resources', 'faces.dat')
ATTENDANCE = os.path.join(CURRENT_FILE_PATH, 'attendance')

MAX_COLUMNS = 3


class GalleryWindow(QWidget, Ui_Images_qW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.CURRENT_FILE_PATH = CURRENT_FILE_PATH
        self.TRAINING_DATASET = TRAINING_DATASET
        self.EXTRACTED_DATASET = EXTRACTED_DATASET
        self.FACES_DAT = FACES_DAT
        self.ATTENDANCE = ATTENDANCE
        self.setupUi(self)
        self.init_ui()
        self.setup_button_events()
        self.get_images()
        self.add_images_to_grid()
        self.show()

    def init_ui(self):
        self.student_name = sys.argv[1] if len(sys.argv) > 1 else ''
        self.base_directory = os.path.abspath(os.path.dirname(__file__))
        self.image_directory = os.path.join(
            self.base_directory, self.TRAINING_DATASET)
        self.images = []
        self.MAX_COLUMNS = 3

    def setup_button_events(self):
        self.train_qPB.clicked.connect(self.train_model)
        self.delete_image_qPB.clicked.connect(self.delete_image)
        self.close_qPB.clicked.connect(self.close)

    def get_images(self):
        self.image_files = os.listdir(self.image_directory)
        for filename in self.image_files:
            if self.student_name in filename:
                image_path = os.path.join(self.image_directory, filename)
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    self.images.append((filename, pixmap))

    def add_images_to_grid(self):
        for i, (filename, pixmap) in enumerate(self.images):
            row = i // self.MAX_COLUMNS
            col = i % self.MAX_COLUMNS
            image_label = QLabel(self)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setPixmap(pixmap.scaledToWidth(200))
            self.Gallery_qGL.addWidget(image_label, row, col)

    def delete_image(self):
        selected_label = self.get_selected_label()
        if selected_label is not None:
            filename = selected_label.property(
                'filename') or self.images[selected_label.index][0]
            print(filename)
            print(self.images)
            os.remove(os.path.join(self.image_directory, filename))
            self.images.pop([selected_label.index][0])
            self.Gallery_qGL.removeWidget(selected_label)
            selected_label.deleteLater()

    def get_selected_label(self):
        for i in range(self.Gallery_qGL.count()):
            widget = self.Gallery_qGL.itemAt(i).widget()
            if widget.property('selected'):
                widget.index = i
                return widget
        return None

    def mousePressEvent(self, event):
        self.deselect_all_widgets()
        clicked_widget = self.get_clicked_widget()
        if clicked_widget is not None:
            self.set_widget_properties(
                clicked_widget,
                selected=True,
                stylesheet='background-color: #4a90e2'
            )
            self.set_widget_filename(clicked_widget)

    def deselect_all_widgets(self):
        for i in range(self.Gallery_qGL.count()):
            widget = self.Gallery_qGL.itemAt(i).widget()
            self.set_widget_properties(widget, selected=False, stylesheet='')

    def get_clicked_widget(self):
        for i in range(self.Gallery_qGL.count()):
            widget = self.Gallery_qGL.itemAt(i).widget()
            if widget.underMouse():
                return widget
        return None

    def set_widget_properties(self, widget, selected=False, stylesheet=''):
        widget.setProperty('selected', selected)
        widget.setStyleSheet(stylesheet)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def set_widget_filename(self, widget):
        filename = widget.property('filename')
        if not filename:
            i = self.Gallery_qGL.indexOf(widget)
            filename = self.images[i][0]
            widget.setProperty('filename', filename)

    def store_faces_with_names(self):
        faceClassifer = cv2.CascadeClassifier(
            f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')

        for imgPath in os.scandir(TRAINING_DATASET):
            if imgPath.is_file() and imgPath.name.endswith('.jpg'):
                imgName = os.path.splitext(imgPath.name)[0]
                image = cv2.imread(os.path.join(
                    TRAINING_DATASET, imgPath.name))
                faces = faceClassifer.detectMultiScale(image, 1.1, 5)
                name = imgName
                personPath = os.path.join(
                    self.EXTRACTED_DATASET, name.split('_')[0])

                if not os.path.exists(personPath):
                    os.makedirs(personPath)

                for x, y, width, height in faces:
                    extracted_face = image[y:y + height, x:x + width]
                    resized_face = cv2.resize(extracted_face, (150, 150))
                    filename = f'{name}.jpg'
                    filepath = os.path.join(personPath, filename)
                    cv2.imwrite(filepath, resized_face)

        self.message_qLB.setText('Treinamento feito com sucesso')

    def train_faces(self):
        directory = EXTRACTED_DATASET
        known_faces = []
        known_names = []

        for name in os.listdir(directory):
            namePath = os.path.join(directory, name)
            print(namePath)
            if not os.path.isdir(namePath):
                continue

            for imageName in os.listdir(namePath):
                imagePath = os.path.join(namePath, imageName)
                if not os.path.isfile(imagePath):
                    continue

                image = face_recognition.load_image_file(imagePath)
                face_locations = face_recognition.face_locations(image)
                face_encodings = face_recognition.face_encodings(
                    image, face_locations)

                for encoding in face_encodings:
                    known_faces.append(encoding)
                    known_names.append(name)

        # with open(self.FACES_DAT, 'wb') as f:
        #     pickle.dump((known_names, known_faces), f)
        f = open(self.FACES_DAT, 'wb')
        pickle.dump((known_names, known_faces), f)

        self.message_qLB.setText('Faces extraidas e armazenadas com sucesso')

    def train_model(self):
        self.store_faces_with_names()
        self.train_faces()


if __name__ == '__main__':
    app = QApplication([])
    window = GalleryWindow()
    app.exec_()
