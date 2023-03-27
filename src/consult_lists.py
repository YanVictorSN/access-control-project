from __future__ import annotations

import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QLabel
from course_attendance_list import AttendanceList


CURRENT_FILE_PATH = os.path.abspath(__file__)
UI_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'ui', 'consult_lists.ui')


class ConsultListsWindow(QWidget):
    def __init__(self):
        super(ConsultListsWindow, self).__init__()
        self.ui = uic.loadUi(UI_PATH, self)
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
        self.course_attendance_list = AttendanceList()
        self.course_attendance_list.show()


if __name__ == '__main__':
    App = QApplication([])
    consult_lists = ConsultListsWindow()
    consult_lists.show()
    sys.exit(App.exec_())

