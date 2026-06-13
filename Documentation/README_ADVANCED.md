# EduManage Advanced Education Management System

## Overview
EduManage is an advanced education management system built with Python and Tkinter. It provides comprehensive management of students, courses, teachers, enrollments, grades, and detailed analytics with visualizations.

## System Features

### 1. **CSV-Based Data Storage**
- Replaced JSON with CSV format for better data management and scalability
- Separate CSV files for each data type:
  - `students_data.csv` - Student information
  - `courses_data.csv` - Course details with teacher assignments
  - `teachers_data.csv` - Teacher information and departments
  - `enrollments_data.csv` - Student-course enrollments and grades

### 2. **Teacher Management**
- Add, manage, and track teacher information
- Assign teachers to multiple courses
- Track teacher workload (number of courses taught)
- Department assignment for organizational purposes
- View teacher details including all assigned courses

      ScreenShot
        ![Project Screenshot](images/teachers_tab.png)


### 3. **Teacher-Course Assignment**
- Assign teachers to courses directly from the GUI
- Automatic removal of previous teacher assignments when reassigning
- Automatic tracking of taught courses per teacher
- Display assigned teacher in course details

### 4. **Enhanced Reporting**
- Student reports now include assigned teacher information
- Comprehensive course details with teacher names
- Grade tracking and history

### 5. **Analytics & Visualization Dashboard**
The new Analysis tab provides:
- **Students per Course**: Bar chart showing enrollment distribution
- **Grade Distribution**: Histogram of grades across all students
- **Teacher Workload**: Horizontal bar chart showing courses per teacher
- **System Statistics**: Overall metrics including:
  - Total number of students
  - Total number of courses
  - Total number of teachers
  - System-wide average grade

## File Structure

```
Intermediate Education System in Python Based on PDF Guidelines/
├── gui_main.py                 # Main GUI application
├── system.py                   # Core system logic (CSV storage)
├── models.py                   # Data models (Student, Course, Teacher)
├── students_data.csv           # Student records
├── courses_data.csv            # Course records with teacher assignments
├── teachers_data.csv           # Teacher records
├── enrollments_data.csv        # Student enrollments and grades
└── README_ADVANCED.md          # This file
```

## Installation

### Requirements
```
tkinter              # Usually comes with Python
matplotlib           # For data visualization
```

### Install Dependencies
```bash
pip install matplotlib
```

### Run the Application
```bash
python gui_main.py
```

## User Guide

### Students Tab
- **Add Student**: Enter student ID, name, and email to register new students
- **View All**: List of all registered students

### Courses Tab
- **Add Course**: Enter course ID, name, and credit hours
- **View Assignments**: See which teacher is assigned to each course
- **Teacher Assignment**: Manage teacher assignments (via Teachers tab)

### Teachers Tab (NEW)
- **Add Teacher**: Register teachers with ID, name, email, and department
- **Assign to Course**: Select a teacher and course to create teaching assignments
- **View Workload**: See all courses taught by each teacher

### Enrollment & Grades Tab
- **Enroll Student**: Select student and course to create enrollment
- **Assign Grade**: Enter grades (0-100) for enrolled students

### Reports Tab
- **Generate Report**: Select a student to view:
  - Enrolled courses
  - Credits for each course
  - Assigned grades
  - **Assigned teacher for each course** (NEW)

### Analysis Tab (NEW)
- **Refresh Charts**: Update all visualizations with current data
- **View Charts**:
  - Students per course distribution
  - Grade distribution across ranges
  - Teacher workload comparison
  - System statistics overview

## Data Storage Format

### CSV Structure

**students_data.csv**
```
StudentID,Name,Email
S001,John Doe,john@example.com
S002,Jane Smith,jane@example.com
```

**courses_data.csv**
```
CourseID,Name,Credits,TeacherID
C001,Mathematics,3,T001
C002,English,3,T002
```

**teachers_data.csv**
```
TeacherID,Name,Email,Department
T001,Dr. Smith,smith@example.com,Science
T002,Prof. Johnson,johnson@example.com,Literature
```

**enrollments_data.csv**
```
StudentID,CourseID,Grade
S001,C001,85
S001,C002,90
S002,C001,75
```

## Key Classes

### Person (Base Class)
- `person_id`: Unique identifier
- `name`: Full name
- `email`: Email address with validation
- Properties: `person_id`, `name`, `email`

### Student (extends Person)
- `enrolled_courses`: Dictionary of course_id -> grade
- Methods: `enroll()`, `assign_grade()`

### Teacher (extends Person)
- `department`: Department name
- `taught_courses`: List of course IDs
- Methods: `assign_course()`, `remove_course()`

### Course
- `course_id`: Unique course identifier
- `name`: Course name
- `credits`: Credit hours
- `teacher_id`: Assigned teacher (can be None)

### EducationSystem (Main Controller)
- Manages all students, courses, and teachers
- Handles enrollments and grading
- Provides analytics and reporting
- CSV-based data persistence

## Analytics Methods

### get_analytics()
Returns dictionary with:
- `total_students`: Count of all students
- `total_courses`: Count of all courses
- `total_teachers`: Count of all teachers
- `avg_grade`: System-wide average grade
- `students_per_course`: Dictionary of course -> enrollment count
- `grades_distribution`: Distribution across grade ranges
- `teacher_workload`: Dictionary of teacher -> course count

## Features Comparison

| Feature | Basic | Advanced |
|---------|-------|----------|
| Student Management | ✓ | ✓ |
| Course Management | ✓ | ✓ |
| Enrollment & Grades | ✓ | ✓ |
| Reports | ✓ | ✓ + Teacher Info |
| Teacher Management | ✗ | ✓ |
| Teacher-Course Assignment | ✗ | ✓ |
| CSV Storage | ✗ | ✓ |
| Analytics Dashboard | ✗ | ✓ |
| Data Visualization | ✗ | ✓ |

## Error Handling

The system includes comprehensive error handling:
- Duplicate ID prevention
- Data validation for emails and grades
- Exception handling for file I/O operations
- User-friendly error messages via message boxes

## Performance Considerations

- **CSV Files**: Efficient for moderate-sized datasets (100s-1000s of records)
- **In-Memory Storage**: All data loaded into memory for fast access
- **Real-Time Updates**: Data saved immediately after each operation
- **Scalability**: For larger datasets, consider database integration

## Future Enhancements

Potential features for future versions:
- Database integration (SQLite, PostgreSQL)
- User authentication and roles
- Attendance tracking
- Assignment and test management
- More advanced analytics (GPA calculations, trend analysis)
- Export reports to PDF/Excel
- Email notifications
- Multi-user concurrent access
- Backup and recovery system

## Troubleshooting

### Issue: matplotlib not found
**Solution**: Install matplotlib
```bash
pip install matplotlib
```

### Issue: CSV files not found
**Solution**: The system will create them automatically on first save

### Issue: GUI window not appearing
**Solution**: Ensure tkinter is installed (usually included with Python)

### Issue: Data not saving
**Solution**: Check file permissions in the directory

## License
This is an educational project for demonstration purposes.

## Support
For issues or questions, refer to the code comments and docstrings in:
- `system.py` - Core system logic
- `models.py` - Data model definitions
- `gui_main.py` - User interface implementation
