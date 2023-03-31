from __future__ import annotations

import os
import pathlib
import sys
import json

from course_attendance import AttendanceListWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
UI_PATH = pathlib.Path(CURRENT_FILE_PATH, 'ui', 'course_attendance_list.ui')
DATABASE_PATH = pathlib.Path(CURRENT_FILE_PATH, 'database', 'student_data.JSON')

class CourseAttendanceListWindow(QWidget):
    my_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(UI_PATH, self)
        self.calendar = self.findChild(QCalendarWidget, 'calendarWidget')
        self.label = self.findChild(QLabel, 'selected_date_qL')
        self.calendar.selectionChanged.connect(self.grab_date)
        self.button_clicked_event()
        self.get_dataset(DATABASE_PATH)
        self.data = None
        self.show()

    def receive_data(self,data):
        data_classes = self.database["classes"]
        for i in data_classes:
            class_id = i["class_id"]
            if class_id == int(data):
                self.data = class_id
                class_name = i["class_name"]
                class_year = i["class_year"]
                name_and_year = f"{class_name} {class_year}"
                self.course_qL.setText(f"Turma: {name_and_year}")
                break
    
    def get_dataset(self, path):
        with open(path, encoding="utf-8") as f:
            self.database = json.load(f)
            return self.database
        
    def grab_date(self):
        dateSelected = self.calendar.selectedDate()
        self.label.setText('Data Selecionada: ' + dateSelected.toString('dd/MM/yyyy'))

    def button_clicked_event(self):
        self.new_entry_qPB.clicked.connect(self.go_to_course_attendance_list)
        self.close_qPB.clicked.connect(self.close)

    def go_to_course_attendance_list(self):
        Attendance = AttendanceListWindow()
        AttendanceData = Attendance.set_class_info
        self.my_signal.connect(AttendanceData)
        self.my_signal.emit(str(self.data))

if __name__ == '__main__':
    App = QApplication([])
    consult_lists = CourseAttendanceListWindow()
    consult_lists.show()
    sys.exit(App.exec_())
