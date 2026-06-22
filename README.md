# EduManage — Advanced Education Management System

EduManage is a desktop-based education management application built in Python. It provides school administrators with a centralized panel to manage students, courses, units, teacher workloads, grades, academic reporting, and statistics.

---

## 🚀 Quick Start & Installation

### 1. Install Dependencies
This project uses **CustomTkinter** for modern GUI aesthetics, **Matplotlib** for charts, and **ReportLab** for professional PDF exports. Install all requirements by running:
```bash
pip install customtkinter matplotlib reportlab pytest
```

### 2. Run the Application
Start the primary modern interface:
```bash
python gui_main.py
```
*(If running on a system without CustomTkinter capabilities, you can use the standard Tkinter fallback: `python gui_main_basic.py`)*

### 3. Run Automated Tests
Verify code behavior and data integrity constraints:
```bash
pytest
```

---

## 🌟 Key Features

1. **👥 Student Management:** Full CRUD operations with automatic email format checks and unique ID assignment.
2. **📚 Course & Unit Catalog:** Global uniqueness checks for course unit codes with structured unit mappings.
3. **👨‍🏫 Teacher Assignment:** Assign teachers to courses and individual units while tracking workload statistics.
4. **📝 Enrollment & Grading:** Enroll students in specific units and record academic grades (validated 0-100).
5. **📊 Reports & Styled PDF Export:** Generate transcript previews and export branded PDF files containing custom grade badges, CGPA calculations, and registrar signature lines.
6. **📈 Analytics Dashboard:** View visual charts representing enrollment distributions, grade trends, and teacher workload.
7. **💾 Built-in Backup System:** Instantly bundle all databases into a timestamped ZIP archive directly from the GUI header.

---

## 📂 Project Structure

- [gui_main.py](file:///c:/Users/abdir/Desktop/Assignment3/gui_main.py): The main CustomTkinter GUI application.
- [system.py](file:///c:/Users/abdir/Desktop/Assignment3/system.py): Core controller containing CRUD operations, business rules, and CSV storage logic.
- [models.py](file:///c:/Users/abdir/Desktop/Assignment3/models.py): Object-oriented domain classes (`Person`, `Student`, `Teacher`, `Course`, `Unit`).
- [tests/](file:///c:/Users/abdir/Desktop/Assignment3/tests): Test suite checking positive and negative operations.
- [Data_Storage(CSV)/](file:///c:/Users/abdir/Desktop/Assignment3/Data_Storage(CSV)): Transparent databases stored in CSV format.
- [Documentation/](file:///c:/Users/abdir/Desktop/Assignment3/Documentation): Comprehensive coursework reports and system manuals.
- [TEAM_PRESENTATION.html](file:///c:/Users/abdir/Desktop/Assignment3/TEAM_PRESENTATION.html): 54-slide team presentation deck.

GitHub Link: https://github.com/SubekoPio/Assignment3.git
