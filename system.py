import csv
import os
import json
from models import Student, Course, Teacher, Unit

class EducationSystem:
    """Main system controller for EduManage - Advanced Edition."""
    def __init__(self, students_file=None, courses_file=None, teachers_file=None, enrollments_file=None, data_file=None):
        if data_file:
            base_dir = os.path.dirname(os.path.abspath(data_file))
        else:
            base_dir = os.getcwd()
            if None in (students_file, courses_file, teachers_file, enrollments_file):
                base_dir = os.getcwd()

        self.students_file = students_file or os.path.join(base_dir, "students_data.csv")
        self.courses_file = courses_file or os.path.join(base_dir, "courses_data.csv")
        self.teachers_file = teachers_file or os.path.join(base_dir, "teachers_data.csv")
        self.enrollments_file = enrollments_file or os.path.join(base_dir, "enrollments_data.csv")
        
        self.students = {}  # student_id: Student object
        self.courses = {}   # course_id: Course object
        self.teachers = {}  # teacher_id: Teacher object
        self.enrollments = []  # list of (student_id, course_id, grade) tuples
        
        self.load_data()

    def add_student(self, student_id, name, email):
        if student_id in self.students:
            raise ValueError(f"Student with ID {student_id} already exists.")
        new_student = Student(student_id, name, email)
        self.students[student_id] = new_student
        return new_student

    def add_course(self, course_id, name, credits):
        if course_id in self.courses:
            raise ValueError(f"Course with ID {course_id} already exists.")
        new_course = Course(course_id, name, credits)
        self.courses[course_id] = new_course
        return new_course

    def add_course_unit(self, course_id, unit_id, name, credits):
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found.")
        self.courses[course_id].add_unit(unit_id, name, credits)
        return True

    def update_course_unit(self, course_id, unit_id, name=None, credits=None):
        """Update unit metadata (name/credits) for a given course."""
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found.")
        course = self.courses[course_id]
        for u in course.units:
            if u.get('unit_id') == unit_id:
                if name is not None:
                    u['name'] = name
                if credits is not None:
                    u['credits'] = credits
                return True
        raise ValueError(f"Unit {unit_id} not found in course {course_id}.")

    def delete_course_unit(self, course_id, unit_id):
        """Delete a unit from a course and remove related unit enrollments."""
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found.")
        course = self.courses[course_id]
        original_count = len(course.units)
        course.units = [u for u in course.units if u.get('unit_id') != unit_id]
        if len(course.units) == original_count:
            raise ValueError(f"Unit {unit_id} not found in course {course_id}.")

        # remove unit enrollments from students
        for student in self.students.values():
            if course_id in student.enrolled_courses:
                units = student.enrolled_courses[course_id].get('units', {})
                if unit_id in units:
                    del units[unit_id]
                if not units:
                    # remove whole course enrollment if no units remain
                    del student.enrolled_courses[course_id]
        return True

    def update_student(self, student_id, name, email):
        if student_id not in self.students:
            raise ValueError(f"Student {student_id} not found.")
        student = self.students[student_id]
        student.name = name
        student.email = email
        return student

    def delete_student(self, student_id):
        if student_id not in self.students:
            raise ValueError(f"Student {student_id} not found.")
        del self.students[student_id]

    def update_course(self, course_id, name, credits):
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found.")
        course = self.courses[course_id]
        course.name = name
        course.credits = credits
        return course

    def delete_course(self, course_id):
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found.")
        course = self.courses.pop(course_id)
        for student in self.students.values():
            if course_id in student.enrolled_courses:
                del student.enrolled_courses[course_id]
        if course.teacher_id and course.teacher_id in self.teachers:
            self.teachers[course.teacher_id].remove_course(course_id)

    def add_teacher(self, teacher_id, name, email, department=""):
        if teacher_id in self.teachers:
            raise ValueError(f"Teacher with ID {teacher_id} already exists.")
        new_teacher = Teacher(teacher_id, name, email, department)
        self.teachers[teacher_id] = new_teacher
        return new_teacher

    def assign_teacher_to_course(self, teacher_id, course_id):
        if teacher_id not in self.teachers:
            raise ValueError(f"Teacher {teacher_id} not found.")
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found.")
        
        # Remove previous teacher if exists
        # legacy behavior: set course-level teacher (kept for backward compatibility)
        prev = self.courses[course_id].teacher_id
        if prev and prev in self.teachers:
            # remove course-level assignment
            self.teachers[prev].remove_course(course_id) if hasattr(self.teachers[prev], 'remove_course') else None
        self.courses[course_id].teacher_id = teacher_id
        self.teachers[teacher_id].assign_course(course_id)

    def assign_teacher_to_unit(self, teacher_id, course_id, unit_id):
        """Assign a teacher to a specific unit inside a course."""
        if teacher_id not in self.teachers:
            raise ValueError(f"Teacher {teacher_id} not found.")
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found.")
        course = self.courses[course_id]
        prev_tid = None
        for u in course.units:
            if u.get('unit_id') == unit_id:
                prev_tid = u.get('teacher_id')
                u['teacher_id'] = teacher_id
                break
        else:
            raise ValueError(f"Unit {unit_id} not found in course {course_id}.")

        # update teacher records
        if prev_tid and prev_tid in self.teachers:
            # remove mapping from previous teacher
            try:
                self.teachers[prev_tid].remove_unit(course_id, unit_id)
            except Exception:
                pass
        self.teachers[teacher_id].assign_unit(course_id, unit_id)

    def update_teacher(self, teacher_id, name, email, department=""):
        if teacher_id not in self.teachers:
            raise ValueError(f"Teacher {teacher_id} not found.")
        teacher = self.teachers[teacher_id]
        teacher.name = name
        teacher.email = email
        teacher.department = department
        return teacher

    def delete_teacher(self, teacher_id):
        if teacher_id not in self.teachers:
            raise ValueError(f"Teacher {teacher_id} not found.")
        for course in self.courses.values():
            if course.teacher_id == teacher_id:
                course.teacher_id = None
        del self.teachers[teacher_id]

    def remove_enrollment(self, student_id, course_id):
        if student_id not in self.students:
            raise ValueError(f"Student {student_id} not found.")
        student = self.students[student_id]
        if course_id not in student.enrolled_courses:
            raise ValueError(f"Enrollment not found for student {student_id} and course {course_id}.")
        del student.enrolled_courses[course_id]

    def remove_unit_enrollment(self, student_id, course_id, unit_id):
        """Remove a single unit enrollment for a student within a course."""
        if student_id not in self.students:
            raise ValueError(f"Student {student_id} not found.")
        student = self.students[student_id]
        if course_id not in student.enrolled_courses:
            raise ValueError(f"Course enrollment not found for student {student_id} and course {course_id}.")
        units = student.enrolled_courses[course_id].get('units', {})
        if unit_id not in units:
            raise ValueError(f"Unit {unit_id} enrollment not found for student {student_id} in course {course_id}.")
        del units[unit_id]
        # if no more units, remove the whole course enrollment
        if not units:
            del student.enrolled_courses[course_id]

    def enroll_student(self, student_id, course_id):
        if student_id not in self.students:
            raise ValueError(f"Student {student_id} not found.")
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found.")
        self.students[student_id].enroll(course_id)

    def assign_grade(self, student_id, course_id, grade):
        if student_id not in self.students:
            raise ValueError(f"Student {student_id} not found.")
        # set overall grade marker (deprecated)
        self.students[student_id].assign_grade(course_id, grade)

    def enroll_student_unit(self, student_id, course_id, unit_id):
        if student_id not in self.students:
            raise ValueError(f"Student {student_id} not found.")
        if course_id not in self.courses:
            raise ValueError(f"Course {course_id} not found.")
        # ensure unit exists in course
        course = self.courses[course_id]
        if not any(u['unit_id'] == unit_id for u in course.units):
            raise ValueError(f"Unit {unit_id} not found in course {course_id}.")
        self.students[student_id].enroll_unit(course_id, unit_id)

    def assign_unit_grade(self, student_id, course_id, unit_id, grade):
        if student_id not in self.students:
            raise ValueError(f"Student {student_id} not found.")
        self.students[student_id].assign_unit_grade(course_id, unit_id, grade)

    def get_student_report(self, student_id):
        if student_id not in self.students:
            raise ValueError(f"Student {student_id} not found.")
        
        student = self.students[student_id]
        report = {
            "student_name": student.name,
            "student_id": student.person_id,
            "courses": [],
            "cgpa": 0.0
        }
        total_points = 0.0
        total_credits = 0.0
        for cid, data in student.enrolled_courses.items():
            course = self.courses.get(cid)
            if not course:
                continue
            teacher_name = "Unassigned"
            if course.teacher_id and course.teacher_id in self.teachers:
                teacher_name = self.teachers[course.teacher_id].name

            # units list
            units_info = []
            course_points = 0.0
            course_credits = 0.0
            for u in course.units:
                uid = u.get('unit_id')
                uname = u.get('name')
                ucredits = u.get('credits', 0)
                ugrade = data.get('units', {}).get(uid)
                if ugrade is None or ugrade == '':
                    letter = 'N/A'
                    point = None
                else:
                    letter = self.grade_to_letter(float(ugrade))
                    point = self.grade_to_point(float(ugrade))
                    if point is not None:
                        course_points += point * ucredits
                        course_credits += ucredits
                # determine teacher for this unit if present
                teacher_name = 'Unassigned'
                tid = u.get('teacher_id') or None
                if tid and tid in self.teachers:
                    teacher_name = self.teachers[tid].name
                units_info.append({ 'unit_id': uid, 'unit_name': uname, 'credits': ucredits, 'grade': ugrade, 'letter': letter, 'point': point, 'teacher': teacher_name })

            course_gpa = (course_points / course_credits) if course_credits else 0.0
            # accumulate for cgpa
            total_points += course_points
            total_credits += course_credits

            report['courses'].append({ 'course_id': cid, 'course_name': course.name, 'credits': course.credits, 'teacher': teacher_name, 'units': units_info, 'course_gpa': course_gpa })

        report['cgpa'] = (total_points / total_credits) if total_credits else 0.0
        return report

    def get_analytics(self):
        """Get analytics data for visualizations."""
        analytics = {
            "total_students": len(self.students),
            "total_courses": len(self.courses),
            "total_teachers": len(self.teachers),
            "avg_grade": self._calculate_avg_grade(),
            "students_per_course": self._get_students_per_course(),
            "grades_distribution": self._get_grades_distribution(),
            "teacher_workload": self._get_teacher_workload()
        }
        return analytics

    def _calculate_avg_grade(self):
        """Calculate average grade across all students."""
        grades = []
        for student in self.students.values():
            for course_data in student.enrolled_courses.values():
                for grade in course_data.get('units', {}).values():
                    if grade is not None and isinstance(grade, (int, float)):
                        grades.append(grade)
        return sum(grades) / len(grades) if grades else 0

    def _get_students_per_course(self):
        """Get count of students per course."""
        data = {}
        for course_id, course in self.courses.items():
            count = sum(1 for s in self.students.values() if course_id in s.enrolled_courses and s.enrolled_courses[course_id].get('units'))
            data[course.name] = count
        return data

    def _get_grades_distribution(self):
        """Get distribution of grades by letter grade (A, B+, B, C+, C, D+, D, F)."""
        buckets = {'A': 0, 'B+': 0, 'B': 0, 'C+': 0, 'C': 0, 'D+': 0, 'D': 0, 'F': 0}
        for student in self.students.values():
            for course_data in student.enrolled_courses.values():
                for grade in course_data.get('units', {}).values():
                    if grade is not None and isinstance(grade, (int, float)):
                        letter = self.grade_to_letter(float(grade))
                        if letter in buckets:
                            buckets[letter] += 1
        return buckets

    def _get_teacher_workload(self):
        """Get number of dedicated units per teacher."""
        data = {}
        for teacher in self.teachers.values():
            taught_units = getattr(teacher, 'taught_units', {}) or {}
            count = sum(len(units) for units in taught_units.values())
            data[teacher.name] = count
        return data

    def grade_to_letter(self, grade):
        if grade < 50:
            return 'F'
        if grade >= 85:
            return 'A'
        if grade >= 80:
            return 'B+'
        if grade >= 70:
            return 'B'
        if grade >= 65:
            return 'C+'
        if grade >= 60:
            return 'C'
        if grade >= 55:
            return 'D+'
        if grade >= 50:
            return 'D'

    def grade_to_point(self, grade):
        # Mapping to a 4.0 scale
        if grade < 50:
            return 0.0
        if grade >= 85:
            return 4.0
        if grade >= 80:
            return 3.5
        if grade >= 70:
            return 3.0
        if grade >= 65:
            return 2.5
        if grade >= 60:
            return 2.0
        if grade >= 55:
            return 1.5
        if grade >= 50:
            return 1.0
        return 0.0

    def save_data(self):
        """Save all data to CSV files."""
        # Save students
        with open(self.students_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['StudentID', 'Name', 'Email'])
            for student in self.students.values():
                writer.writerow([student.person_id, student.name, student.email])
        
        # Save courses (including units as JSON in a column)
        with open(self.courses_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['CourseID', 'Name', 'Credits', 'TeacherID', 'Units'])
            for course in self.courses.values():
                units_json = json.dumps(course.units)
                writer.writerow([course.course_id, course.name, course.credits, course.teacher_id or '', units_json])
        
        # Save teachers
        with open(self.teachers_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['TeacherID', 'Name', 'Email', 'Department'])
            for teacher in self.teachers.values():
                writer.writerow([teacher.person_id, teacher.name, teacher.email, teacher.department])
        
        # Save enrollments at unit level
        with open(self.enrollments_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['StudentID', 'CourseID', 'UnitID', 'Grade'])
            for student_id, student in self.students.items():
                for course_id, data in student.enrolled_courses.items():
                    for unit_id, grade in data.get('units', {}).items():
                        writer.writerow([student_id, course_id, unit_id, grade if grade is not None else ''])

    def load_data(self):
        """Load all data from CSV files."""
        # Load students
        if os.path.exists(self.students_file):
            try:
                with open(self.students_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['StudentID']:
                            student = Student(row['StudentID'], row['Name'], row['Email'])
                            self.students[row['StudentID']] = student
            except Exception as e:
                print(f"Error loading students: {e}")
        
        # Load courses
        if os.path.exists(self.courses_file):
            try:
                with open(self.courses_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['CourseID']:
                            units = []
                            try:
                                units = json.loads(row.get('Units', '[]') or '[]')
                            except Exception:
                                units = []
                            course = Course(row['CourseID'], row['Name'], int(row['Credits']), row.get('TeacherID') or None, units)
                            self.courses[row['CourseID']] = course
            except Exception as e:
                print(f"Error loading courses: {e}")
        
        # Load teachers
        if os.path.exists(self.teachers_file):
            try:
                with open(self.teachers_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['TeacherID']:
                            teacher = Teacher(row['TeacherID'], row['Name'], 
                                            row['Email'], row.get('Department', ''))
                            self.teachers[row['TeacherID']] = teacher
            except Exception as e:
                print(f"Error loading teachers: {e}")

        # Link course assignments to teachers
        for course in self.courses.values():
            if course.teacher_id and course.teacher_id in self.teachers:
                self.teachers[course.teacher_id].assign_course(course.course_id)
        
        # Load enrollments
        if os.path.exists(self.enrollments_file):
            try:
                with open(self.enrollments_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        sid = row.get('StudentID')
                        cid = row.get('CourseID')
                        uid = row.get('UnitID')
                        grade = row.get('Grade')
                        if sid in self.students and cid in self.courses and uid:
                            student = self.students[sid]
                            # ensure course enrollment exists
                            if cid not in student.enrolled_courses:
                                student.enrolled_courses[cid] = { 'units': {} }
                            student.enrolled_courses[cid]['units'][uid] = (float(grade) if grade else None)
            except Exception as e:
                print(f"Error loading enrollments: {e}")
