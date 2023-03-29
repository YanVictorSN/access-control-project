from __future__ import annotations

import os
import sys

from course_attendance import AttendanceListWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(CURRENT_FILE_PATH, 'ui', 'course_attendance_list.ui')


class CourseAttendanceListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(UI, self)
        self.calendar = self.findChild(QCalendarWidget, 'calendarWidget')
        self.label = self.findChild(QLabel, 'selected_date_qL')
        self.calendar.selectionChanged.connect(self.grab_date)
        self.button_clicked_event()
        self.show()

    def grab_date(self):
        dateSelected = self.calendar.selectedDate()
        self.label.setText('Data Selecionada: ' + dateSelected.toString('dd/MM/yyyy'))

    def button_clicked_event(self):
        self.new_entry_qPB.clicked.connect(self.go_to_course_attendance_list)
        self.close_qPB.clicked.connect(self.close)

    def go_to_course_attendance_list(self):
        self.close()
        self.course_attendance_list = AttendanceListWindow()
        self.course_attendance_list.show()


if __name__ == '__main__':
    App = QApplication([])
    consult_lists = CourseAttendanceListWindow()
    consult_lists.show()
    sys.exit(App.exec_())
