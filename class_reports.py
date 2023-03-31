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

#Get Json files from DB
COURSE_DB = os.path.join(CURRENT_FILE_PATH, 'database', 'Course.json')
# ATTENDANCE_STUDENT = os.path.join(CURRENT_FILE_PATH, 'database', 'Attendance_Student.json')

class ClassReportsWindow(QWidget):

    #Starts the Class Reports Window on the screen
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        # self.course_DB = self.get_database(COURSE_DB)
        # self.course_DB = self.set_classes_info(ATTENDANCE_STUDENT)
        # self.set_class_info()
        # self.set_selected_date()
        self.show()   

    #Print Class Info at teh Label
    # def set_class_info(self):
    #     self.label.setText('Turma: ' + COURSE_DB['course_name','course_yea'])

    #Show Table
    def init_ui(self):
        self.reports_qTW.setHorizontalHeaderLabels(['Código', 'Status', 'Alunos'])
        self.reports_qTW.resizeColumnsToContents()

    # def get_database(self, path):
    #         with open(path, encoding='utf-8') as f:
    #             return json.load(f)
            
    #Assigning events to the buttons
    def button_clicked_event(self):

        #Close class_reports window when called
        self.close__qPB.clicked.connect(self.close)

        #Throw to the course_attendance window when called on next lines
        self.new_entry_qPB.clicked.connect(self.go_to_course_attendance)

    def go_to_course_attendance(self):
        run_subprocess(ATTENDANCE)

if __name__ == '__main__':
    App = QApplication(sys.argv)
    Home = ClassReportsWindow()
    Home.show()
    App.exec_()
