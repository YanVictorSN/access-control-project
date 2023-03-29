# parent/app.py
from __future__ import annotations

import os
import sys

from PyQt5.QtWidgets import QApplication

from main import MainWindow
from run_subprocess import convert_ui_files

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCES = os.path.join(CURRENT_FILE_PATH, 'resources')
TRAINING_DATASET = os.path.join(CURRENT_FILE_PATH, 'resources', 'training_dataset')
EXTRACTED_DATASET = os.path.join(CURRENT_FILE_PATH, 'resources', 'extracted_dataset')
ATTENDANCE = os.path.join(CURRENT_FILE_PATH, 'attendance')


def create_folders():
    os.makedirs(RESOURCES, exist_ok=True)
    os.makedirs(TRAINING_DATASET, exist_ok=True)
    os.makedirs(EXTRACTED_DATASET, exist_ok=True)
    os.makedirs(ATTENDANCE, exist_ok=True)


if __name__ == '__main__':
    create_folders()
    convert_ui_files()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
