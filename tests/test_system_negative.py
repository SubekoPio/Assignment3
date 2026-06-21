from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from system import EducationSystem


TEST_SCOPE = {
    "Core service": "EducationSystem in system.py",
    "Validation rules": "Existence checks, uniqueness, precondition checks",
    "Error handling": "Expected ValueError paths for invalid operations",
    "Domain operations": "Student/Course/Teacher/Unit API guardrails",
}


def make_system(tmp_path):
    return EducationSystem(
        students_file=str(tmp_path / "students.csv"),
        courses_file=str(tmp_path / "courses.csv"),
        teachers_file=str(tmp_path / "teachers.csv"),
        enrollments_file=str(tmp_path / "enrollments.csv"),
    )


def test_add_duplicate_course_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_course("C1", "Programming", 3)
    with pytest.raises(ValueError, match="already exists"):
        sys_obj.add_course("C1", "Programming 2", 4)


def test_add_duplicate_teacher_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_teacher("T1", "Dr. Green", "green@example.com")
    with pytest.raises(ValueError, match="already exists"):
        sys_obj.add_teacher("T1", "Dr. Blue", "blue@example.com")


def test_assign_teacher_to_missing_course_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_teacher("T1", "Dr. Green", "green@example.com")
    with pytest.raises(ValueError, match="Course C999 not found"):
        sys_obj.assign_teacher_to_course("T1", "C999")


def test_assign_missing_teacher_to_course_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_course("C1", "Programming", 3)
    with pytest.raises(ValueError, match="Teacher T999 not found"):
        sys_obj.assign_teacher_to_course("T999", "C1")


def test_assign_teacher_to_missing_unit_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_teacher("T1", "Dr. Green", "green@example.com")
    sys_obj.add_course("C1", "Programming", 3)
    with pytest.raises(ValueError, match="Unit U999 not found"):
        sys_obj.assign_teacher_to_unit("T1", "C1", "U999")


def test_enroll_student_missing_student_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_course("C1", "Programming", 3)
    sys_obj.add_course_unit("C1", "U1", "Python Basics", 2)
    with pytest.raises(ValueError, match="Student S999 not found"):
        sys_obj.enroll_student_unit("S999", "C1", "U1")


def test_enroll_student_missing_course_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_student("S1", "Alice", "alice@example.com")
    with pytest.raises(ValueError, match="Course C999 not found"):
        sys_obj.enroll_student_unit("S1", "C999", "U1")


def test_enroll_student_missing_unit_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_student("S1", "Alice", "alice@example.com")
    sys_obj.add_course("C1", "Programming", 3)
    with pytest.raises(ValueError, match="Unit U999 not found"):
        sys_obj.enroll_student_unit("S1", "C1", "U999")


def test_assign_grade_without_enrollment_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_student("S1", "Alice", "alice@example.com")
    sys_obj.add_course("C1", "Programming", 3)
    sys_obj.add_course_unit("C1", "U1", "Python Basics", 2)
    with pytest.raises(ValueError, match="not enrolled"):
        sys_obj.assign_unit_grade("S1", "C1", "U1", 80)


def test_remove_nonexistent_unit_enrollment_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_student("S1", "Alice", "alice@example.com")
    sys_obj.add_course("C1", "Programming", 3)
    sys_obj.add_course_unit("C1", "U1", "Python Basics", 2)
    sys_obj.enroll_student_unit("S1", "C1", "U1")
    with pytest.raises(ValueError, match="Unit U2 enrollment not found"):
        sys_obj.remove_unit_enrollment("S1", "C1", "U2")


def test_get_report_for_missing_student_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    with pytest.raises(ValueError, match="Student S404 not found"):
        sys_obj.get_student_report("S404")


def test_delete_missing_teacher_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    with pytest.raises(ValueError, match="Teacher T404 not found"):
        sys_obj.delete_teacher("T404")


def test_delete_missing_course_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    with pytest.raises(ValueError, match="Course C404 not found"):
        sys_obj.delete_course("C404")


def test_update_missing_student_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    with pytest.raises(ValueError, match="Student S404 not found"):
        sys_obj.update_student("S404", "Ghost", "ghost@example.com")


def test_update_missing_course_unit_raises(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_course("C1", "Programming", 3)
    with pytest.raises(ValueError, match="Unit U404 not found"):
        sys_obj.update_course_unit("C1", "U404", name="Nope", credits=1)


if __name__ == "__main__":
    print("\n=== test_system_negative.py: Detailed Run ===")
    print("Models/components under test:")
    for name, desc in TEST_SCOPE.items():
        print(f"- {name}: {desc}")
    print("\nRunning tests in verbose mode...\n")
    raise SystemExit(pytest.main([__file__, "-v", "-rA"]))
