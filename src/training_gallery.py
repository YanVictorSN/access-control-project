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
        self.button_clicked_event()
        self.get_images()
        self.add_image_to_grid()
        self.show()

    def init_ui(self):
        self.student_name = sys.argv[1] if len(sys.argv) > 1 else ''

    def button_clicked_event(self):
        self.delete_image_QPB.clicked.connect(self.delete_image)
        self.close_QPB.clicked.connect(self.close)

    def get_images(self):
        base_directory = os.path.abspath(os.path.dirname(__file__))
        self.image_directory = os.path.join(base_directory, DATASET_FOLDER)
        self.image_files = os.listdir(self.image_directory)
        self.images = []
        for filename in self.image_files:
            if self.student_name in filename:
                image_path = os.path.join(self.image_directory, filename)
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    self.images.append((filename, pixmap))

    def add_image_to_grid(self):
        row, col = 0, 0
        for filename, pixmap in self.images:
            image_label = QLabel(self)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setPixmap(pixmap.scaledToWidth(200))
            self.Gallery_QGL.addWidget(image_label, row, col)
            col += 1
            if col == MAX_COLUMNS:
                row += 1
                col = 0

    def delete_image(self):
        # Get the selected image label
        selected_label = None
        for i in range(self.Gallery_QGL.count()):
            widget = self.Gallery_QGL.itemAt(i).widget()
            if widget.property('selected'):
                selected_label = widget
                break

        # Delete the selected image file
        if selected_label is not None:
            filename = selected_label.property('filename')
            if not filename:
                # Get the filename from the image list
                filename = self.images[i][0]
            os.remove(os.path.join(self.image_directory, filename))

            # Remove the selected image label from the layout
            self.Gallery_QGL.removeWidget(selected_label)
            selected_label.deleteLater()

    def mousePressEvent(self, event):
        # Deselect all image labels
        for i in range(self.Gallery_QGL.count()):
            widget = self.Gallery_QGL.itemAt(i).widget()
            self.set_colors(widget)
            # Set an empty filename property
            widget.setProperty('filename', '')

        # Get the clicked image label
        for i in range(self.Gallery_QGL.count()):
            widget = self.Gallery_QGL.itemAt(i).widget()
            if widget.underMouse():
                self.set_colors(
                    widget,
                    is_selected=True,
                    stylesheet='background-color: #4a90e2'
                )
                # Set the filename property on the clicked image label
                filename = widget.property('filename')
                if not filename:
                    filename = self.images[i][0]
                    widget.setProperty('filename', filename)
                break

    def set_colors(self, widget, is_selected=False, stylesheet=''):
        widget.setProperty('selected', is_selected)
        widget.setStyleSheet(stylesheet)
        widget.style().unpolish(widget)
        widget.style().polish(widget)


if __name__ == '__main__':
    app = QApplication([])
    window = GalleryWindow()
    app.exec_()
