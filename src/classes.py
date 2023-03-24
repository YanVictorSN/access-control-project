from __future__ import annotations

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


UI_PATH = 'ui/classes.ui'


class CourseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.show()

    def init_ui(self):
        self.course_qTW.setHorizontalHeaderLabels(['Código', 'Ano', 'Alunos', 'Turma'])
        self.course_qTW.resizeColumnsToContents()

    def button_clicked_event(self):
        self.close_qPB.clicked.connect(self.close)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = CourseWindow()
    Home.show()
    App.exec_()
