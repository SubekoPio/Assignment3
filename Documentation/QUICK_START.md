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
   - Teacher ID (e.g., T001)
   - Name (e.g., Dr. Smith)
   - Email (e.g., smith@example.com)
   - Department (e.g., Mathematics)
3. Click **Add Teacher**
4. Repeat for additional teachers

**CSV Output**: Updates `teachers_data.csv`

### Step 2: Add Courses
1. Click the **Courses** tab
2. Enter:
   - Course ID (e.g., M101)
   - Name (e.g., Calculus I)
   - Credits (e.g., 3)
3. Click **Add Course**
4. Repeat for additional courses

**CSV Output**: Updates `courses_data.csv`

### Step 3: Assign Teachers to Courses
1. Click the **Teachers** tab (scroll down to assignment section)
2. Select a teacher from the **Teacher** dropdown
3. Select a course from the **Course** dropdown
4. Click **Assign**
5. Verify assignment in the course list

**CSV Output**: Updates `courses_data.csv` with teacher_id

### Step 4: Add Students
1. Click the **Students** tab
2. Enter:
   - Student ID (e.g., S001)
   - Name (e.g., John Doe)
   - Email (e.g., john@example.com)
3. Click **Add Student**
4. Repeat for additional students

**CSV Output**: Updates `students_data.csv`

### Step 5: Enroll Students in Courses
1. Click **Enrollment & Grades** tab
2. Select a student from the **Student ID** dropdown
3. Select a course from the **Course ID** dropdown
4. Click **Enroll Student**
5. Success message confirms enrollment

**CSV Output**: Updates `enrollments_data.csv`

### Step 6: Assign Grades
1. Click **Enrollment & Grades** tab
2. Select the same student and course (from enrollments)
3. Enter a grade (0-100) in the **Grade** field
4. Click **Assign Grade**
5. Success message confirms grade assignment

**CSV Output**: Updates `enrollments_data.csv`

### Step 7: View Student Reports
1. Click **Reports** tab
2. Select a student from the **Select Student** dropdown
3. Click **Generate Report**
4. View the report showing:
   - Student name and ID
   - Enrolled courses
   - Credits per course
   - Grades earned
   - **Assigned teacher for each course** ← NEW!

### Step 8: View Analytics Dashboard
1. Click **Analysis** tab
2. Click **Refresh Charts** to generate visualizations
3. View four chart types:
   - **Top-Left**: Students per course (bar chart)
   - **Top-Right**: Grade distribution (bar chart)
   - **Bottom-Left**: Teacher workload (horizontal bar chart)
   - **Bottom-Right**: System statistics (text summary)

## Data Files Generated

After following the tutorial, you'll have:

```
students_data.csv          # Student records
courses_data.csv           # Course details with teacher assignments
teachers_data.csv          # Teacher information
enrollments_data.csv       # Student enrollments and grades
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

### Assign Teachers:
- T001 → M101
- T002 → P201
- T003 → E102

### Enroll Students and Assign Grades:
- S001 in M101: 85
- S001 in P201: 78
- S002 in M101: 92
- S002 in E102: 88
- S003 in P201: 76
- S003 in E102: 94

## Key Features to Try

### Feature 1: Teacher Tracking
✓ See which teacher teaches each course in the **Courses** tab
✓ View each teacher's workload in the **Teachers** tab

### Feature 2: Comprehensive Reports
✓ Generate student reports that include **teacher names**
✓ See complete course details with instructor information

### Feature 3: Analytics
✓ See enrollment trends across courses
✓ Understand grade distribution in the system
✓ Monitor teacher workload balance

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
2. Select a different teacher and same course
3. Click **Assign** - automatically replaces previous assignment
4. Previous teacher is automatically removed from course

### Data Persistence
✓ All data saved automatically after each operation
✓ Quit and restart application - all data is preserved
✓ Delete CSV files to start fresh

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Teacher dropdown empty | Make sure you've added teachers first |
| Can't enroll student | First add student, then add course, then enroll |
| Grades not saving | Make sure student is enrolled in course first |
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
