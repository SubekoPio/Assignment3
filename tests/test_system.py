import os
from tempfile import TemporaryDirectory
import pytest
from system import EducationSystem


def test_unit_enrollment_and_gpa(tmp_path):
    # Use temp files for persistence
    td = tmp_path
    sys = EducationSystem()
    sys.students_file = str(td / 'students.csv')
    sys.courses_file = str(td / 'courses.csv')
    sys.teachers_file = str(td / 'teachers.csv')
    sys.enrollments_file = str(td / 'enrollments.csv')

    # Clear in-memory
    sys.students = {}
    sys.courses = {}
    sys.teachers = {}

    # Create course and units
    sys.add_course('C1', 'Course One', 3)
    sys.add_course_unit('C1', 'U1', 'Unit One', 2)
    sys.add_course_unit('C1', 'U2', 'Unit Two', 1)

    # Add teacher and assign to unit
    sys.add_teacher('T1', 'Teach One', 't1@example.com')
    sys.assign_teacher_to_unit('T1', 'C1', 'U1')

    # Add student and enroll units
    sys.add_student('1', 'Alice', 'a@example.com')
    sys.enroll_student_unit('1', 'C1', 'U1')
    sys.enroll_student_unit('1', 'C1', 'U2')

    # Assign grades
    sys.assign_unit_grade('1', 'C1', 'U1', 80.0)
    sys.assign_unit_grade('1', 'C1', 'U2', 90.0)

    # Save and reload
    sys.save_data()
    # create a fresh instance to load from disk
    sys2 = EducationSystem()
    sys2.students_file = sys.students_file
    sys2.courses_file = sys.courses_file
    sys2.teachers_file = sys.teachers_file
    sys2.enrollments_file = sys.enrollments_file
    sys2.students = {}
    sys2.courses = {}
    sys2.teachers = {}
    # load explicitly from the temp files
    sys2.load_data()

    # Re-link teachers (load_data assigns teacher->course links)
    # Compute report
    report = sys.get_student_report('1')
    assert report['student_id'] == '1'
    assert len(report['courses']) == 1
    course = report['courses'][0]
    # course_gpa should be close to ((3.5*2)+(4.0*1))/3 == 3.666...
    assert abs(course['course_gpa'] - 3.6666666) < 0.001
    assert abs(report['cgpa'] - 3.6666666) < 0.001


def test_multiple_course_teachers_and_unit_assignment_persist(tmp_path):
    sys = EducationSystem(
        students_file=str(tmp_path / 'students.csv'),
        courses_file=str(tmp_path / 'courses.csv'),
        teachers_file=str(tmp_path / 'teachers.csv'),
        enrollments_file=str(tmp_path / 'enrollments.csv')
    )

    sys.add_course('C1', 'Course One', 3)
    sys.add_course_unit('C1', 'U1', 'Unit One', 1)
    sys.add_course_unit('C1', 'U2', 'Unit Two', 2)
    sys.add_teacher('T1', 'Teach One', 't1@example.com')
    sys.add_teacher('T2', 'Teach Two', 't2@example.com')
    sys.add_teacher('T3', 'Teach Three', 't3@example.com')

    sys.assign_teacher_to_course('T1', 'C1')
    sys.assign_teacher_to_course('T2', 'C1')
    sys.assign_teacher_to_unit('T2', 'C1', 'U1')
    sys.assign_teacher_to_unit('T3', 'C1', 'U2')

    assert sys.courses['C1'].teacher_ids == ['T1', 'T2', 'T3']
    assert sys.courses['C1'].units[0]['teacher_id'] == 'T2'
    assert sys.courses['C1'].units[1]['teacher_id'] == 'T3'

    sys.save_data()
    loaded = EducationSystem(
        students_file=sys.students_file,
        courses_file=sys.courses_file,
        teachers_file=sys.teachers_file,
        enrollments_file=sys.enrollments_file
    )

    assert loaded.courses['C1'].teacher_ids == ['T1', 'T2', 'T3']
    assert loaded.teachers['T2'].taught_units['C1'] == ['U1']


def test_unit_id_must_be_unique(tmp_path):
    sys = EducationSystem(
        students_file=str(tmp_path / 'students.csv'),
        courses_file=str(tmp_path / 'courses.csv'),
        teachers_file=str(tmp_path / 'teachers.csv'),
        enrollments_file=str(tmp_path / 'enrollments.csv')
    )

    sys.add_course('C1', 'Course One', 3)
    sys.add_course('C2', 'Course Two', 3)
    sys.add_course_unit('C1', 'U1', 'Unit One', 1)

    with pytest.raises(ValueError, match="Unit ID U1 already exists"):
        sys.add_course_unit('C1', 'U1', 'Duplicate Unit', 1)

    with pytest.raises(ValueError, match="Unit ID U1 already exists"):
        sys.add_course_unit('C2', 'U1', 'Duplicate Across Course', 1)


def test_deleting_unit_unassigns_it_from_teachers(tmp_path):
    sys = EducationSystem(
        students_file=str(tmp_path / 'students.csv'),
        courses_file=str(tmp_path / 'courses.csv'),
        teachers_file=str(tmp_path / 'teachers.csv'),
        enrollments_file=str(tmp_path / 'enrollments.csv')
    )

    sys.add_course('C1', 'Course One', 3)
    sys.add_course_unit('C1', 'U1', 'Unit One', 1)
    sys.add_course_unit('C1', 'U2', 'Unit Two', 2)
    sys.add_teacher('T1', 'Teach One', 't1@example.com')
    sys.add_teacher('T2', 'Teach Two', 't2@example.com')
    sys.assign_teacher_to_unit('T1', 'C1', 'U1')
    sys.teachers['T2'].assign_unit('C1', 'U1')

    sys.delete_course_unit('C1', 'U1')

    assert all(
        'U1' not in teacher.taught_units.get('C1', [])
        for teacher in sys.teachers.values()
    )
    assert [unit['unit_id'] for unit in sys.courses['C1'].units] == ['U2']
