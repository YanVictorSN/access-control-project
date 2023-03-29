from __future__ import annotations

import json
import os
import pathlib
import pickle
import sys
from datetime import date
from datetime import datetime

import cv2
import face_recognition
import pandas as pd
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QWidget

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
UI_PATH = pathlib.Path(CURRENT_FILE_PATH, 'ui', 'course_attendance.ui')
DATABASE_PATH = pathlib.Path(CURRENT_FILE_PATH, 'database', 'student_data.JSON')


class AttendanceListWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(UI_PATH, self)
        self.init_ui()
        self.button_clicked_event()
        self.start_attendance_cam()
        self.set_attendance_time()
        self.get_dataset(DATABASE_PATH)
        self.set_class_info()
        self.set_student_info()
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

    def get_dataset(self, path):
        with open(path, encoding='utf-8') as f:
            self.database = json.load(f)
            return self.database

    def set_class_info(self):
        class_info = self.database['classes'][0]
        self.course_name_qL.setText(f"{ class_info ['class_name']} {class_info['class_year']}")

    def set_student_info(self):
        data_students = self.database['students']
        self.attendence_qTW.setRowCount(len(data_students))

        for i, student in enumerate(data_students):
            student_name = QTableWidgetItem(student['student_name'])
            student_code = QTableWidgetItem(str(student['student_code']))
            self.attendence_qTW.setItem(i, 0, student_code)
            self.attendence_qTW.setItem(i, 1, student_name)


class AttendanceCam(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        counter = 0
        face_recognizer = FaceRecognizer()
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                # Flip the image
                flipped_frame = cv2.flip(frame, 1)
                if counter % 20 == 0:
                    # Recognize faces and draw bounding boxes and names
                    face_locations, face_names = face_recognizer.recognize_faces(flipped_frame)
                counter += 1

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    if face_names != ['Unknown']:
                        cv2.rectangle(flipped_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        cv2.rectangle(flipped_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(flipped_frame, name, (left + 6, bottom - 6),
                                    font, 1.0, (255, 255, 255), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(flipped_frame, 'Nenhum rosto cadastrado encontrado',
                                    (15, 27), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

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
        self.FACES_DAT = pathlib.Path(self.CURRENT_FILE_PATH, 'resources', 'faces.dat')
        self.ATTENDANCE = pathlib.Path(self.CURRENT_FILE_PATH, 'attendance')

    def load_known_faces(self):
        with open(self.FACES_DAT, 'rb') as f:
            return pickle.load(f)

    def recognize_face_names(self, known_names, known_faces, rgb_small_frame):
        face_names = []
        face_encodings = face_recognition.face_encodings(rgb_small_frame)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = 'Unknown'
            if True in matches and name != 'Unknown':
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
            face_names.append(name)
        return face_names

    def mark_attendance(self, name, added_names):
        today = date.today().strftime('%Y-%m-%d')
        capitalized_name = name.capitalize()
        if capitalized_name not in added_names:
            filename = f'attendance_{today}.xlsx'
            full_path = pathlib.Path(self.ATTENDANCE, filename)
            df = pd.DataFrame({'Name': [capitalized_name], 'Date': [today]})
            if not full_path.exists():
                df.to_excel(full_path, index=False)
            else:
                df_existing = pd.read_excel(full_path)
                if capitalized_name not in df_existing['Name'].values:
                    df_existing = df_existing.append(df, ignore_index=True)
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
        for name in face_names:
            self.mark_attendance(name, added_names)

        return face_locations, face_names


if __name__ == '__main__':
    App = QApplication([])
    Home = AttendanceListWindow()
    sys.exit(App.exec())
