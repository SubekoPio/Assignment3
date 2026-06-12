class Person:
    """Base class for people in the system."""
    def __init__(self, person_id, name, email):
        self._person_id = person_id
        self._name = name
        self._email = email

    @property
    def person_id(self):
        return self._person_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._email = value

    def to_dict(self):
        return {
            "id": self._person_id,
            "name": self._name,
            "email": self._email
        }


class Student(Person):
    """Student class inheriting from Person."""
    def __init__(self, person_id, name, email):
        super().__init__(person_id, name, email)
        # enrolled_courses: course_id -> { 'units': { unit_id: grade_or_None } }
        self.enrolled_courses = {}

    def enroll(self, course_id):
        if course_id not in self.enrolled_courses:
            self.enrolled_courses[course_id] = { 'units': {} }

    def enroll_unit(self, course_id, unit_id):
        if course_id not in self.enrolled_courses:
            self.enroll(course_id)
        units = self.enrolled_courses[course_id].get('units', {})
        if unit_id not in units:
            units[unit_id] = None
        self.enrolled_courses[course_id]['units'] = units

    def assign_grade(self, course_id, grade):
        # Deprecated: use assign_unit_grade for unit-level grades
        if course_id in self.enrolled_courses:
            # set overall marker
            self.enrolled_courses[course_id].setdefault('overall', None)
            self.enrolled_courses[course_id]['overall'] = grade
        else:
            raise ValueError(f"Student is not enrolled in course {course_id}")

    def assign_unit_grade(self, course_id, unit_id, grade):
        if course_id in self.enrolled_courses:
            units = self.enrolled_courses[course_id].get('units', {})
            if unit_id in units:
                units[unit_id] = grade
                self.enrolled_courses[course_id]['units'] = units
            else:
                raise ValueError(f"Student is not enrolled in unit {unit_id} for course {course_id}")
        else:
            raise ValueError(f"Student is not enrolled in course {course_id}")

    def to_dict(self):
        data = super().to_dict()
        data["enrolled_courses"] = self.enrolled_courses
        return data

    @classmethod
    def from_dict(cls, data):
        student = cls(data["id"], data["name"], data["email"])
        student.enrolled_courses = data.get("enrolled_courses", {})
        return student


class Teacher(Person):
    """Teacher class inheriting from Person."""
    def __init__(self, person_id, name, email, department=""):
        super().__init__(person_id, name, email)
        self.department = department
        # taught_units: course_id -> list of unit_ids
        self.taught_units = {}

    def assign_course(self, course_id):
        # legacy support: mark teacher as teaching a course (no specific unit)
        if course_id not in self.taught_units:
            self.taught_units[course_id] = []

    def assign_unit(self, course_id, unit_id):
        if course_id not in self.taught_units:
            self.taught_units[course_id] = []
        if unit_id not in self.taught_units[course_id]:
            self.taught_units[course_id].append(unit_id)

    def remove_course(self, course_id):
        if course_id in self.taught_units:
            del self.taught_units[course_id]

    def remove_unit(self, course_id, unit_id):
        if course_id in self.taught_units and unit_id in self.taught_units[course_id]:
            self.taught_units[course_id].remove(unit_id)
            if not self.taught_units[course_id]:
                del self.taught_units[course_id]

    def to_dict(self):
        data = super().to_dict()
        data["department"] = self.department
        data["taught_units"] = self.taught_units
        return data

    @classmethod
    def from_dict(cls, data):
        teacher = cls(data["id"], data["name"], data["email"], data.get("department", ""))
        teacher.taught_units = data.get("taught_units", {})
        return teacher


class Course:
    """Course class representing an educational course."""
    def __init__(self, course_id, name, credits, teacher_id=None, units=None):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.teacher_id = teacher_id
        # units: list of dicts { 'unit_id', 'name', 'credits' }
        self.units = units or []

    def add_unit(self, unit_id, name, credits):
        self.units.append({ 'unit_id': unit_id, 'name': name, 'credits': credits, 'teacher_id': None })

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "name": self.name,
            "credits": self.credits,
            "teacher_id": self.teacher_id,
            "units": self.units
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["course_id"], data["name"], data["credits"], data.get("teacher_id"), data.get("units", []))


class Unit:
    def __init__(self, unit_id, name, credits):
        self.unit_id = unit_id
        self.name = name
        self.credits = credits

    def to_dict(self):
        return { 'unit_id': self.unit_id, 'name': self.name, 'credits': self.credits }

    @classmethod
    def from_dict(cls, data):
        return cls(data['unit_id'], data.get('name', ''), data.get('credits', 0))
