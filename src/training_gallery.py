from __future__ import annotations

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

UI_PATH = 'ui/training_gallery.ui'
DATASET_FOLDER = 'training_dataset'
MAX_COLUMNS = 3


class GalleryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.setup_button_events()
        self.get_images()
        self.add_images_to_grid()
        self.show()

    def init_ui(self):
        self.student_name = sys.argv[1] if len(sys.argv) > 1 else ''
        self.base_directory = os.path.abspath(os.path.dirname(__file__))
        self.image_directory = os.path.join(self.base_directory, DATASET_FOLDER)
        self.images = []
        self.MAX_COLUMNS = 3

    def setup_button_events(self):
        self.ui.delete_image_QPB.clicked.connect(self.delete_image)
        self.ui.close_QPB.clicked.connect(self.close)

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
            self.ui.Gallery_QGL.addWidget(image_label, row, col)

    def delete_image(self):
        selected_label = self.get_selected_label()
        if selected_label is not None:
            filename = selected_label.property('filename') or self.images[selected_label.index][0]
            os.remove(os.path.join(self.image_directory, filename))
            self.ui.Gallery_QGL.removeWidget(selected_label)
            selected_label.deleteLater()

    def get_selected_label(self):
        for i in range(self.ui.Gallery_QGL.count()):
            widget = self.ui.Gallery_QGL.itemAt(i).widget()
            if widget.property('selected'):
                widget.index = i
                return widget
        return None

    def mousePressEvent(self, event):
        self.deselect_all_image_labels()
        for i in range(self.ui.Gallery_QGL.count()):
            widget = self.ui.Gallery_QGL.itemAt(i).widget()
            if widget.underMouse():
                self.select_image_label(widget)

    def deselect_all_image_labels(self):
        for i in range(self.ui.Gallery_QGL.count()):
            widget = self.ui.Gallery_QGL.itemAt(i).widget()
            self.set_widget_properties(widget, selected=False, stylesheet='')

    def select_image_label(self, widget):
        self.set_widget_properties(widget, selected=True, stylesheet='background-color: #4a90e2')
        filename = widget.property('filename') or self.images[widget.index][0]
        widget.setProperty('filename', filename)

    def set_widget_properties(self, widget, selected=False, stylesheet=''):
        widget.setProperty('selected', selected)
        widget.setStyleSheet(stylesheet)
        widget.style().unpolish(widget)
        widget.style().polish(widget)


if __name__ == '__main__':
    app = QApplication([])
    window = GalleryWindow()
    app.exec_()
