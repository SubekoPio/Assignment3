import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from system import EducationSystem
from fpdf import FPDF

class EduManageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EduManage - Advanced Education Management System")
        self.root.geometry("1000x700")
        self.system = EducationSystem()
        self.selected_student_id = None
        self.selected_course_id = None
        self.selected_teacher_id = None
        self.selected_enrollment = None

        # Define Colors
        self.primary_color = "#2C3E50"
        self.secondary_color = "#3498DB"
        self.bg_color = "#ECF0F1"
        self.accent_color = "#E74C3C"
        self.text_color = "#2C3E50"

        self.root.configure(bg=self.bg_color)
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Notebook
        style.configure("TNotebook", background=self.bg_color)
        style.configure("TNotebook.Tab", background="#BDC3C7", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", self.secondary_color)])

        # Configuration of Treeview
        style.configure("Treeview", background="white", fieldbackground="white", rowheight=25)
        style.map("Treeview", background=[("selected", self.secondary_color)])
        style.configure("Treeview.Heading", background="#BDC3C7", font=('Helvetica', 10, 'bold'))

    def create_widgets(self):
        # Headers
        header = tk.Frame(self.root, bg=self.primary_color, height=60)
        header.pack(fill="x")
        tk.Label(header, text="EduManage Advanced System", fg="white", bg=self.primary_color, 
                 font=("Helvetica", 18, "bold")).pack(pady=15)

        # Main Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.tab_students = tk.Frame(self.notebook, bg=self.bg_color)
        self.tab_courses = tk.Frame(self.notebook, bg=self.bg_color)
        self.tab_teachers = tk.Frame(self.notebook, bg=self.bg_color)
        self.tab_enroll = tk.Frame(self.notebook, bg=self.bg_color)
        self.tab_reports = tk.Frame(self.notebook, bg=self.bg_color)
        self.tab_analysis = tk.Frame(self.notebook, bg=self.bg_color)

        self.notebook.add(self.tab_students, text=" Students ")
        self.notebook.add(self.tab_courses, text=" Courses ")
        self.notebook.add(self.tab_teachers, text=" Teachers ")
        self.notebook.add(self.tab_enroll, text=" Enrollment & Grades ")
        self.notebook.add(self.tab_reports, text=" Reports ")
        self.notebook.add(self.tab_analysis, text=" Analysis ")

        self.setup_student_tab()
        self.setup_course_tab()
        self.setup_teacher_tab()
        self.setup_enroll_tab()
        self.setup_report_tab()
        self.setup_analysis_tab()
        self.update_comboboxes()

    def setup_student_tab(self):
        # Input of Frame
        input_frame = tk.LabelFrame(self.tab_students, text="Student Details", bg=self.bg_color, font=("Helvetica", 10, "bold"))
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="ID:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.ent_sid = tk.Entry(input_frame)
        self.ent_sid.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Name:", bg=self.bg_color).grid(row=0, column=2, padx=5, pady=5)
        self.ent_sname = tk.Entry(input_frame)
        self.ent_sname.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Email:", bg=self.bg_color).grid(row=0, column=4, padx=5, pady=5)
        self.ent_semail = tk.Entry(input_frame)
        self.ent_semail.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(input_frame, text="Add Student", command=self.add_student, bg=self.secondary_color, fg="white").grid(row=1, column=0, padx=10, pady=5)
        tk.Button(input_frame, text="Update Student", command=self.update_student, bg="#F39C12", fg="white").grid(row=1, column=1, padx=10, pady=5)
        tk.Button(input_frame, text="Delete Student", command=self.delete_student, bg=self.accent_color, fg="white").grid(row=1, column=2, padx=10, pady=5)
        tk.Button(input_frame, text="Clear", command=self.clear_student_form, bg="#7F8C8D", fg="white").grid(row=1, column=3, padx=10, pady=5)

        # --- NEW SEARCH FRAME ---
        search_frame = tk.Frame(self.tab_students, bg=self.bg_color)
        search_frame.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(search_frame, text="🔍 Search Students:", bg=self.bg_color, font=("Helvetica", 10, "bold")).pack(side="left", padx=5)
        self.ent_search_student = tk.Entry(search_frame, width=40)
        self.ent_search_student.pack(side="left", padx=5)
        self.ent_search_student.bind("<KeyRelease>", lambda e: self.refresh_student_list(self.ent_search_student.get()))

        # Table Frame
        self.tree_students = ttk.Treeview(self.tab_students, columns=("ID", "Name", "Email"), show="headings", selectmode="browse")
        self.tree_students.heading("ID", text="Student ID")
        self.tree_students.heading("Name", text="Name")
        self.tree_students.heading("Email", text="Email")
        self.tree_students.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_students.bind("<<TreeviewSelect>>", self.on_student_select)
        self.refresh_student_list()

    def setup_course_tab(self):
        input_frame = tk.LabelFrame(self.tab_courses, text="Course Details", bg=self.bg_color, font=("Helvetica", 10, "bold"))
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="ID:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.ent_cid = tk.Entry(input_frame)
        self.ent_cid.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Name:", bg=self.bg_color).grid(row=0, column=2, padx=5, pady=5)
        self.ent_cname = tk.Entry(input_frame)
        self.ent_cname.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Total Credits:", bg=self.bg_color).grid(row=0, column=4, padx=5, pady=5)
        self.ent_ccredits = tk.Entry(input_frame)
        self.ent_ccredits.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(input_frame, text="Add Course", command=self.add_course, bg=self.secondary_color, fg="white").grid(row=1, column=0, padx=10, pady=5)
        tk.Button(input_frame, text="Update Course", command=self.update_course, bg="#F39C12", fg="white").grid(row=1, column=1, padx=10, pady=5)
        tk.Button(input_frame, text="Delete Course", command=self.delete_course, bg=self.accent_color, fg="white").grid(row=1, column=2, padx=10, pady=5)
        tk.Button(input_frame, text="Clear", command=self.clear_course_form, bg="#7F8C8D", fg="white").grid(row=1, column=3, padx=10, pady=5)
        tk.Button(input_frame, text="Export CSV", command=self.export_summary, bg="#27AE60", fg="white").grid(row=1, column=4, padx=10, pady=5)

        # --- NEW SEARCH FRAME ---
        search_frame_c = tk.Frame(self.tab_courses, bg=self.bg_color)
        search_frame_c.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(search_frame_c, text="🔍 Search Courses:", bg=self.bg_color, font=("Helvetica", 10, "bold")).pack(side="left", padx=5)
        self.ent_search_course = tk.Entry(search_frame_c, width=40)
        self.ent_search_course.pack(side="left", padx=5)
        self.ent_search_course.bind("<KeyRelease>", lambda e: self.refresh_course_list(self.ent_search_course.get()))

        self.tree_courses = ttk.Treeview(self.tab_courses, columns=("ID", "Name", "Credits", "Teacher"), show="headings", selectmode="browse")
        self.tree_courses.heading("ID", text="Course ID")
        self.tree_courses.heading("Name", text="Name")
        self.tree_courses.heading("Credits", text="Total Credits")
        self.tree_courses.heading("Teacher", text="Assigned Teacher")
        self.tree_courses.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_courses.bind("<<TreeviewSelect>>", self.on_course_select)
        self.refresh_course_list()

        # Unit management
        unit_frame = tk.LabelFrame(self.tab_courses, text="Manage Units for Selected Course", bg=self.bg_color, font=("Helvetica", 10, "bold"))
        unit_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(unit_frame, text="Unit ID:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.ent_unit_id = tk.Entry(unit_frame)
        self.ent_unit_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(unit_frame, text="Unit Name:", bg=self.bg_color).grid(row=0, column=2, padx=5, pady=5)
        self.ent_unit_name = tk.Entry(unit_frame)
        self.ent_unit_name.grid(row=0, column=3, padx=5, pady=5)
        tk.Label(unit_frame, text="Credits:", bg=self.bg_color).grid(row=0, column=4, padx=5, pady=5)
        self.ent_unit_credits = tk.Entry(unit_frame, width=6)
        self.ent_unit_credits.grid(row=0, column=5, padx=5, pady=5)
        tk.Button(unit_frame, text="Add Unit to Course", command=self.add_unit_to_course, bg=self.secondary_color, fg="white").grid(row=0, column=6, padx=10, pady=5)
        tk.Button(unit_frame, text="Manage Units...", command=self.open_manage_units_dialog, bg="#8E44AD", fg="white").grid(row=0, column=7, padx=10, pady=5)

    def setup_teacher_tab(self):
        # Input Frame
        input_frame = tk.LabelFrame(self.tab_teachers, text="Teacher Details", bg=self.bg_color, font=("Helvetica", 10, "bold"))
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="ID:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.ent_tid = tk.Entry(input_frame)
        self.ent_tid.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Name:", bg=self.bg_color).grid(row=0, column=2, padx=5, pady=5)
        self.ent_tname = tk.Entry(input_frame)
        self.ent_tname.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Email:", bg=self.bg_color).grid(row=0, column=4, padx=5, pady=5)
        self.ent_temail = tk.Entry(input_frame)
        self.ent_temail.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(input_frame, text="Department:", bg=self.bg_color).grid(row=1, column=0, padx=5, pady=5)
        self.ent_tdept = tk.Entry(input_frame)
        self.ent_tdept.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(input_frame, text="Add Teacher", command=self.add_teacher, bg=self.secondary_color, fg="white").grid(row=1, column=2, padx=10, pady=5)
        tk.Button(input_frame, text="Update Teacher", command=self.update_teacher, bg="#F39C12", fg="white").grid(row=1, column=3, padx=10, pady=5)
        tk.Button(input_frame, text="Delete Teacher", command=self.delete_teacher, bg=self.accent_color, fg="white").grid(row=1, column=4, padx=10, pady=5)
        tk.Button(input_frame, text="Clear", command=self.clear_teacher_form, bg="#7F8C8D", fg="white").grid(row=1, column=5, padx=10, pady=5)

        # Assignment Frame
        assign_frame = tk.LabelFrame(self.tab_teachers, text="Assign Teacher to Course", bg=self.bg_color, font=("Helvetica", 10, "bold"))
        assign_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(assign_frame, text="Teacher:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.cb_assign_teacher = ttk.Combobox(assign_frame)
        self.cb_assign_teacher.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(assign_frame, text="Course:", bg=self.bg_color).grid(row=0, column=2, padx=5, pady=5)
        self.cb_assign_course = ttk.Combobox(assign_frame)
        self.cb_assign_course.grid(row=0, column=3, padx=5, pady=5)
        self.cb_assign_course.bind('<<ComboboxSelected>>', self.on_assign_course_selected)

        tk.Label(assign_frame, text="Unit:", bg=self.bg_color).grid(row=0, column=4, padx=5, pady=5)
        self.cb_assign_unit = ttk.Combobox(assign_frame, width=24)
        self.cb_assign_unit.grid(row=0, column=5, padx=5, pady=5)

       
        tk.Button(assign_frame, text="Assign Course", command=self.assign_course_only, bg="#2980B9", fg="white").grid(row=0, column=6, padx=5, pady=5)
        tk.Button(assign_frame, text="Assign Unit", command=self.assign_unit_only, bg="#27AE60", fg="white").grid(row=0, column=7, padx=5, pady=5)

        # --- NEW SEARCH FRAME ---
        search_frame_t = tk.Frame(self.tab_teachers, bg=self.bg_color)
        search_frame_t.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(search_frame_t, text="🔍 Search Teachers:", bg=self.bg_color, font=("Helvetica", 10, "bold")).pack(side="left", padx=5)
        self.ent_search_teacher = tk.Entry(search_frame_t, width=40)
        self.ent_search_teacher.pack(side="left", padx=5)
        self.ent_search_teacher.bind("<KeyRelease>", lambda e: self.refresh_teacher_list(self.ent_search_teacher.get()))


        # Table Frame
        self.tree_teachers = ttk.Treeview(self.tab_teachers, columns=("ID", "Name", "Email", "Department", "Courses"), show="headings", selectmode="browse")
        self.tree_teachers.heading("ID", text="Teacher ID")
        self.tree_teachers.heading("Name", text="Name")
        self.tree_teachers.heading("Email", text="Email")
        self.tree_teachers.heading("Department", text="Department")
        self.tree_teachers.heading("Courses", text="Courses Taught")
        self.tree_teachers.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_teachers.bind("<<TreeviewSelect>>", self.on_teacher_select)
        self.refresh_teacher_list()

    def setup_enroll_tab(self):
        top_frame = tk.Frame(self.tab_enroll, bg=self.bg_color)
        top_frame.pack(fill="x", padx=10, pady=10)

        action_frame = tk.LabelFrame(top_frame, text="Enroll Student & Assign Grade", bg=self.bg_color, font=("Helvetica", 10, "bold"))
        action_frame.pack(fill="x", expand=True, padx=5, pady=5)

        tk.Label(action_frame, text="Student:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.cb_students = ttk.Combobox(action_frame, width=30)
        self.cb_students.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(action_frame, text="Course:", bg=self.bg_color).grid(row=0, column=2, padx=5, pady=10, sticky="w")
        self.cb_courses = ttk.Combobox(action_frame, width=30)
        self.cb_courses.grid(row=0, column=3, padx=5, pady=10)
        self.cb_courses.bind("<<ComboboxSelected>>", self.on_cb_course_selected)

        tk.Button(action_frame, text="Enroll (Course)", command=self.enroll_student, bg=self.secondary_color, fg="white", width=18).grid(row=0, column=4, padx=10, pady=10)

        tk.Label(action_frame, text="Grade:", bg=self.bg_color).grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.ent_grade = tk.Entry(action_frame, width=10)
        self.ent_grade.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        tk.Button(action_frame, text="Assign Grade", command=self.assign_grade, bg="#27AE60", fg="white", width=18).grid(row=1, column=4, padx=10, pady=10)
        tk.Button(action_frame, text="Remove Enrollment", command=self.delete_enrollment, bg=self.accent_color, fg="white", width=18).grid(row=1, column=5, padx=10, pady=10)

        # Units list for selected course (multi-select)
        units_frame = tk.LabelFrame(self.tab_enroll, text="Course Units (select to enroll or grade)", bg=self.bg_color, font=("Helvetica", 10, "bold"))
        units_frame.pack(fill="x", padx=10, pady=5)
        self.lb_units = tk.Listbox(units_frame, selectmode='multiple', height=4, exportselection=False)
        self.lb_units.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        btns_units = tk.Frame(units_frame, bg=self.bg_color)
        btns_units.pack(side='left', padx=5)
        tk.Button(btns_units, text="Enroll Selected Units", command=self.enroll_selected_units, bg="#2980B9", fg="white").pack(fill='x', pady=2)
        tk.Button(btns_units, text="Assign Grade To Selected Unit", command=self.assign_grade_to_selected_unit, bg="#27AE60", fg="white").pack(fill='x', pady=2)

        list_frame = tk.LabelFrame(self.tab_enroll, text="Current Enrollments", bg=self.bg_color, font=("Helvetica", 10, "bold"))
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_enrollments = ttk.Treeview(list_frame, columns=("Student", "Course", "Unit", "Grade"), show="headings", selectmode="browse")
        self.tree_enrollments.heading("Student", text="Student")
        self.tree_enrollments.heading("Course", text="Course")
        self.tree_enrollments.heading("Unit", text="Unit")
        self.tree_enrollments.heading("Grade", text="Grade")
        self.tree_enrollments.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_enrollments.bind("<<TreeviewSelect>>", self.on_enrollment_select)
        self.refresh_enrollment_list()

    def setup_report_tab(self):
        frame = tk.Frame(self.tab_reports, bg=self.bg_color)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Select Student:", bg=self.bg_color).pack(side="left", padx=5)
        self.cb_report_student = ttk.Combobox(frame)
        self.cb_report_student.pack(side="left", padx=5)
        tk.Button(frame, text="Generate Report", command=self.generate_report, bg=self.secondary_color, fg="white").pack(side="left", padx=10)
        tk.Button(frame, text="Export to PDF", command=self.export_report_pdf, bg="#8E44AD", fg="white").pack(side="left", padx=10)

        self.txt_report = tk.Text(self.tab_reports, height=15, font=("Courier", 10))
        self.txt_report.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_analysis_tab(self):
        """Setup analysis dashboard with charts."""
        btn_frame = tk.Frame(self.tab_analysis, bg=self.bg_color)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(btn_frame, text="Student:", bg=self.bg_color).pack(side='left', padx=5)
        self.cb_analysis_student = ttk.Combobox(btn_frame)
        self.cb_analysis_student.pack(side='left', padx=5)
        tk.Button(btn_frame, text="Refresh Charts", command=self.refresh_analysis, bg=self.secondary_color, fg="white").pack(side="left", padx=10)

        self.canvas_frame = tk.Frame(self.tab_analysis, bg=self.bg_color)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

    def refresh_analysis(self):
        """Refresh and display analysis charts."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        analytics = self.system.get_analytics()

        # Create figure with subplots
        fig = Figure(figsize=(12, 7), dpi=80)
        
        # Chart 1: Students per course
        if analytics["students_per_course"]:
            ax1 = fig.add_subplot(2, 2, 1)
            courses = list(analytics["students_per_course"].keys())
            counts = list(analytics["students_per_course"].values())
            ax1.bar(courses, counts, color=self.secondary_color)
            ax1.set_title("Students Enrolled per Course")
            ax1.set_xlabel("Course")
            ax1.set_ylabel("Count")
            ax1.tick_params(axis='x', rotation=45)

        # Chart 2: Grade distribution (letter buckets)
        if analytics["grades_distribution"]:
            ax2 = fig.add_subplot(2, 2, 2)
            # fixed order
            order = ['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']
            ranges = order
            dist = [analytics["grades_distribution"].get(k, 0) for k in order]

            # if a student selected, highlight buckets that student has
            selected_student = self.cb_analysis_student.get()
            student_buckets = {}
            if selected_student:
                try:
                    sid = self._get_student_id_by_name(selected_student)
                    if sid in self.system.students:
                        student = self.system.students[sid]
                        for course_id, data in student.enrolled_courses.items():
                            for grade in data.get('units', {}).values():
                                if grade is not None and isinstance(grade, (int, float)):
                                    letter = self.system.grade_to_letter(float(grade))
                                    student_buckets[letter] = student_buckets.get(letter, 0) + 1
                except Exception:
                    # mapping failed (e.g. duplicate name); ignore and show general analysis
                    student_buckets = {}

            colors = [self.secondary_color if student_buckets.get(k, 0) > 0 else self.accent_color for k in order]
            bars = ax2.bar(ranges, dist, color=colors)
            ax2.set_title("Grade Distribution (Letter Grades)")
            ax2.set_xlabel("Letter Grade")
            ax2.set_ylabel("Count")
            ax2.tick_params(axis='x', rotation=45)

            # annotate student counts on bars
            if student_buckets:
                for i, k in enumerate(order):
                    sb = student_buckets.get(k, 0)
                    if sb:
                        ax2.text(i, dist[i] + 0.1, f"You: {sb}", ha='center', color='black')

        # Chart 3: Teacher workload
        if analytics["teacher_workload"]:
            ax3 = fig.add_subplot(2, 2, 3)
            teachers = list(analytics["teacher_workload"].keys())
            workload = list(analytics["teacher_workload"].values())
            ax3.barh(teachers, workload, color="#27AE60")
            ax3.set_title("Teacher Workload (Courses)")
            ax3.set_xlabel("Number of Courses")

        # Chart 4: System statistics
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.axis('off')
        stats_text = f"""
SYSTEM STATISTICS

Total Students: {analytics['total_students']}
Total Courses: {analytics['total_courses']}
Total Teachers: {analytics['total_teachers']}
Average Grade: {analytics['avg_grade']:.2f}
        """
        ax4.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center', 
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        fig.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Logic Methods
    def add_student(self):
        sid = self.ent_sid.get()
        name = self.ent_sname.get()
        email = self.ent_semail.get()
        try:
            self.system.add_student(sid, name, email)
            self.system.save_data()
            self.refresh_student_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "Student added successfully!")
            self.ent_sid.delete(0, tk.END)
            self.ent_sname.delete(0, tk.END)
            self.ent_semail.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_course(self):
        cid = self.ent_cid.get()
        name = self.ent_cname.get()
        try:
            credits = int(self.ent_ccredits.get())
            self.system.add_course(cid, name, credits)
            self.system.save_data()
            self.refresh_course_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "Course added successfully!")
            self.ent_cid.delete(0, tk.END)
            self.ent_cname.delete(0, tk.END)
            self.ent_ccredits.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def is_unit_id_taken(self, cid, uid, current_editing_id=None):
        """
        Returns True if the ID is taken by a different unit.
        current_editing_id: The ID of the unit being edited (pass None if adding a new one).
        """
        course = self.system.courses.get(cid)
        if not course:
            return False
        
        for u in course.units:
            # Check if this ID is in use by ANY unit that isn't the one we are editing
            if u['unit_id'] == uid and u['unit_id'] != current_editing_id:
                return True
        return False

    def add_unit_to_course(self):
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Select a course first (or update form and select)")
            return
        
        uid = self.ent_unit_id.get().strip()
        uname = self.ent_unit_name.get().strip()
        
        # 1. Check for duplicate ID
        if self.is_unit_id_taken(self.selected_course_id, uid):
            messagebox.showerror("Error", f"Unit ID '{uid}' already exists in this course!")
            return # Stop execution here so the duplicate is not added
            
        try:
            ucredits = float(self.ent_unit_credits.get())
        except Exception:
            messagebox.showerror("Error", "Unit credits must be a number")
            return
            
        try:
            self.system.add_course_unit(self.selected_course_id, uid, uname, ucredits)
            self.system.save_data()
            self.refresh_course_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", f"Unit {uid} added to course {self.selected_course_id}")
            
            # Clear fields only after success
            self.ent_unit_id.delete(0, tk.END)
            self.ent_unit_name.delete(0, tk.END)
            self.ent_unit_credits.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_teacher(self):
        tid = self.ent_tid.get()
        name = self.ent_tname.get()
        email = self.ent_temail.get()
        dept = self.ent_tdept.get()
        try:
            self.system.add_teacher(tid, name, email, dept)
            self.system.save_data()
            self.refresh_teacher_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "Teacher added successfully!")
            self.ent_tid.delete(0, tk.END)
            self.ent_tname.delete(0, tk.END)
            self.ent_temail.delete(0, tk.END)
            self.ent_tdept.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def assign_course_only(self):
        try:
            teacher_str = self.cb_assign_teacher.get()
            course_str = self.cb_assign_course.get()

            if not teacher_str or not course_str:
                messagebox.showwarning("Warning", "Please select a teacher and a course.")
                return
            
            teacher_id = teacher_str.split(" - ")[0]
            course_id = course_str.split(" - ")[0]

            self.system.assign_teacher_to_course(teacher_id, course_id)
            self.system.save_data()
            self.refresh_course_list()
            self.refresh_teacher_list()
            messagebox.showinfo("Success", f"Teacher {teacher_id} assigned to entire course {course_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def assign_unit_only(self):
        try:
            teacher_str = self.cb_assign_teacher.get()
            course_str = self.cb_assign_course.get()
            unit_str = self.cb_assign_unit.get()

            if not teacher_str or not course_str or not unit_str:
                messagebox.showwarning("Warning", "Please select a teacher, a course, AND a specific unit.")
                return

            teacher_id = teacher_str.split(" - ")[0]
            course_id = course_str.split(" - ")[0]
            unit_id = unit_str.split(" - ")[0]

            self.system.assign_teacher_to_unit(teacher_id, course_id, unit_id)
            self.system.save_data()
            self.refresh_course_list()
            self.refresh_teacher_list()
            messagebox.showinfo("Success", f"Teacher {teacher_id} assigned to unit {unit_id} in {course_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_assign_course_selected(self, event=None):
        try:
            course_str = self.cb_assign_course.get()
            if not course_str:
                return
            cid = course_str.split(' - ')[0]
            course = self.system.courses.get(cid)
            vals = []
            if course:
                vals = [f"{u.get('unit_id')} - {u.get('name')}" for u in course.units]
            self.cb_assign_unit['values'] = vals
        except Exception:
            pass

    def enroll_student(self):
        try:
            student_str = self.cb_students.get()
            course_str = self.cb_courses.get()

            if not student_str or not course_str:
                messagebox.showwarning("Warning", "Please select both student and course")
                return

            sid = self._get_student_id_by_name(student_str)
            cid = course_str.split(" - ")[0]

            self.system.enroll_student(sid, cid)
            self.system.save_data()
            self.refresh_enrollment_list()
            messagebox.showinfo("Success", f"Enrolled {sid} in {cid}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def enroll_selected_units(self):
        try:
            student_str = self.cb_students.get()
            course_str = self.cb_courses.get()
            if not student_str or not course_str:
                messagebox.showwarning("Warning", "Please select both student and course")
                return
            sid = self._get_student_id_by_name(student_str)
            cid = course_str.split(" - ")[0]
            selections = self.lb_units.curselection()
            if not selections:
                messagebox.showwarning("Warning", "Select at least one unit to enroll")
                return
            units = [self.lb_units.get(i).split(" - ")[0] for i in selections]
            for uid in units:
                self.system.enroll_student_unit(sid, cid, uid)
            self.system.save_data()
            self.refresh_enrollment_list()
            messagebox.showinfo("Success", f"Enrolled {sid} in {len(units)} unit(s) of {cid}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def assign_grade_to_selected_unit(self):
        try:
            # Prefer selected enrollment row (unit-specific)
            if not self.selected_enrollment:
                messagebox.showwarning("Warning", "Select an enrollment row to assign grade to")
                return
            sid, cid, uid = self.selected_enrollment
            grade = float(self.ent_grade.get())
            self.system.assign_unit_grade(sid, cid, uid, grade)
            self.system.save_data()
            self.refresh_enrollment_list()
            messagebox.showinfo("Success", "Grade assigned successfully!")
            self.ent_grade.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Grade must be a number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def assign_grade(self):
        # Deprecated: grades are assigned at unit level. Prompt user to use unit assignment.
        messagebox.showinfo("Info", "Grades are assigned per course-unit. Select an enrollment row or use 'Assign Grade To Selected Unit'.")

    def generate_report(self):
        try:
            student_str = self.cb_report_student.get()
            if not student_str:
                messagebox.showwarning("Warning", "Please select a student")
                return

            sid = self._get_student_id_by_name(student_str)
            report = self.system.get_student_report(sid)
            
            self.txt_report.delete(1.0, tk.END)
            self.txt_report.insert(tk.END, f"REPORT CARD\n{'='*110}\n")
            self.txt_report.insert(tk.END, f"Name: {report['student_name']}\nID: {report['student_id']}\n\n")
            
            # UPDATED HEADER: Included 'C.Cred' (Course) and 'U.Cred' (Unit)
            header = f"{'Course':<20} {'C.Cred':<7} {'Unit':<18} {'U.Cred':<7} {'Grade':<8} {'Letter':<8} {'Points':<8} {'Teacher':<16}\n"
            self.txt_report.insert(tk.END, header)
            self.txt_report.insert(tk.END, f"{'-'*110}\n")
            
            for c in report['courses']:
                # The total course credits are stored in c['credits']
                course_total_credits = c.get('credits', 0)
                
                # GPA header line for the course
                self.txt_report.insert(tk.END, f"{c['course_name']} (GPA: {c['course_gpa']:.2f})\n")
                
                for u in c['units']:
                    # Extract values for the row
                    grade = u.get('grade') if u.get('grade') is not None else 'N/A'
                    letter = u.get('letter', 'N/A')
                    point = f"{u.get('point'):.1f}" if isinstance(u.get('point'), (int, float)) else 'N/A'
                    teacher = u.get('teacher', 'Unassigned')
                    unit_credits = u.get('credits', 'N/A') # Grabbing unit credits
                    
                    # UPDATED ROW: Added unit_credits variable and adjusted alignment
                    row = f"{c['course_name'][:18]:<20} {str(course_total_credits):<7} {u['unit_name'][:16]:<18} {str(unit_credits):<7} {str(grade):<8} {letter:<8} {point:<8} {teacher[:16]:<16}\n"
                    self.txt_report.insert(tk.END, row)
                
                self.txt_report.insert(tk.END, "\n")
            
            self.txt_report.insert(tk.END, f"OVERALL CGPA: {report['cgpa']:.2f}\n")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_report_pdf(self):
            report_text = self.txt_report.get("1.0", tk.END).strip()
            if not report_text:
                messagebox.showwarning("Warning", "Please generate a report first.")
                return
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Report as PDF"
            )
            if not filepath:
                return
            try:
                pdf = FPDF()
                pdf.add_page()
                
                # Use a standard built-in font
                pdf.set_font("Courier", size=10)
                for line in report_text.split('\n'):
                    # Providing width, height, and text
                    pdf.cell(w=0, h=5, txt=line, ln=True)
                    
                pdf.output(filepath)
                messagebox.showinfo("Success", "PDF exported successfully!")
                
            except Exception as e:
                # This will show the specific error details to help us debug
                messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")

    def refresh_student_list(self, search_query=""):
        for i in self.tree_students.get_children():
            self.tree_students.delete(i)
            
        query = search_query.lower()
        for s in self.system.students.values():
            # Check if query matches ID, Name, or Email
            if query in s.person_id.lower() or query in s.name.lower() or query in s.email.lower():
                self.tree_students.insert("", "end", values=(s.person_id, s.name, s.email))

    def refresh_course_list(self, search_query=""):
        for i in self.tree_courses.get_children():
            self.tree_courses.delete(i)
            
        query = search_query.lower()
        for c in self.system.courses.values():
            teacher_name = "N/A"
            if c.teacher_id and c.teacher_id in self.system.teachers:
                teacher_name = self.system.teachers[c.teacher_id].name
                
            # Check if query matches Course ID, Name, Credits, or Teacher Name
            if (query in c.course_id.lower() or 
                query in c.name.lower() or 
                query in str(c.credits) or 
                query in teacher_name.lower()):
                self.tree_courses.insert("", "end", values=(c.course_id, c.name, c.credits, teacher_name))

    def refresh_teacher_list(self, search_query=""):
        for i in self.tree_teachers.get_children():
            self.tree_teachers.delete(i)
            
        query = search_query.lower()
        for t in self.system.teachers.values():
            if getattr(t, 'taught_units', None):
                parts = []
                for cid, units in t.taught_units.items():
                    parts.append(f"{cid}({len(units)})")
                courses_str = ", ".join(parts)
            else:
                courses_str = "None"
                
            # Check if query matches ID, Name, Email, Department, or Assigned Courses
            if (query in t.person_id.lower() or 
                query in t.name.lower() or 
                query in t.email.lower() or 
                query in t.department.lower() or
                query in courses_str.lower()):
                self.tree_teachers.insert("", "end", values=(t.person_id, t.name, t.email, t.department, courses_str))

    def export_summary(self):
        try:
            # Calls the method we added to system.py
            self.system.export_courses_summary("courses_summary_report.csv")
            # Shows a popup confirming it worked
            messagebox.showinfo("Success", "Course summary exported successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export summary: {str(e)}")

    def on_student_select(self, event):
        selected = self.tree_students.selection()
        if not selected:
            return
        values = self.tree_students.item(selected[0], 'values')
        self.selected_student_id = values[0]
        self.ent_sid.delete(0, tk.END)
        self.ent_sid.insert(0, values[0])
        self.ent_sid.config(state='readonly')
        self.ent_sname.delete(0, tk.END)
        self.ent_sname.insert(0, values[1])
        self.ent_semail.delete(0, tk.END)
        self.ent_semail.insert(0, values[2])

    def on_course_select(self, event):
        selected = self.tree_courses.selection()
        if not selected:
            return
        values = self.tree_courses.item(selected[0], 'values')
        self.selected_course_id = values[0]
        self.ent_cid.delete(0, tk.END)
        self.ent_cid.insert(0, values[0])
        self.ent_cid.config(state='readonly')
        self.ent_cname.delete(0, tk.END)
        self.ent_cname.insert(0, values[1])
        self.ent_ccredits.delete(0, tk.END)
        self.ent_ccredits.insert(0, values[2])

    def on_teacher_select(self, event):
        selected = self.tree_teachers.selection()
        if not selected:
            return
        values = self.tree_teachers.item(selected[0], 'values')
        self.selected_teacher_id = values[0]
        self.ent_tid.delete(0, tk.END)
        self.ent_tid.insert(0, values[0])
        self.ent_tid.config(state='readonly')
        self.ent_tname.delete(0, tk.END)
        self.ent_tname.insert(0, values[1])
        self.ent_temail.delete(0, tk.END)
        self.ent_temail.insert(0, values[2])
        self.ent_tdept.delete(0, tk.END)
        self.ent_tdept.insert(0, values[3])

    def on_enrollment_select(self, event):
        selected = self.tree_enrollments.selection()
        if not selected:
            return
        values = self.tree_enrollments.item(selected[0], 'values')
        student_id = values[0].split(" - ")[0]
        student_name = values[0].split(" - ", 1)[1]
        course_id = values[1].split(" - ")[0]
        unit_id = values[2].split(" - ")[0]
        self.selected_enrollment = (student_id, course_id, unit_id)
        # set comboboxes: students combobox shows names only
        self.cb_students.set(student_name)
        self.cb_courses.set(values[1])
        # select unit in listbox if present
        try:
            for i in range(self.lb_units.size()):
                if self.lb_units.get(i).split(" - ")[0] == unit_id:
                    self.lb_units.selection_clear(0, tk.END)
                    self.lb_units.selection_set(i)
                    break
        except Exception:
            pass
        self.ent_grade.delete(0, tk.END)
        self.ent_grade.insert(0, values[3])

    def clear_student_form(self):
        self.selected_student_id = None
        self.ent_sid.config(state='normal')
        self.ent_sid.delete(0, tk.END)
        self.ent_sname.delete(0, tk.END)
        self.ent_semail.delete(0, tk.END)

    def clear_course_form(self):
        self.selected_course_id = None
        self.ent_cid.config(state='normal')
        self.ent_cid.delete(0, tk.END)
        self.ent_cname.delete(0, tk.END)
        self.ent_ccredits.delete(0, tk.END)

    def clear_teacher_form(self):
        self.selected_teacher_id = None
        self.ent_tid.config(state='normal')
        self.ent_tid.delete(0, tk.END)
        self.ent_tname.delete(0, tk.END)
        self.ent_temail.delete(0, tk.END)
        self.ent_tdept.delete(0, tk.END)

    def update_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("Warning", "Select a student to update")
            return
        name = self.ent_sname.get()
        email = self.ent_semail.get()
        try:
            self.system.update_student(self.selected_student_id, name, email)
            self.system.save_data()
            self.refresh_student_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "Student updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("Warning", "Select a student to delete")
            return
        if not messagebox.askyesno("Confirm", "Delete selected student and all enrollments?"):
            return
        try:
            self.system.delete_student(self.selected_student_id)
            self.system.save_data()
            self.refresh_student_list()
            self.refresh_enrollment_list()
            self.update_comboboxes()
            self.clear_student_form()
            messagebox.showinfo("Success", "Student deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_course(self):
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Select a course to update")
            return
        name = self.ent_cname.get()
        try:
            credits = int(self.ent_ccredits.get())
            self.system.update_course(self.selected_course_id, name, credits)
            self.system.save_data()
            self.refresh_course_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "Course updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Credits must be a number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_course(self):
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Select a course to delete")
            return
        if not messagebox.askyesno("Confirm", "Delete selected course and remove it from enrollments?"):
            return
        try:
            self.system.delete_course(self.selected_course_id)
            self.system.save_data()
            self.refresh_course_list()
            self.refresh_student_list()
            self.refresh_enrollment_list()
            self.refresh_teacher_list()
            self.update_comboboxes()
            self.clear_course_form()
            messagebox.showinfo("Success", "Course deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_teacher(self):
        if not self.selected_teacher_id:
            messagebox.showwarning("Warning", "Select a teacher to update")
            return
        name = self.ent_tname.get()
        email = self.ent_temail.get()
        dept = self.ent_tdept.get()
        try:
            self.system.update_teacher(self.selected_teacher_id, name, email, dept)
            self.system.save_data()
            self.refresh_teacher_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "Teacher updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_teacher(self):
        if not self.selected_teacher_id:
            messagebox.showwarning("Warning", "Select a teacher to delete")
            return
        if not messagebox.askyesno("Confirm", "Delete selected teacher and unassign courses?"):
            return
        try:
            self.system.delete_teacher(self.selected_teacher_id)
            self.system.save_data()
            self.refresh_course_list()
            self.refresh_teacher_list()
            self.update_comboboxes()
            self.clear_teacher_form()
            messagebox.showinfo("Success", "Teacher deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_enrollment_list(self):
        for i in self.tree_enrollments.get_children():
            self.tree_enrollments.delete(i)
        for student in self.system.students.values():
            for course_id, data in student.enrolled_courses.items():
                course = self.system.courses.get(course_id)
                if course:
                    student_label = f"{student.person_id} - {student.name}"
                    course_label = f"{course.course_id} - {course.name}"
                    for unit_id, grade in data.get('units', {}).items():
                        # find unit name
                        unit_name = unit_id
                        for u in course.units:
                            if u.get('unit_id') == unit_id:
                                unit_name = u.get('name')
                                break
                        unit_label = f"{unit_id} - {unit_name}"
                        self.tree_enrollments.insert("", "end", values=(student_label, course_label, unit_label, grade if grade is not None else "N/A"))

    def delete_enrollment(self):
        if not self.selected_enrollment:
            messagebox.showwarning("Warning", "Select an enrollment to remove")
            return
        if not messagebox.askyesno("Confirm", "Remove selected enrollment?"):
            return
        # selected_enrollment contains (student_id, course_id, unit_id)
        student_id, course_id, unit_id = self.selected_enrollment
        try:
            # remove unit enrollment
            self.system.remove_unit_enrollment(student_id, course_id, unit_id)
            self.system.save_data()
            self.refresh_enrollment_list()
            self.refresh_student_list()
            self.selected_enrollment = None
            messagebox.showinfo("Success", "Enrollment removed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_comboboxes(self):
        s_list = [f"{s.name}" for s in self.system.students.values()]
        c_list = [f"{c.course_id} - {c.name}" for c in self.system.courses.values()]
        t_list = [f"{t.person_id} - {t.name}" for t in self.system.teachers.values()]
        
        self.cb_students['values'] = s_list
        self.cb_courses['values'] = c_list
        self.cb_report_student['values'] = s_list
        self.cb_assign_teacher['values'] = t_list
        self.cb_assign_course['values'] = c_list

        # update units listbox if course selected
        try:
            current = self.cb_courses.get()
            if current:
                cid = current.split(" - ")[0]
                course = self.system.courses.get(cid)
                self.lb_units.delete(0, tk.END)
                if course:
                    for u in course.units:
                        self.lb_units.insert(tk.END, f"{u.get('unit_id')} - {u.get('name')}")
        except Exception:
            pass

        # update analysis student combobox as well
        try:
            self.cb_analysis_student['values'] = s_list
        except Exception:
            pass

    def _get_student_id_by_name(self, name):
        for s in self.system.students.values():
            if s.name == name:
                return s.person_id
        raise ValueError(f"Student with name '{name}' not found")
    
   

    def open_manage_units_dialog(self):
        cid = self.selected_course_id
        # fallback to entry if not selected
        if not cid:
            cid = self.ent_cid.get().strip()
        if not cid:
            messagebox.showwarning("Warning", "Select a course first to manage units")
            return
        course = self.system.courses.get(cid)
        if not course:
            messagebox.showerror("Error", f"Course {cid} not found")
            return

        dlg = tk.Toplevel(self.root)
        dlg.title(f"Manage Units for {cid} - {course.name}")
        dlg.geometry("620x420")

        tree = ttk.Treeview(dlg, columns=("UnitID", "Name", "Credits"), show='headings', selectmode='browse')
        tree.heading('UnitID', text='Unit ID')
        tree.heading('Name', text='Unit Name')
        tree.heading('Credits', text='Credits')
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        form = tk.Frame(dlg)
        form.pack(fill='x', padx=10, pady=5)
        tk.Label(form, text='Unit ID:').grid(row=0, column=0, padx=5, pady=3)
        ent_uid = tk.Entry(form)
        ent_uid.grid(row=0, column=1, padx=5, pady=3)
        tk.Label(form, text='Name:').grid(row=0, column=2, padx=5, pady=3)
        ent_uname = tk.Entry(form, width=30)
        ent_uname.grid(row=0, column=3, padx=5, pady=3)
        tk.Label(form, text='Credits:').grid(row=0, column=4, padx=5, pady=3)
        ent_ucredits = tk.Entry(form, width=8)
        ent_ucredits.grid(row=0, column=5, padx=5, pady=3)

        btn_frame = tk.Frame(dlg)
        btn_frame.pack(fill='x', padx=10, pady=5)

        def refresh_tree():
            for r in tree.get_children():
                tree.delete(r)
            for u in course.units:
                tree.insert('', 'end', values=(u.get('unit_id'), u.get('name'), u.get('credits')))

        def on_tree_select(event=None):
            sel = tree.selection()
            if not sel:
                return
            vals = tree.item(sel[0], 'values')
            ent_uid.delete(0, tk.END)
            ent_uid.insert(0, vals[0])
            ent_uid.config(state='readonly')
            ent_uname.delete(0, tk.END)
            ent_uname.insert(0, vals[1])
            ent_ucredits.delete(0, tk.END)
            ent_ucredits.insert(0, vals[2])

        def add_new_unit():
            uid = ent_uid.get().strip()
            name = ent_uname.get().strip()
            if self.is_unit_id_taken(cid, uid, current_editing_id=None):
                messagebox.showerror('Error', f"Unit ID '{uid}' already exists!")
                return
            
            try:
                credits = float(ent_ucredits.get())
            except Exception:
                messagebox.showerror('Error', 'Credits must be a number')
                return
            try:
                self.system.add_course_unit(cid, uid, name, credits)
                self.system.save_data()
                refresh_tree()
                self.refresh_course_list()
                self.update_comboboxes()
                messagebox.showinfo('Success', f'Added unit {uid}')
            except Exception as e:
                messagebox.showerror('Error', str(e))

        def save_unit():
            uid = ent_uid.get().strip()
            name = ent_uname.get().strip()
            try:
                credits = float(ent_ucredits.get())
            except Exception:
                messagebox.showerror('Error', 'Credits must be a number')
                return
            try:
                self.system.update_course_unit(cid, uid, name=name, credits=credits)
                self.system.save_data()
                refresh_tree()
                self.refresh_course_list()
                self.update_comboboxes()
                messagebox.showinfo('Success', f'Updated unit {uid}')
            except Exception as e:
                messagebox.showerror('Error', str(e))

        def delete_unit():
            uid = ent_uid.get().strip()
            if not uid:
                messagebox.showwarning('Warning', 'Select a unit to delete')
                return
            if not messagebox.askyesno('Confirm', f'Delete unit {uid}? This will remove related enrollments.'):
                return
            try:
                self.system.delete_course_unit(cid, uid)
                self.system.save_data()
                refresh_tree()
                self.refresh_course_list()
                self.update_comboboxes()
                self.refresh_enrollment_list()
                ent_uid.config(state='normal')
                ent_uid.delete(0, tk.END)
                ent_uname.delete(0, tk.END)
                ent_ucredits.delete(0, tk.END)
                messagebox.showinfo('Success', f'Deleted unit {uid}')
            except Exception as e:
                messagebox.showerror('Error', str(e))

        tk.Button(btn_frame, text='Add New', command=add_new_unit, bg=self.secondary_color, fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text='Save', command=save_unit, bg='#F39C12', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text='Delete', command=delete_unit, bg=self.accent_color, fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text='Close', command=dlg.destroy).pack(side='right', padx=5)

        tree.bind('<<TreeviewSelect>>', on_tree_select)
        refresh_tree()

    def on_cb_course_selected(self, event):
        try:
            course_str = self.cb_courses.get()
            if not course_str:
                return
            cid = course_str.split(" - ")[0]
            course = self.system.courses.get(cid)
            self.lb_units.delete(0, tk.END)
            if course:
                for u in course.units:
                    self.lb_units.insert(tk.END, f"{u.get('unit_id')} - {u.get('name')}")
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = EduManageGUI(root)
    root.mainloop()
