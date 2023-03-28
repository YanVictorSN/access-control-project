# parent/app.py
from __future__ import annotations

import os
import pathlib
import sys

from PyQt5.QtWidgets import QApplication

from src.main import MainWindow

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TRAINING_DATASET = pathlib.Path(CURRENT_FILE_PATH, 'src', 'resources', 'training_dataset')
EXTRACTED_DATASET = pathlib.Path(CURRENT_FILE_PATH, 'src', 'resources', 'extracted_dataset')
ATTENDANCE = pathlib.Path(CURRENT_FILE_PATH, 'src', 'attendance')


def create_folders():
    os.makedirs(TRAINING_DATASET, exist_ok=True)
    os.makedirs(EXTRACTED_DATASET, exist_ok=True)
    os.makedirs(ATTENDANCE, exist_ok=True)


if __name__ == '__main__':
    create_folders()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
