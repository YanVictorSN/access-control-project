from __future__ import annotations

import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from run_subprocess import run_subprocess

CURRENT_FILE_PATH = os.path.abspath(__file__)

#Assigning paths to import UI class_reports code
UI_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'ui', 'ui_class_reports.ui')

#Assigning paths to import functions from course_attendance_list.py and course_attendance.py
ATTENDACE_LIST = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'course_attendance_list.py')
ATTENDANCE = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'course_attendance.py')

class ClassReportsWindow(QWidget):

    #Starts the Class Reports Window on the screen
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.show()   

    #Show Table
    def init_ui(self):
        self.course_qTW.setHorizontalHeaderLabels(['Código', 'Status', 'Alunos'])
        self.course_qTW.resizeColumnsToContents()

    #Assigning events to the buttons
    def button_clicked_event(self):

        #Throw to the course_attendance_list window when called on next lines
        self.close__qPB.clicked.connect(self.close)

        #Throw to the course_attendance window when called on next lines
        self.btn_training.clicked.connect(self.go_to_attendance)

    def go_to_course_attendance_list(self):
        run_subprocess(ATTENDACE_LIST)

    def go_to_attendance(self):
        run_subprocess(ATTENDANCE)

if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = ClassReportsWindow()
    Home.show()
    App.exec_()
