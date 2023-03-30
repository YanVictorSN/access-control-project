# flake8: noqa
# pylint: skip-file
from __future__ import annotations

schema = {
    'type': 'object',
    'properties': {
            'Student': {
                'type': 'object',
                'properties': {
                    'student_id': {'type': 'integer'},
                    'student_code': {'type': 'string'},
                    'student_name': {'type': 'string'}
                }
            },
        'Courses': {
                'type': 'object',
                'properties': {
                    'course_id': {'type': 'integer'},
                    'course_code': {'type': 'string'},
                    'course_name': {'type': 'string'},
                    'course_year': {'type': 'string'}
                }
            },
        'Attendance': {
                'type': 'object',
                'properties': {
                    'attendance_id': {'type': 'integer'},
                    'attendance_date': {'type': 'string'},
                    'course_id': {'type': 'integer', 'foreign_key': 'course.course_id'}
                }
            },
        'Student_course': {
                'type': 'object',
                'properties': {
                    'student_id': {'type': 'integer', 'foreign_key': 'Student.student_id'},
                    'course_id': {'type': 'integer', 'foreign_key': 'course.course_id'}
                }
            },
        'Attendance_Student': {
                'type': 'object',
                'properties': {
                    'attendance_id': {'type': 'integer', 'foreign_key': 'Attendance.attendance_id'},
                    'student_id': {'type': 'integer', 'foreign_key': 'Student.student_id'},
                    'presence': {'type': 'integer', 'default': 0}
                }
            }
    }
}
