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
