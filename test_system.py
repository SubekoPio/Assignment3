import os
import pytest
from system import EducationSystem


def test_edu_system(tmp_path):
    students_file = tmp_path / 'students_data.csv'
    courses_file = tmp_path / 'courses_data.csv'
    teachers_file = tmp_path / 'teachers_data.csv'
    enrollments_file = tmp_path / 'enrollments_data.csv'

    system = EducationSystem(
        students_file=str(students_file),
        courses_file=str(courses_file),
        teachers_file=str(teachers_file),
        enrollments_file=str(enrollments_file)
    )

    system.add_student('S001', 'John Doe', 'john@example.com')
    system.add_course('CS101', 'Intro to Python', 3)
    system.add_course_unit('CS101', 'U1', 'Basics', 2)
    system.add_course_unit('CS101', 'U2', 'Advanced', 1)

    system.add_teacher('T001', 'Jane Smith', 'jane@example.com', 'Computer Science')
    system.assign_teacher_to_unit('T001', 'CS101', 'U1')

    system.enroll_student_unit('S001', 'CS101', 'U1')
    system.enroll_student_unit('S001', 'CS101', 'U2')
    system.assign_unit_grade('S001', 'CS101', 'U1', 80.0)
    system.assign_unit_grade('S001', 'CS101', 'U2', 90.0)

    system.save_data()

    new_system = EducationSystem(
        students_file=str(students_file),
        courses_file=str(courses_file),
        teachers_file=str(teachers_file),
        enrollments_file=str(enrollments_file)
    )

    assert 'S001' in new_system.students
    assert 'CS101' in new_system.courses
    report = new_system.get_student_report('S001')
    assert report['student_name'] == 'John Doe'
    assert len(report['courses']) == 1
    assert report['courses'][0]['course_name'] == 'Intro to Python'
    assert abs(report['courses'][0]['course_gpa'] - 3.6666666) < 0.001
    assert abs(report['cgpa'] - 3.6666666) < 0.001


def test_multiple_course_teachers_and_unit_assignment_persist(tmp_path):
    students_file = tmp_path / 'students_data.csv'
    courses_file = tmp_path / 'courses_data.csv'
    teachers_file = tmp_path / 'teachers_data.csv'
    enrollments_file = tmp_path / 'enrollments_data.csv'

    system = EducationSystem(
        students_file=str(students_file),
        courses_file=str(courses_file),
        teachers_file=str(teachers_file),
        enrollments_file=str(enrollments_file)
    )

    system.add_course('CS201', 'Systems Programming', 4)
    system.add_course_unit('CS201', 'U1', 'Processes', 2)
    system.add_course_unit('CS201', 'U2', 'Files', 2)
    system.add_teacher('T001', 'Jane Smith', 'jane@example.com', 'Computer Science')
    system.add_teacher('T002', 'Mary Jones', 'mary@example.com', 'Computer Science')
    system.add_teacher('T003', 'Alex Lee', 'alex@example.com', 'Computer Science')

    system.assign_teacher_to_course('T001', 'CS201')
    system.assign_teacher_to_course('T002', 'CS201')
    assert system.courses['CS201'].teacher_ids == ['T001', 'T002']

    system.assign_teacher_to_unit('T002', 'CS201', 'U1')
    system.assign_teacher_to_unit('T003', 'CS201', 'U2')

    assert system.courses['CS201'].has_teacher('T003')
    assert system.courses['CS201'].units[0]['teacher_id'] == 'T002'
    assert system.courses['CS201'].units[1]['teacher_id'] == 'T003'

    system.save_data()
    reloaded = EducationSystem(
        students_file=str(students_file),
        courses_file=str(courses_file),
        teachers_file=str(teachers_file),
        enrollments_file=str(enrollments_file)
    )

    assert reloaded.courses['CS201'].teacher_ids == ['T001', 'T002', 'T003']
    assert reloaded.courses['CS201'].units[0]['teacher_id'] == 'T002'
    assert reloaded.courses['CS201'].units[1]['teacher_id'] == 'T003'
    assert 'CS201' in reloaded.teachers['T002'].assigned_courses
    assert reloaded.teachers['T002'].taught_units['CS201'] == ['U1']


def test_unit_id_must_be_unique(tmp_path):
    system = EducationSystem(
        students_file=str(tmp_path / 'students_data.csv'),
        courses_file=str(tmp_path / 'courses_data.csv'),
        teachers_file=str(tmp_path / 'teachers_data.csv'),
        enrollments_file=str(tmp_path / 'enrollments_data.csv')
    )

    system.add_course('CS101', 'Intro to Python', 3)
    system.add_course('CS102', 'Data Structures', 3)
    system.add_course_unit('CS101', 'U1', 'Basics', 2)

    with pytest.raises(ValueError, match="Unit ID U1 already exists"):
        system.add_course_unit('CS101', 'U1', 'Duplicate Basics', 1)

    with pytest.raises(ValueError, match="Unit ID U1 already exists"):
        system.add_course_unit('CS102', 'U1', 'Another Course Unit', 1)


def test_deleting_unit_unassigns_it_from_teachers(tmp_path):
    system = EducationSystem(
        students_file=str(tmp_path / 'students_data.csv'),
        courses_file=str(tmp_path / 'courses_data.csv'),
        teachers_file=str(tmp_path / 'teachers_data.csv'),
        enrollments_file=str(tmp_path / 'enrollments_data.csv')
    )

    system.add_course('CS101', 'Intro to Python', 3)
    system.add_course_unit('CS101', 'U1', 'Basics', 2)
    system.add_course_unit('CS101', 'U2', 'Advanced', 1)
    system.add_teacher('T001', 'Jane Smith', 'jane@example.com', 'Computer Science')
    system.add_teacher('T002', 'Mary Jones', 'mary@example.com', 'Computer Science')
    system.assign_teacher_to_unit('T001', 'CS101', 'U1')
    system.teachers['T002'].assign_unit('CS101', 'U1')

    system.delete_course_unit('CS101', 'U1')

    assert all(
        'U1' not in teacher.taught_units.get('CS101', [])
        for teacher in system.teachers.values()
    )
    assert [unit['unit_id'] for unit in system.courses['CS101'].units] == ['U2']


if __name__ == '__main__':
    import pytest
    pytest.main([str(os.path.abspath(__file__))])
