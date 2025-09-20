# lib/enrollment.py
from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Optional


class Student:
    all: List["Student"] = []

    def __init__(self, name: str):
        self.name = name
        self._enrollments: List[Enrollment] = []
        self._grades: Dict[Enrollment, float] = {}
        Student.all.append(self)

    # --- relationships ---
    def enroll(self, course: "Course") -> "Enrollment":
        if not isinstance(course, Course):
            raise TypeError("course must be a Course")
        enr = Enrollment(self, course)
        self._enrollments.append(enr)
        course._enrollments.append(enr)
        return enr

    def enrollments(self) -> List["Enrollment"]:
        return self._enrollments.copy()

    def courses(self) -> List["Course"]:
        return [en.course for en in self._enrollments]

    # --- aggregates (instance-level) ---
    def course_count(self) -> int:
        return len(self._enrollments)

    def set_grade(self, enrollment: "Enrollment", grade: float) -> None:
        if not isinstance(enrollment, Enrollment):
            raise TypeError("enrollment must be an Enrollment")
        if enrollment not in self._enrollments:
            raise ValueError("enrollment does not belong to this student")
        self._grades[enrollment] = float(grade)

    def aggregate_average_grade(self) -> float:
        if not self._grades:
            return 0.0
        return sum(self._grades.values()) / len(self._grades)


class Course:
    all: List["Course"] = []

    def __init__(self, title: str):
        self.title = title
        self._enrollments: List[Enrollment] = []
        Course.all.append(self)

    # --- relationships ---
    def enroll_student(self, student: "Student") -> "Enrollment":
        if not isinstance(student, Student):
            raise TypeError("student must be a Student")
        enr = Enrollment(student, self)
        self._enrollments.append(enr)
        student._enrollments.append(enr)
        return enr

    def enrollments(self) -> List["Enrollment"]:
        return self._enrollments.copy()

    def students(self) -> List["Student"]:
        return [en.student for en in self._enrollments]

    # --- aggregates (instance-level) ---
    def student_count(self) -> int:
        return len(self._enrollments)


class Enrollment:
    all: List["Enrollment"] = []

    def __init__(self, student: Student, course: Course):
        if not isinstance(student, Student) or not isinstance(course, Course):
            raise TypeError("student must be Student and course must be Course")
        self.student = student
        self.course = course
        self._enrollment_date: datetime = datetime.now()
        Enrollment.all.append(self)

    def get_enrollment_date(self) -> datetime:
        return self._enrollment_date

    # --- aggregates (class-level) ---
    @classmethod
    def aggregate_enrollments_per_day(cls) -> Dict[datetime.date, int]:
        counts: Dict[datetime.date, int] = {}
        for en in cls.all:
            d = en.get_enrollment_date().date()
            counts[d] = counts.get(d, 0) + 1
        return counts