# parent/app.py
from __future__ import annotations

import sys

from PyQt5.QtWidgets import QApplication

from src.main import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
