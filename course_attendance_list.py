from __future__ import annotations

import os
import sys
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

from course_attendance import AttendanceListWindow
from ui.ui_course_attendance_list import Ui_Images_qW

from class_reports import ClassReportsWindow


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
COURSE_DB = os.path.join(CURRENT_FILE_PATH, 'database', 'Course.json')


class CourseAttendanceListWindow(QWidget, Ui_Images_qW):
    my_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.calendar = self.findChild(QCalendarWidget, 'calendarWidget')
        self.label = self.findChild(QLabel, 'selected_date_qL')
        self.calendar.selectionChanged.connect(self.grab_date)
        self.course_DB = self.get_database(COURSE_DB)
        self.data = None
        self.button_clicked_event()
        self.show()

    def receive_data(self, data):
        data_courses = self.course_DB["courses"]
        for i in data_courses:
            class_id = i["course_id"]
            if class_id == int(data):
                self.data = class_id
                course_name = i["course_name"]
                course_year = i["course_year"]
                name_and_year = f"{course_name} {course_year}"
                self.course_qL.setText(f"Turma: {name_and_year}")
                break

    def get_database(self, path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    def grab_date(self):
        dateSelected = self.calendar.selectedDate()
        self.label.setText('Data Selecionada: ' + dateSelected.toString('dd/MM/yyyy'))

    def button_clicked_event(self):
        self.new_entry_qPB.clicked.connect(self.go_to_course_attendance_list)
        self.view_report_qPB.clicked.connect(self.go_to_class_reports)
        self.close_qPB.clicked.connect(self.close)

    def go_to_course_attendance_list(self):
        self.AttendanceList = AttendanceListWindow()
        self.AttendanceListData = self.AttendanceList.set_course_info
        self.my_signal.connect(self.AttendanceListData)
        self.my_signal.emit(str(self.data))

    def go_to_class_reports(self):
        self.close()
        self.class_reports = ClassReportsWindow()
        self.class_reports.show()


if __name__ == '__main__':
    App = QApplication([])
    consult_lists = CourseAttendanceListWindow()
    consult_lists.show()
    sys.exit(App.exec_())
