from __future__ import annotations

import json
import os
import pickle
import sys
from datetime import date
from datetime import datetime

import cv2
import face_recognition
import pandas as pd
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget

from ui.ui_course_attendance import Ui_Attendance_qW

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
COURSE_DB = os.path.join(CURRENT_FILE_PATH, 'database', 'Course.json')
STUDENT_DB = os.path.join(CURRENT_FILE_PATH, 'database', 'Student.json')


class AttendanceListWindow(QWidget, Ui_Attendance_qW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.button_clicked_event()
        self.start_attendance_cam()
        self.set_attendance_time()
        self.student_DB = self.get_database(STUDENT_DB)
        self.course_DB = self.get_database(COURSE_DB)
        self.data = None
        self.show()

    def init_ui(self):
        self.attendence_qTW.setHorizontalHeaderLabels(['Matrícula', 'Nome'])
        self.attendence_qTW.resizeColumnsToContents()

    def button_clicked_event(self):
        self.close_qPB.clicked.connect(self.stop_thread)

    def start_attendance_cam(self):
        self.attendance_cam = AttendanceCam()
        self.attendance_cam.start()
        self.attendance_cam.ImageUpdate.connect(self.get_image)

    def stop_thread(self):
        self.attendance_cam.stop()
        self.close()

    def get_image(self, image):
        self.camera_qL.setPixmap(QPixmap.fromImage(image))

    def set_attendance_time(self):
        current_date = datetime.now()
        current_date_formated = current_date.strftime('%d/%m/%Y')
        self.attendance_date_qL.setText(current_date_formated)

    def get_database(self, path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    def set_course_info(self, data):
        data_courses = self.course_DB['courses']
        for i in data_courses:
            class_id = i['course_id']
            if class_id == int(data):
                self.data = class_id
                course_name = i['course_name']
                course_year = i['course_year']
                name_and_year = f'{course_name} {course_year}'
                self.course_name_qL.setText(f'{name_and_year}')
                self.set_student_info()
                break

    def set_student_info(self):
        data_students = self.student_DB['students']
        count = 0
        for student in data_students:
            if student['student_course_id'] == str(self.data):
                self.insert_student_to_ui(count, student['student_code'], student['student_name'])
                count += 1

    def insert_student_to_ui(self, row_position, code, name):
        self.attendence_qTW.insertRow(row_position)
        self.attendence_qTW.setItem(row_position, 0, QTableWidgetItem(code))
        self.attendence_qTW.setItem(row_position, 1, QTableWidgetItem(name))


class AttendanceCam(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        counter = 0
        faces_found = ['Unknown']
        face_recognizer = FaceRecognizer()
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                # Flip the image
                flipped_frame = cv2.flip(frame, 1)
                if counter % 10 == 0:
                    # Recognize faces and draw bounding boxes and names
                    face_locations, face_names = face_recognizer.recognize_faces(flipped_frame)

                    # Remove faces that have already been found
                    face_names = [name for name in face_names if name not in faces_found]

                    # Add new faces to the list of found faces
                    faces_found.extend(face_names)

                counter += 1

                if face_names:
                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        cv2.putText(flipped_frame, f'{name.capitalize()} presente',
                                    (15, 27), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 50), 1)

                # Convert the modified frame to Qt format and emit the image
                flipped_image = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
                qimage = QImage(flipped_image.data, flipped_image.shape[1],
                                flipped_image.shape[0], QImage.Format_RGB888)
                scaled_qimage = qimage.scaled(640, 480, Qt.KeepAspectRatio)

                self.ImageUpdate.emit(scaled_qimage)
        Capture.release()

    def stop(self):
        self.ThreadActive = False
        self.wait()
        self.quit()


class FaceRecognizer:
    def __init__(self):
        self.CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.FACES_DAT = os.path.join(self.CURRENT_FILE_PATH, 'resources', 'faces.dat')
        self.ATTENDANCE = os.path.join(self.CURRENT_FILE_PATH, 'attendance')

    def load_known_faces(self):
        with open(self.FACES_DAT, 'rb') as f:
            return pickle.load(f)

    def recognize_face_names(self, known_names, known_faces, rgb_small_frame):
        face_names = []
        face_encodings = face_recognition.face_encodings(rgb_small_frame)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = 'Unknown'
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
            face_names.append(name)
        return face_names

    def mark_attendance(self, name, added_names):
        today = date.today().strftime('%d-%m-%y')
        capitalized_name = name.capitalize()
        if capitalized_name not in added_names:
            filename = 'attendance.xlsx'
            full_path = os.path.join(self.ATTENDANCE, filename)
            all_names = ['Amorim', 'Yan', 'Bruno', 'Sara', 'Vitoria']
            if not os.path.exists(full_path):
                # Create a new DataFrame with all student names and today's date as the columns
                columns = ['Name'] + [today]
                df = pd.DataFrame(columns=columns)
                df['Name'] = all_names
                df[today] = ' '
                df.loc[df['Name'] == capitalized_name, today] = 'PRESENTE'
                df.to_excel(full_path, index=False)
            else:
                df_existing = pd.read_excel(full_path)
                if capitalized_name not in df_existing['Name'].values:
                    # Add a new row to the existing DataFrame with the name and "present" on today's date
                    new_row = pd.DataFrame({'Name': [capitalized_name], today: ['PRESENTE']})
                    df_existing = df_existing.append(new_row, ignore_index=True)
                else:
                    # Update the value in the row corresponding to the name and today's date to "present"
                    df_existing.loc[df_existing['Name'] == capitalized_name, today] = 'PRESENTE'
                df_existing.to_excel(full_path, index=False)
            added_names.add(capitalized_name)

    def recognize_faces(self, frame):
        # Scale down the frame to improve recognition speed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the small frame to RGB for face recognition
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find the locations and names of the faces in the image
        face_locations = face_recognition.face_locations(rgb_small_frame)
        known_names, known_faces = self.load_known_faces()
        face_names = self.recognize_face_names(known_names, known_faces, rgb_small_frame)

        # Scale up the face locations to match the original frame size
        face_locations = [(top * 4, right * 4, bottom * 4, left * 4) for (top, right, bottom, left) in face_locations]

        # Mark attendance for the recognized faces
        added_names = set()
        for name in face_names if face_names != ['Unknown'] else []:
            self.mark_attendance(name, added_names)

        return face_locations, face_names


if __name__ == '__main__':
    App = QApplication([])
    Home = AttendanceListWindow()
    sys.exit(App.exec())
