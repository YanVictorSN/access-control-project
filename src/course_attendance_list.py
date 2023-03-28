from __future__ import annotations

import os
import sys
from datetime import datetime
import json

from course_attendance import AttendanceListWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


CURRENT_FILE_PATH = os.path.abspath(__file__)
UI_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'ui', 'course_attendance_list.ui')
DATABASE_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'database', 'student_data.JSON')


class CourseAttendanceListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(UI_PATH, self)
        self.calendar = self.findChild(QCalendarWidget, 'calendarWidget')
        self.label = self.findChild(QLabel, 'selected_date_qL')
        self.calendar.selectionChanged.connect(self.grab_date)
        self.button_clicked_event()
        self.start_attendance_cam()
        self.set_attendance_time()
        self.get_dataset(DATABASE_PATH)
        self.set_student_info()
        self.set_class_info()
        self.button_end_attendance_list()
        self.show()

    def grab_date(self):
        dateSelected = self.calendar.selectedDate()
        self.label.setText('Data Selecionada: ' + dateSelected.toString('dd/MM/yyyy'))

    def button_clicked_event(self):
        self.close_qPB.clicked.connect(self.cancel)

    def start_attendance_cam(self):
        self.attendance_cam = AttendanceCam()
        self.attendance_cam.start()
        self.attendance_cam.ImageUpdate.connect(self.get_image)

    def cancel(self):
        self.attendance_cam.stop()

    def get_image(self, image):
        self.camera_qL.setPixmap(QPixmap.fromImage(image))

    def get_dataset(self, path):
        with open(path) as f:
            self.database = json.load(f)
            return self.database

    def set_attendance_time(self):
        current_date = datetime.now()
        current_date_formated = current_date.strftime('%d/%m/%Y')
        self.attendance_date_qL.setText(current_date_formated)

    def set_class_info(self):
        class_info = self.database['classes'][0]
        self.course_name_qL.setText(f"{ class_info ['class_name']} {class_info['class_year']}")

    def set_student_info(self):
        data_students = self.database["students"]
        self.attendence_qTW.setRowCount(len(data_students))
      
        for i, student in enumerate(data_students):
            student_name = QTableWidgetItem(student["student_name"])
            student_code = QTableWidgetItem(str(student['student_code']))
            self.attendence_qTW.setItem(i, 0, student_code)
            self.attendence_qTW.setItem(i, 1, student_name)
    
    def button_end_attendance_list(self):
        self.finish_qPB.clicked.connect(self.end_attendance_list)
    
    def end_attendance_list(self):
        self.get_dataset(DATABASE_PATH)

class AttendanceCam(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(
                    FlippedImage.data,
                    FlippedImage.shape[1],
                    FlippedImage.shape[0],
                    QImage.Format_RGB888
                )
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        Capture.release()
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
