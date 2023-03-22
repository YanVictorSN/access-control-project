from __future__ import annotations

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


UI_PATH = 'ui/template.ui'
EXAMPLE = 'example.py'


class TemplateWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.button_clicked_event()
        self.show()

    def button_clicked_event(self):
        self.example_QPB.clicked.connect(self.go_to_example)
        self.close_QPB.clicked.connect(self.close)

    def go_to_example(self):
        # # function to go to example.py
        # subprocess.Popen(['python', EXAMPLE])
        print(f'fui para o {EXAMPLE}')


if __name__ == '__main__':
    App = QApplication([])
    Home = TemplateWindow()
    sys.exit(App.exec())
