from pathlib import Path
import sys

import pytest

# Ensure project root is importable when running tests from workspace root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from system import EducationSystem


def make_system(tmp_path):
    return EducationSystem(
        students_file=str(tmp_path / "students.csv"),
        courses_file=str(tmp_path / "courses.csv"),
        teachers_file=str(tmp_path / "teachers.csv"),
        enrollments_file=str(tmp_path / "enrollments.csv"),
    )


def seed_basic_data(sys_obj):
    sys_obj.add_student("S1", "Alice", "alice@example.com")
    sys_obj.add_student("S2", "Bob", "bob@example.com")

    sys_obj.add_teacher("T1", "Dr. Green", "green@example.com", "CS")
    sys_obj.add_teacher("T2", "Dr. Blue", "blue@example.com", "Math")

    sys_obj.add_course("C1", "Programming", 3)
    sys_obj.add_course("C2", "Databases", 4)

    sys_obj.add_course_unit("C1", "U1", "Python Basics", 2)
    sys_obj.add_course_unit("C1", "U2", "Algorithms", 1)
    sys_obj.add_course_unit("C2", "U3", "SQL", 2)


def test_import_and_empty_initialization_with_temp_files(tmp_path):
    sys_obj = make_system(tmp_path)
    assert sys_obj.students == {}
    assert sys_obj.courses == {}
    assert sys_obj.teachers == {}


def test_next_id_generation(tmp_path):
    sys_obj = make_system(tmp_path)

    assert sys_obj.next_student_id() == "S1"
    assert sys_obj.next_teacher_id() == "T1"
    assert sys_obj.next_course_id() == "C1"

    sys_obj.add_student("S1", "Alice", "alice@example.com")
    sys_obj.add_teacher("T1", "Dr. Green", "green@example.com")
    sys_obj.add_course("C1", "Programming", 3)
    sys_obj.add_course_unit("C1", "U1", "Python Basics", 2)

    assert sys_obj.next_student_id() == "S2"
    assert sys_obj.next_teacher_id() == "T2"
    assert sys_obj.next_course_id() == "C2"
    assert sys_obj.next_unit_id() == "U2"


def test_crud_student_course_teacher(tmp_path):
    sys_obj = make_system(tmp_path)

    sys_obj.add_student("S1", "Alice", "alice@example.com")
    sys_obj.add_course("C1", "Programming", 3)
    sys_obj.add_teacher("T1", "Dr. Green", "green@example.com", "CS")

    with pytest.raises(ValueError, match="already exists"):
        sys_obj.add_student("S1", "Other", "other@example.com")

    sys_obj.update_student("S1", "Alice Updated", "alice.updated@example.com")
    assert sys_obj.students["S1"].name == "Alice Updated"

    with pytest.raises(ValueError, match="Invalid email format"):
        sys_obj.update_student("S1", "Alice Updated", "not-an-email")

    sys_obj.update_course("C1", "Programming I", 4)
    assert sys_obj.courses["C1"].credits == 4

    sys_obj.update_teacher("T1", "Dr. Green Updated", "green2@example.com", "Engineering")
    assert sys_obj.teachers["T1"].department == "Engineering"

    sys_obj.delete_student("S1")
    assert "S1" not in sys_obj.students


def test_unit_uniqueness_and_unit_update_delete(tmp_path):
    sys_obj = make_system(tmp_path)
    sys_obj.add_course("C1", "Programming", 3)
    sys_obj.add_course("C2", "Databases", 4)

    sys_obj.add_course_unit("C1", "U1", "Python Basics", 2)

    with pytest.raises(ValueError, match="Unit ID U1 already exists"):
        sys_obj.add_course_unit("C1", "U1", "Duplicate", 1)

    with pytest.raises(ValueError, match="Unit ID U1 already exists"):
        sys_obj.add_course_unit("C2", "U1", "Duplicate Global", 1)

    sys_obj.update_course_unit("C1", "U1", name="Python Intro", credits=3)
    unit = sys_obj.courses["C1"].units[0]
    assert unit["name"] == "Python Intro"
    assert unit["credits"] == 3

    sys_obj.delete_course_unit("C1", "U1")
    assert sys_obj.courses["C1"].units == []


def test_teacher_assignment_and_cleanup_on_delete_teacher(tmp_path):
    sys_obj = make_system(tmp_path)
    seed_basic_data(sys_obj)

    sys_obj.assign_teacher_to_course("T1", "C1")
    sys_obj.assign_teacher_to_course("T2", "C1")
    sys_obj.assign_teacher_to_unit("T1", "C1", "U1")
    sys_obj.assign_teacher_to_unit("T2", "C1", "U2")

    assert "T1" in sys_obj.courses["C1"].teacher_ids
    assert "T2" in sys_obj.courses["C1"].teacher_ids
    assert sys_obj.courses["C1"].units[0]["teacher_id"] == "T1"
    assert sys_obj.courses["C1"].units[1]["teacher_id"] == "T2"

    sys_obj.delete_teacher("T2")
    assert "T2" not in sys_obj.teachers
    assert "T2" not in sys_obj.courses["C1"].teacher_ids
    assert sys_obj.courses["C1"].units[1]["teacher_id"] is None


def test_unit_enrollment_grading_report_and_cgpa(tmp_path):
    sys_obj = make_system(tmp_path)
    seed_basic_data(sys_obj)

    sys_obj.assign_teacher_to_unit("T1", "C1", "U1")
    sys_obj.assign_teacher_to_unit("T2", "C1", "U2")

    sys_obj.enroll_student_unit("S1", "C1", "U1")
    sys_obj.enroll_student_unit("S1", "C1", "U2")
    sys_obj.assign_unit_grade("S1", "C1", "U1", 80.0)
    sys_obj.assign_unit_grade("S1", "C1", "U2", 90.0)

    report = sys_obj.get_student_report("S1")

    assert report["student_id"] == "S1"
    assert len(report["courses"]) == 1
    assert report["courses"][0]["course_id"] == "C1"

    # Expected course GPA: ((3.5 * 2) + (4.0 * 1)) / 3 = 3.6666...
    assert pytest.approx(report["courses"][0]["course_gpa"], rel=1e-4) == 3.6666666
    assert pytest.approx(report["cgpa"], rel=1e-4) == 3.6666666

    teacher_names = {u["teacher"] for u in report["courses"][0]["units"]}
    assert "Dr. Green" in teacher_names
    assert "Dr. Blue" in teacher_names


def test_remove_unit_enrollment_and_remove_course_enrollment(tmp_path):
    sys_obj = make_system(tmp_path)
    seed_basic_data(sys_obj)

    sys_obj.enroll_student_unit("S1", "C1", "U1")
    sys_obj.enroll_student_unit("S1", "C1", "U2")

    sys_obj.remove_unit_enrollment("S1", "C1", "U1")
    assert "U1" not in sys_obj.students["S1"].enrolled_courses["C1"]["units"]

    # Removing the last unit should remove whole course enrollment.
    sys_obj.remove_unit_enrollment("S1", "C1", "U2")
    assert "C1" not in sys_obj.students["S1"].enrolled_courses

    sys_obj.enroll_student_unit("S1", "C2", "U3")
    sys_obj.remove_enrollment("S1", "C2")
    assert "C2" not in sys_obj.students["S1"].enrolled_courses


def test_delete_course_unit_cascades_student_and_teacher_links(tmp_path):
    sys_obj = make_system(tmp_path)
    seed_basic_data(sys_obj)

    sys_obj.assign_teacher_to_unit("T1", "C1", "U1")
    sys_obj.assign_teacher_to_unit("T2", "C1", "U2")

    sys_obj.enroll_student_unit("S1", "C1", "U1")
    sys_obj.enroll_student_unit("S1", "C1", "U2")

    sys_obj.delete_course_unit("C1", "U1")

    assert all("U1" not in t.taught_units.get("C1", []) for t in sys_obj.teachers.values())
    remaining_unit_ids = [u["unit_id"] for u in sys_obj.courses["C1"].units]
    assert remaining_unit_ids == ["U2"]
    assert "U1" not in sys_obj.students["S1"].enrolled_courses["C1"]["units"]


def test_analytics_counts_distribution_and_workload(tmp_path):
    sys_obj = make_system(tmp_path)
    seed_basic_data(sys_obj)

    sys_obj.assign_teacher_to_unit("T1", "C1", "U1")
    sys_obj.assign_teacher_to_unit("T2", "C1", "U2")
    sys_obj.assign_teacher_to_unit("T2", "C2", "U3")

    sys_obj.enroll_student_unit("S1", "C1", "U1")
    sys_obj.enroll_student_unit("S1", "C1", "U2")
    sys_obj.enroll_student_unit("S2", "C2", "U3")

    sys_obj.assign_unit_grade("S1", "C1", "U1", 88.0)  # A
    sys_obj.assign_unit_grade("S1", "C1", "U2", 72.0)  # B
    sys_obj.assign_unit_grade("S2", "C2", "U3", 49.0)  # F

    analytics = sys_obj.get_analytics()

    assert analytics["total_students"] == 2
    assert analytics["total_courses"] == 2
    assert analytics["total_teachers"] == 2
    assert analytics["students_per_course"]["Programming"] == 1
    assert analytics["students_per_course"]["Databases"] == 1
    assert analytics["grades_distribution"]["A"] == 1
    assert analytics["grades_distribution"]["B"] == 1
    assert analytics["grades_distribution"]["F"] == 1
    assert analytics["teacher_workload"]["Dr. Green"] == 1
    assert analytics["teacher_workload"]["Dr. Blue"] == 2


def test_save_load_round_trip_persists_links_and_grades(tmp_path):
    sys_obj = make_system(tmp_path)
    seed_basic_data(sys_obj)

    sys_obj.assign_teacher_to_course("T1", "C1")
    sys_obj.assign_teacher_to_course("T2", "C1")
    sys_obj.assign_teacher_to_unit("T2", "C1", "U2")

    sys_obj.enroll_student_unit("S1", "C1", "U1")
    sys_obj.enroll_student_unit("S1", "C1", "U2")
    sys_obj.assign_unit_grade("S1", "C1", "U1", 85.0)

    sys_obj.save_data()

    loaded = EducationSystem(
        students_file=sys_obj.students_file,
        courses_file=sys_obj.courses_file,
        teachers_file=sys_obj.teachers_file,
        enrollments_file=sys_obj.enrollments_file,
    )

    assert loaded.courses["C1"].teacher_ids == ["T1", "T2"]
    assert loaded.teachers["T2"].taught_units["C1"] == ["U2"]
    assert loaded.students["S1"].enrolled_courses["C1"]["units"]["U1"] == 85.0
    assert loaded.students["S1"].enrolled_courses["C1"]["units"]["U2"] is None


def test_delete_course_cleans_student_and_teacher_links(tmp_path):
    sys_obj = make_system(tmp_path)
    seed_basic_data(sys_obj)

    sys_obj.assign_teacher_to_course("T1", "C1")
    sys_obj.enroll_student_unit("S1", "C1", "U1")

    sys_obj.delete_course("C1")

    assert "C1" not in sys_obj.courses
    assert "C1" not in sys_obj.students["S1"].enrolled_courses
    assert "C1" not in sys_obj.teachers["T1"].assigned_courses


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
