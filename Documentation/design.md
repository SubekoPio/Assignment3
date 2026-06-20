# EduManage: Education Management System Design

## 1. Problem Description and Justification
Educational institutions often struggle with managing student records, course enrollments, and grading using manual paper-based methods or disjointed spreadsheets. This leads to data inconsistency, loss of records, and inefficiencies in generating student reports. A centralized, automated system is required to streamline these processes.

## 2. Objectives
- To provide a user-friendly, menu-driven interface for managing students and courses.
- To allow enrollment of students into specific courses.
- To enable grading and generation of student report cards.
- To ensure data persistence using file handling (JSON).
- To demonstrate key Python programming concepts including OOP (inheritance, encapsulation), error handling, and data structures.

## 3. System Architecture and Data Structures
### Classes
- **`Person` (Base Class)**: Encapsulates common attributes like `person_id`, `name`, and `email`.
- **`Student` (Derived Class)**: Inherits from `Person`. Adds attributes for `enrolled_courses` (dictionary mapping course ID to grade).
- **`Course`**: Represents a course with `course_id`, `name`, and `credits`.
- **`EducationSystem`**: The main controller class that manages lists of students and courses, handles file I/O, and contains the business logic.

### Data Structures
- **Lists**: Used to store collections of `Student` and `Course` objects.
- **Dictionaries**: Used within the `Student` class to map `course_id` to `grade`, and for JSON serialization.

### File Handling
- Data will be saved to and loaded from `data.json` to ensure persistence across sessions.

## 4. Modules
- **Data Models**: `models.py` containing `Person`, `Student`, and `Course`.
- **System Controller**: `system.py` containing `EducationSystem`.
- **Main Application**: `main.py` containing the menu-driven CLI and user input validation.

## 2026-06 Maintenance Update
- Added complete course unit management workflow in the main GUI (add, edit, delete via manage-units dialog).
- Fixed enrollment logic to use explicit unit selection so students can only enroll into selected units.
- Improved teacher-course-unit consistency with persisted multi-teacher tracking (teacher_ids) and cleaned unlink logic on delete.
- Fixed report tab generation/export by using the correct report API and stable PDF export from rendered report text.
- Updated CSV storage model: courses_data.csv now includes TeacherIDs; enrollments_data.csv stores unit-level rows (StudentID, CourseID, UnitID, Grade).
- Validation status: automated tests pass (8/8).

## 2026-06 UI Polish Update
- Increased analysis chart text sizes (titles, axis labels, ticks, and stats panel) for readability.
- Improved table readability with larger TreeView typography and row heights.
- Enhanced dark/light theme switching to rebuild tab content cleanly for smoother visual transitions.
- Upgraded course unit management dialog to a fully themed interface with styled CRUD controls and larger fonts.

