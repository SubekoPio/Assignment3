# EduManage GUI Design

## 1. Visual Theme
- **Primary Color**: `#2C3E50` (Dark Blue/Grey for Headers)
- **Secondary Color**: `#3498DB` (Bright Blue for Buttons)
- **Background Color**: `#ECF0F1` (Light Grey for main window)
- **Accent Color**: `#E74C3C` (Red for delete/exit actions)
- **Font**: `Helvetica` or `Arial` for a clean, modern look.

## 2. Layout Structure
- **Main Window**: A tabbed interface (using `ttk.Notebook`) to separate different functionalities:
    - **Dashboard**: Overview of total students and courses.
    - **Students**: Table view of students with "Add" and "Delete" buttons.
    - **Courses**: Table view of courses with "Add" and "Delete" buttons.
    - **Enrollment & Grading**: Interface to select students and courses for enrollment and grade assignment.
    - **Reports**: Searchable interface to generate and view student report cards.

## 3. UI Components
- **`ttk.Treeview`**: For displaying lists of students and courses in a table format.
- **`tk.Button`**: Styled with custom colors and padding.
- **`tk.Entry`**: For data input with clear labels.
- **`messagebox`**: For error handling and confirmation dialogs.

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
- Replaced the previous dark-oriented styling with a modern light-first theme system and larger baseline UI fonts.
- Upgraded course unit management dialog to a fully themed interface with styled CRUD controls and larger fonts.
- Fixed the Courses tab split-view initialization so Course Units are visible by default.
- Restyled Enrollment cards/headings to align with the app-wide tab design.
- Added teacher snapshot selector and combined student/teacher detail readouts in Analysis.

