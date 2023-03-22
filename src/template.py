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
        self.buttonClickedEvent()
        self.show()

    def buttonClickedEvent(self):
        self.example_QPB.clicked.connect(self.goToExample)
        self.close_QPB.clicked.connect(self.close)

    def goToExample(self):
        # # function to go to example.py
        # subprocess.Popen(['python', EXAMPLE])
        print(f'fui para o {EXAMPLE}')


if __name__ == '__main__':
    App = QApplication([])
    Home = TemplateWindow()
    sys.exit(App.exec())
