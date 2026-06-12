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
