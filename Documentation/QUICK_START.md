# EduManage Advanced System - Quick Start Guide

## Installation & Launch
```bash
# Ensure matplotlib is installed
pip install matplotlib

# Navigate to the directory
cd "Intermediate Education System in Python Based on PDF Guidelines"

# Run the application
python gui_main.py
```

## Step-by-Step Tutorial

### Step 1: Add Teachers
1. Click the **Teachers** tab
2. Enter:
   - Name (e.g., Dr. Smith)
   - Email (e.g., smith@example.com)
   - Department (e.g., Mathematics)
3. Click **Add Teacher**
4. Repeat for additional teachers

**CSV Output**: Updates `teachers_data.csv`

### Step 2: Add Courses
1. Click the **Courses** tab
2. Enter:
   - Name (e.g., Calculus I)
   - Credits (e.g., 3)
3. Click **Add Course**
4. Repeat for additional courses

**CSV Output**: Updates `courses_data.csv`

### Step 3: Add Units to Courses
1. Click the **Courses** tab
2. Select a course in the table
3. In the **Course Units** panel, add Unit Name and Credits
4. Click **Add**
5. Repeat per course

**CSV Output**: Updates `courses_data.csv` (`Units` column)

### Step 4: Assign Teachers to Courses/Units
1. Click the **Teachers** tab (scroll down to assignment section)
2. Select a teacher from the **Teacher** dropdown
3. Select a course from the **Course** dropdown
4. Optionally select a specific unit from the **Unit** dropdown
5. Click **Assign Course** or **Assign Unit**
6. Verify assignments in teachers/courses tables

**CSV Output**: Updates `courses_data.csv` with `TeacherID`, `TeacherIDs`, and unit `teacher_id`

### Step 5: Add Students
1. Click the **Students** tab
2. Enter:
   - Name (e.g., John Doe)
   - Email (e.g., john@example.com)
3. Click **Add Student**
4. Repeat for additional students

**CSV Output**: Updates `students_data.csv`

### Step 6: Enroll Students in Course Units
1. Click **Enrollment & Grades** tab
2. Select a student from the **Student** dropdown
3. Select a course from the **Course** dropdown
4. Pick one or more units from the units list
5. Click **Enroll Selected Units**
6. Success message confirms enrollment

**CSV Output**: Updates `enrollments_data.csv`

### Step 7: Assign Grades
1. Click **Enrollment & Grades** tab
2. Select an enrollment row (student-course-unit)
3. Enter a grade (0-100) in the **Grade** field
4. Click **Assign Grade**
5. Success message confirms grade assignment

**CSV Output**: Updates `enrollments_data.csv`

### Step 8: View Student Reports
1. Click **Reports** tab
2. Select a student from the **Select Student** dropdown
3. Click **Generate Report**
4. View the report showing:
   - Student name and ID
   - Enrolled courses and units
   - Credits per course and unit
   - Unit grades and letters
   - **Assigned teacher for each unit**

### Step 9: View Analytics Dashboard
1. Click **Analysis** tab
2. Click **Refresh Charts** to generate visualizations
3. View four chart types (with larger labels and improved readability):
   - **Top-Left**: Students per course (bar chart)
   - **Top-Right**: Grade distribution (bar chart)
   - **Bottom-Left**: Teacher workload (horizontal bar chart)
   - **Bottom-Right**: System statistics (text summary)

## Data Files Generated

After following the tutorial, you'll have:

```
students_data.csv          # Student records
courses_data.csv           # Course details with units and teacher assignments
teachers_data.csv          # Teacher information
enrollments_data.csv       # Student enrollments and grades at unit level
```

## Sample Data for Testing

### Add These Teachers:
| ID | Name | Email | Department |
|----|------|-------|-----------|
| T001 | Dr. Smith | smith@example.com | Mathematics |
| T002 | Prof. Johnson | johnson@example.com | Physics |
| T003 | Ms. Williams | williams@example.com | English |

### Add These Courses:
| ID | Name | Credits |
|----|------|---------|
| M101 | Calculus I | 3 |
| P201 | Physics II | 4 |
| E102 | Literature | 3 |

### Add These Students:
| ID | Name | Email |
|----|------|-------|
| S001 | Alice Brown | alice@example.com |
| S002 | Bob Davis | bob@example.com |
| S003 | Carol White | carol@example.com |

### Add Units:
- M101: U1 Limits (1), U2 Derivatives (2)
- P201: U1 Kinematics (2), U2 Dynamics (2)
- E102: U1 Poetry (1), U2 Prose (2)

### Assign Teachers:
- T001 â†’ M101 (course)
- T002 â†’ P201-U1 (unit)
- T003 â†’ E102-U2 (unit)

### Enroll Students and Assign Grades:
- S001 in M101-U1: 85
- S001 in P201-U1: 78
- S002 in M101-U2: 92
- S002 in E102-U1: 88
- S003 in P201-U2: 76
- S003 in E102-U2: 94

## Key Features to Try

### Feature 1: Teacher Tracking
âœ“ See which teacher teaches each course in the **Courses** tab
âœ“ View each teacher's workload in the **Teachers** tab

### Feature 2: Comprehensive Reports
âœ“ Generate student reports that include **teacher names**
âœ“ See complete course details with instructor information

### Feature 3: Analytics
âœ“ See enrollment trends across courses
âœ“ Understand grade distribution in the system
âœ“ Monitor teacher workload balance

## Tips & Tricks

### View All Teachers' Courses
1. Go to **Teachers** tab
2. Look at the rightmost "Courses Taught" column
3. Shows comma-separated list of course IDs

### Check Course Assignment
1. Go to **Courses** tab
2. Look at rightmost column "Assigned Teacher"
3. Shows teacher name or "Unassigned" if not yet assigned

### Modify Teacher Assignment
1. Go to **Teachers** tab
2. Select a different teacher and same course/unit
3. Click **Assign Course** or **Assign Unit**
4. Workload updates instantly

### Data Persistence
âœ“ All data saved automatically after each operation
âœ“ Quit and restart application - all data is preserved
âœ“ Delete CSV files to start fresh

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Teacher dropdown empty | Make sure you've added teachers first |
| Unit dropdown empty | Add units to selected course first |
| Can't enroll student | Add student, course, and at least one unit first |
| Grades not saving | Select an enrollment row before assigning grade |
| Charts not showing | Click "Refresh Charts" button |
| CSV files not created | They auto-create on first save operation |

## Common Workflows

### Workflow 1: Set Up New Course
```
1. Add Teacher (Teachers tab)
2. Add Course (Courses tab)
3. Assign Teacher to Course (Teachers tab)
4. Add Students (Students tab)
5. Enroll Students (Enrollment tab)
```

### Workflow 2: Record Grades
```
1. Ensure student is enrolled (check Enrollment tab)
2. Enter grade value (Enrollment tab)
3. View in Report (Reports tab)
4. Check Analytics (Analysis tab)
```

### Workflow 3: Reorganize Teachers
```
1. Go to Teachers tab
2. Find "Assign Teacher to Course" section
3. Select different teacher
4. Select course
5. Click Assign - updates automatically
```

## Advanced Features

### Batch Operations
- Add multiple students/teachers/courses in succession
- Data saves after each operation
- No data loss on application restart

### Real-Time Synchronization
- Changes visible immediately across all tabs
- Teacher assignments update course lists
- Reports always reflect latest data

### Robust Analytics
- Handles missing grades (shows as "N/A")
- Calculates metrics only from valid data
- Charts update with "Refresh Charts" button

## Next Steps
1. Explore the codebase in `models.py`, `system.py`, `gui_main.py`
2. Consider adding more courses and students
3. Test the data persistence by restarting the app
4. Export CSV data for external analysis

## Support Documentation
See also:
- `README_ADVANCED.md` - Comprehensive feature documentation
- `UPGRADE_SUMMARY.md` - Technical upgrade details
- Code comments in Python files for implementation details

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
- Added consistent action-button variants and improved card spacing to make workflows visually clearer.
- Fixed the Courses tab splitter defaults so Course Units are visible without manual resizing.
- Updated Enrollment panel colors/cards to align with the same style as Students/Courses/Teachers tabs.
- Added analysis dropdown support for both Student and Teacher snapshots while keeping the general dashboard charts.

