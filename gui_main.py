import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from system import EducationSystem
from fpdf import FPDF
import re
import os

# Set appearance and default theme
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class EduManageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EduManage - Advanced Education Management System")
        self.root.geometry("1200x800")
        self.system = EducationSystem()
        self.selected_student_id = None
        self.selected_course_id = None
        self.selected_teacher_id = None
        self.selected_enrollment = None
        self.dark_mode = True  # Track current theme

        # Define Colors for light and dark modes
        self.light_colors = {
            "primary": "#2C3E50",
            "secondary": "#3498DB",
            "bg": "#ECF0F1",
            "accent": "#E74C3C",
            "text": "#2C3E50"
        }
        
        self.dark_colors = {
            "primary": "#1a1a2e",
            "secondary": "#0f3460",
            "bg": "#16213e",
            "accent": "#e94560",
            "text": "#eaeaea"
        }

        self.current_colors = self.dark_colors if self.dark_mode else self.light_colors
        
        self.root.configure(fg_color=self.current_colors["bg"])
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        pass  # customtkinter handles styling automatically

    def validate_email(self, email):
        """Validate email format using regex pattern."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def toggle_theme(self):
        """Toggle between light and dark modes."""
        self.dark_mode = not self.dark_mode
        new_mode = "dark" if self.dark_mode else "light"
        ctk.set_appearance_mode(new_mode)
        self.current_colors = self.dark_colors if self.dark_mode else self.light_colors
        self.theme_toggle_btn.configure(text="☀️ Light" if self.dark_mode else "🌙 Dark")

    def create_widgets(self):
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color=self.current_colors["bg"])
        main_container.pack(fill="both", expand=True)

        # Header with theme toggle
        header = ctk.CTkFrame(main_container, fg_color=self.current_colors["primary"], height=80)
        header.pack(fill="x", pady=(0, 10), padx=10)
        header.configure(corner_radius=10)

        header_text = ctk.CTkLabel(
            header,
            text="🎓 EduManage - Advanced Education Management System",
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        )
        header_text.pack(pady=20)

        # Theme toggle button in corner
        self.theme_toggle_btn = ctk.CTkButton(
            header,
            text="☀️ Light",
            command=self.toggle_theme,
            width=100,
            height=30,
            fg_color="#FF9800",
            hover_color="#F57C00",
            text_color="white",
            corner_radius=8
        )
        self.theme_toggle_btn.pack(side="right", padx=20, pady=20)

        # Main Notebook (Tabs) with customtkinter
        self.notebook = ctk.CTkTabview(
            main_container,
            segmented_button_fg_color=self.current_colors["secondary"],
            text_color="white"
        )
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Create tabs
        self.tab_students = self.notebook.add(" 👥 Students ")
        self.tab_courses = self.notebook.add(" 📚 Courses ")
        self.tab_teachers = self.notebook.add(" 👨‍🏫 Teachers ")
        self.tab_enroll = self.notebook.add(" 📝 Enrollment & Grades ")
        self.tab_reports = self.notebook.add(" 📊 Reports ")
        self.tab_analysis = self.notebook.add(" 📈 Analysis ")

        self.setup_student_tab()
        self.setup_course_tab()
        self.setup_teacher_tab()
        self.setup_enroll_tab()
        self.setup_report_tab()
        self.setup_analysis_tab()
        self.update_comboboxes()

    def create_input_frame(self, parent, title):
        """Create a styled input frame."""
        frame = ctk.CTkFrame(parent, fg_color=self.current_colors.get("secondary", "#3498DB"), corner_radius=10)
        frame.pack(fill="x", padx=10, pady=10)
        
        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        )
        label.pack(pady=(10, 0))
        
        inner_frame = ctk.CTkFrame(frame, fg_color=self.current_colors["bg"], corner_radius=8)
        inner_frame.pack(fill="x", padx=10, pady=10)
        
        return inner_frame

    def setup_student_tab(self):
        # Input Frame
        input_frame = self.create_input_frame(self.tab_students, "Student Details")

        # Create two columns in input frame
        col1 = ctk.CTkFrame(input_frame, fg_color=self.current_colors["bg"])
        col1.pack(fill="x", padx=5, pady=5)

        # ID field
        ctk.CTkLabel(col1, text="Student ID:", text_color=self.current_colors["text"]).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_sid = ctk.CTkEntry(col1, placeholder_text="Enter ID", corner_radius=8)
        self.ent_sid.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Name field
        ctk.CTkLabel(col1, text="Name:", text_color=self.current_colors["text"]).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_sname = ctk.CTkEntry(col1, placeholder_text="Enter name", corner_radius=8)
        self.ent_sname.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Email field
        ctk.CTkLabel(col1, text="Email:", text_color=self.current_colors["text"]).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.ent_semail = ctk.CTkEntry(col1, placeholder_text="student@example.com", corner_radius=8)
        self.ent_semail.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        col1.columnconfigure((1, 3, 5), weight=1)

        # Buttons frame
        btn_frame = ctk.CTkFrame(input_frame, fg_color=self.current_colors["bg"])
        btn_frame.pack(fill="x", padx=5, pady=10)

        ctk.CTkButton(btn_frame, text="➕ Add Student", command=self.add_student, corner_radius=8, width=120).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏️ Update", command=self.update_student, fg_color="#F39C12", hover_color="#E67E22", corner_radius=8, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Delete", command=self.delete_student, fg_color="#E74C3C", hover_color="#C0392B", corner_radius=8, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔄 Clear", command=self.clear_student_form, fg_color="#7F8C8D", hover_color="#5D6D7B", corner_radius=8, width=100).pack(side="left", padx=5)

        # Search frame
        search_frame = ctk.CTkFrame(self.tab_students, fg_color=self.current_colors["bg"])
        search_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(search_frame, text="🔍 Search:", text_color=self.current_colors["text"]).pack(side="left", padx=5)
        self.ent_search_student = ctk.CTkEntry(search_frame, placeholder_text="Search students...", corner_radius=8)
        self.ent_search_student.pack(side="left", padx=5, fill="x", expand=True)
        self.ent_search_student.bind("<KeyRelease>", lambda e: self.refresh_student_list(self.ent_search_student.get()))

        # Table Frame
        table_frame = ctk.CTkFrame(self.tab_students, fg_color=self.current_colors["bg"])
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Using TTK Treeview with custom styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', 
                       background='#2b2b2b' if self.dark_mode else 'white',
                       foreground='white' if self.dark_mode else 'black',
                       rowheight=25,
                       fieldbackground='#2b2b2b' if self.dark_mode else 'white')
        style.map('Treeview', background=[('selected', '#3498DB')])

        self.tree_students = ttk.Treeview(table_frame, columns=("ID", "Name", "Email"), show="headings", selectmode="browse", height=15)
        self.tree_students.heading("ID", text="Student ID")
        self.tree_students.heading("Name", text="Name")
        self.tree_students.heading("Email", text="Email")
        self.tree_students.column("ID", width=100)
        self.tree_students.column("Name", width=200)
        self.tree_students.column("Email", width=300)
        self.tree_students.pack(fill="both", expand=True)
        self.tree_students.bind("<<TreeviewSelect>>", self.on_student_select)
        self.refresh_student_list()

    def setup_course_tab(self):
        # Input Frame
        input_frame = self.create_input_frame(self.tab_courses, "Course Details")

        col1 = ctk.CTkFrame(input_frame, fg_color=self.current_colors["bg"])
        col1.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(col1, text="Course ID:", text_color=self.current_colors["text"]).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_cid = ctk.CTkEntry(col1, placeholder_text="Enter ID", corner_radius=8)
        self.ent_cid.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(col1, text="Name:", text_color=self.current_colors["text"]).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_cname = ctk.CTkEntry(col1, placeholder_text="Enter name", corner_radius=8)
        self.ent_cname.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(col1, text="Credits:", text_color=self.current_colors["text"]).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.ent_ccredits = ctk.CTkEntry(col1, placeholder_text="Credits", corner_radius=8, width=80)
        self.ent_ccredits.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        col1.columnconfigure((1, 3, 5), weight=1)

        # Buttons
        btn_frame = ctk.CTkFrame(input_frame, fg_color=self.current_colors["bg"])
        btn_frame.pack(fill="x", padx=5, pady=10)

        ctk.CTkButton(btn_frame, text="➕ Add Course", command=self.add_course, corner_radius=8, width=120).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏️ Update", command=self.update_course, fg_color="#F39C12", hover_color="#E67E22", corner_radius=8, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Delete", command=self.delete_course, fg_color="#E74C3C", hover_color="#C0392B", corner_radius=8, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="📥 Export", command=self.export_summary, fg_color="#27AE60", hover_color="#229954", corner_radius=8, width=100).pack(side="left", padx=5)

        # Search frame
        search_frame = ctk.CTkFrame(self.tab_courses, fg_color=self.current_colors["bg"])
        search_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(search_frame, text="🔍 Search:", text_color=self.current_colors["text"]).pack(side="left", padx=5)
        self.ent_search_course = ctk.CTkEntry(search_frame, placeholder_text="Search courses...", corner_radius=8)
        self.ent_search_course.pack(side="left", padx=5, fill="x", expand=True)
        self.ent_search_course.bind("<KeyRelease>", lambda e: self.refresh_course_list(self.ent_search_course.get()))

        # Table Frame
        table_frame = ctk.CTkFrame(self.tab_courses, fg_color=self.current_colors["bg"])
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_courses = ttk.Treeview(table_frame, columns=("ID", "Name", "Credits", "Teacher"), show="headings", selectmode="browse", height=15)
        self.tree_courses.heading("ID", text="Course ID")
        self.tree_courses.heading("Name", text="Name")
        self.tree_courses.heading("Credits", text="Credits")
        self.tree_courses.heading("Teacher", text="Teacher")
        self.tree_courses.column("ID", width=100)
        self.tree_courses.column("Name", width=200)
        self.tree_courses.column("Credits", width=100)
        self.tree_courses.column("Teacher", width=200)
        self.tree_courses.pack(fill="both", expand=True)
        self.tree_courses.bind("<<TreeviewSelect>>", self.on_course_select)
        self.refresh_course_list()

        # Unit management
        unit_frame = self.create_input_frame(self.tab_courses, "Manage Units for Selected Course")

        unit_col = ctk.CTkFrame(unit_frame, fg_color=self.current_colors["bg"])
        unit_col.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(unit_col, text="Unit ID:", text_color=self.current_colors["text"]).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_unit_id = ctk.CTkEntry(unit_col, placeholder_text="Enter ID", corner_radius=8)
        self.ent_unit_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(unit_col, text="Unit Name:", text_color=self.current_colors["text"]).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_unit_name = ctk.CTkEntry(unit_col, placeholder_text="Enter name", corner_radius=8)
        self.ent_unit_name.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(unit_col, text="Credits:", text_color=self.current_colors["text"]).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.ent_unit_credits = ctk.CTkEntry(unit_col, placeholder_text="Credits", corner_radius=8, width=80)
        self.ent_unit_credits.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        unit_col.columnconfigure((1, 3, 5), weight=1)

        unit_btn = ctk.CTkFrame(unit_frame, fg_color=self.current_colors["bg"])
        unit_btn.pack(fill="x", padx=5, pady=10)

        ctk.CTkButton(unit_btn, text="➕ Add Unit", command=self.add_unit_to_course, corner_radius=8, width=120).pack(side="left", padx=5)
        ctk.CTkButton(unit_btn, text="⚙️ Manage", command=self.open_manage_units_dialog, fg_color="#8E44AD", hover_color="#7D3C98", corner_radius=8, width=120).pack(side="left", padx=5)

    def setup_teacher_tab(self):
        # Input Frame
        input_frame = self.create_input_frame(self.tab_teachers, "Teacher Details")

        col1 = ctk.CTkFrame(input_frame, fg_color=self.current_colors["bg"])
        col1.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(col1, text="Teacher ID:", text_color=self.current_colors["text"]).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_tid = ctk.CTkEntry(col1, placeholder_text="Enter ID", corner_radius=8)
        self.ent_tid.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(col1, text="Name:", text_color=self.current_colors["text"]).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_tname = ctk.CTkEntry(col1, placeholder_text="Enter name", corner_radius=8)
        self.ent_tname.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(col1, text="Email:", text_color=self.current_colors["text"]).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.ent_temail = ctk.CTkEntry(col1, placeholder_text="teacher@example.com", corner_radius=8)
        self.ent_temail.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        col1.columnconfigure((1, 3, 5), weight=1)

        col2 = ctk.CTkFrame(input_frame, fg_color=self.current_colors["bg"])
        col2.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(col2, text="Department:", text_color=self.current_colors["text"]).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_tdept = ctk.CTkEntry(col2, placeholder_text="Enter department", corner_radius=8)
        self.ent_tdept.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        col2.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ctk.CTkFrame(input_frame, fg_color=self.current_colors["bg"])
        btn_frame.pack(fill="x", padx=5, pady=10)

        ctk.CTkButton(btn_frame, text="➕ Add Teacher", command=self.add_teacher, corner_radius=8, width=120).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏️ Update", command=self.update_teacher, fg_color="#F39C12", hover_color="#E67E22", corner_radius=8, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Delete", command=self.delete_teacher, fg_color="#E74C3C", hover_color="#C0392B", corner_radius=8, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔄 Clear", command=self.clear_teacher_form, fg_color="#7F8C8D", hover_color="#5D6D7B", corner_radius=8, width=100).pack(side="left", padx=5)

        # Assignment Frame
        assign_frame = self.create_input_frame(self.tab_teachers, "Assign Teacher to Course/Unit")

        assign_col = ctk.CTkFrame(assign_frame, fg_color=self.current_colors["bg"])
        assign_col.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(assign_col, text="Teacher:", text_color=self.current_colors["text"]).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cb_assign_teacher = ctk.CTkComboBox(assign_col, corner_radius=8, state="readonly")
        self.cb_assign_teacher.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(assign_col, text="Course:", text_color=self.current_colors["text"]).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.cb_assign_course = ctk.CTkComboBox(assign_col, corner_radius=8, state="readonly")
        self.cb_assign_course.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.cb_assign_course.bind("<<ComboboxSelected>>", self.on_assign_course_selected)

        ctk.CTkLabel(assign_col, text="Unit:", text_color=self.current_colors["text"]).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.cb_assign_unit = ctk.CTkComboBox(assign_col, corner_radius=8, state="readonly")
        self.cb_assign_unit.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        assign_col.columnconfigure((1, 3, 5), weight=1)

        assign_btn = ctk.CTkFrame(assign_frame, fg_color=self.current_colors["bg"])
        assign_btn.pack(fill="x", padx=5, pady=10)

        ctk.CTkButton(assign_btn, text="Assign Course", command=self.assign_course_only, fg_color="#2980B9", hover_color="#1F618D", corner_radius=8, width=120).pack(side="left", padx=5)
        ctk.CTkButton(assign_btn, text="Assign Unit", command=self.assign_unit_only, fg_color="#27AE60", hover_color="#1E8449", corner_radius=8, width=120).pack(side="left", padx=5)

        # Search frame
        search_frame = ctk.CTkFrame(self.tab_teachers, fg_color=self.current_colors["bg"])
        search_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(search_frame, text="🔍 Search:", text_color=self.current_colors["text"]).pack(side="left", padx=5)
        self.ent_search_teacher = ctk.CTkEntry(search_frame, placeholder_text="Search teachers...", corner_radius=8)
        self.ent_search_teacher.pack(side="left", padx=5, fill="x", expand=True)
        self.ent_search_teacher.bind("<KeyRelease>", lambda e: self.refresh_teacher_list(self.ent_search_teacher.get()))

        # Table Frame
        table_frame = ctk.CTkFrame(self.tab_teachers, fg_color=self.current_colors["bg"])
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_teachers = ttk.Treeview(table_frame, columns=("ID", "Name", "Email", "Department", "Courses"), show="headings", selectmode="browse", height=15)
        self.tree_teachers.heading("ID", text="Teacher ID")
        self.tree_teachers.heading("Name", text="Name")
        self.tree_teachers.heading("Email", text="Email")
        self.tree_teachers.heading("Department", text="Department")
        self.tree_teachers.heading("Courses", text="Courses Taught")
        self.tree_teachers.column("ID", width=80)
        self.tree_teachers.column("Name", width=150)
        self.tree_teachers.column("Email", width=180)
        self.tree_teachers.column("Department", width=120)
        self.tree_teachers.column("Courses", width=150)
        self.tree_teachers.pack(fill="both", expand=True)
        self.tree_teachers.bind("<<TreeviewSelect>>", self.on_teacher_select)
        self.refresh_teacher_list()

    def setup_enroll_tab(self):
        top_frame = ctk.CTkFrame(self.tab_enroll, fg_color=self.current_colors["bg"])
        top_frame.pack(fill="x", padx=10, pady=10)

        action_frame = self.create_input_frame(top_frame, "Enroll Student & Assign Grade")

        action_col = ctk.CTkFrame(action_frame, fg_color=self.current_colors["bg"])
        action_col.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(action_col, text="Student:", text_color=self.current_colors["text"]).grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.cb_students = ctk.CTkComboBox(action_col, corner_radius=8, state="readonly")
        self.cb_students.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        ctk.CTkLabel(action_col, text="Course:", text_color=self.current_colors["text"]).grid(row=0, column=2, padx=5, pady=10, sticky="w")
        self.cb_courses = ctk.CTkComboBox(action_col, corner_radius=8, state="readonly")
        self.cb_courses.grid(row=0, column=3, padx=5, pady=10, sticky="ew")
        self.cb_courses.bind("<<ComboboxSelected>>", self.on_cb_course_selected)

        ctk.CTkButton(action_col, text="📝 Enroll Course", command=self.enroll_student, corner_radius=8, width=130).grid(row=0, column=4, padx=10)

        action_col.columnconfigure((1, 3), weight=1)

        grade_col = ctk.CTkFrame(action_frame, fg_color=self.current_colors["bg"])
        grade_col.pack(fill="x", padx=5, pady=10)

        ctk.CTkLabel(grade_col, text="Grade (0-100):", text_color=self.current_colors["text"]).pack(side="left", padx=5)
        self.ent_grade = ctk.CTkEntry(grade_col, placeholder_text="Enter grade", width=100, corner_radius=8)
        self.ent_grade.pack(side="left", padx=5)

        ctk.CTkButton(grade_col, text="✔️ Assign Grade", command=self.assign_grade, fg_color="#27AE60", hover_color="#1E8449", corner_radius=8, width=130).pack(side="left", padx=5)
        ctk.CTkButton(grade_col, text="🗑️ Remove", command=self.delete_enrollment, fg_color="#E74C3C", hover_color="#C0392B", corner_radius=8, width=100).pack(side="left", padx=5)

        # Units list
        units_frame = self.create_input_frame(self.tab_enroll, "Course Units (select to enroll or grade)")

        units_inner = ctk.CTkFrame(units_frame, fg_color=self.current_colors["bg"])
        units_inner.pack(fill="both", expand=True, padx=5, pady=5)

        # Create a frame for listbox and scrollbar
        list_container = ctk.CTkFrame(units_inner, fg_color=self.current_colors["bg"])
        list_container.pack(fill="both", expand=True, side="left")

        self.lb_units = ctk.CTkTextbox(list_container, activate_scrollbars=True, corner_radius=8, height=100)
        self.lb_units.pack(fill="both", expand=True, padx=5, pady=5)

        # Buttons for units
        btns_units = ctk.CTkFrame(units_inner, fg_color=self.current_colors["bg"])
        btns_units.pack(side="left", padx=5)

        ctk.CTkButton(btns_units, text="📝 Enroll Units", command=self.enroll_selected_units, fg_color="#2980B9", hover_color="#1F618D", corner_radius=8).pack(fill="x", pady=3)
        ctk.CTkButton(btns_units, text="✔️ Grade Unit", command=self.assign_grade_to_selected_unit, fg_color="#27AE60", hover_color="#1E8449", corner_radius=8).pack(fill="x", pady=3)

        # Enrollments list
        list_frame = self.create_input_frame(self.tab_enroll, "Current Enrollments")

        table_frame = ctk.CTkFrame(list_frame, fg_color=self.current_colors["bg"])
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree_enrollments = ttk.Treeview(table_frame, columns=("Student", "Course", "Unit", "Grade"), show="headings", selectmode="browse", height=10)
        self.tree_enrollments.heading("Student", text="Student")
        self.tree_enrollments.heading("Course", text="Course")
        self.tree_enrollments.heading("Unit", text="Unit")
        self.tree_enrollments.heading("Grade", text="Grade")
        self.tree_enrollments.column("Student", width=200)
        self.tree_enrollments.column("Course", width=150)
        self.tree_enrollments.column("Unit", width=150)
        self.tree_enrollments.column("Grade", width=100)
        self.tree_enrollments.pack(fill="both", expand=True)
        self.tree_enrollments.bind("<<TreeviewSelect>>", self.on_enrollment_select)
        self.refresh_enrollment_list()

    def setup_report_tab(self):
        frame = ctk.CTkFrame(self.tab_reports, fg_color=self.current_colors["bg"])
        frame.pack(fill="x", padx=10, pady=10)

        report_frame = self.create_input_frame(frame, "Generate Student Report")

        inner = ctk.CTkFrame(report_frame, fg_color=self.current_colors["bg"])
        inner.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(inner, text="Select Student:", text_color=self.current_colors["text"]).pack(side="left", padx=5)
        self.cb_report_student = ctk.CTkComboBox(inner, corner_radius=8, state="readonly")
        self.cb_report_student.pack(side="left", padx=5, fill="x", expand=True)

        ctk.CTkButton(inner, text="📄 Generate", command=self.generate_report, corner_radius=8, width=120).pack(side="left", padx=5)
        ctk.CTkButton(inner, text="📥 Export PDF", command=self.export_report_pdf, fg_color="#8E44AD", hover_color="#7D3C98", corner_radius=8, width=130).pack(side="left", padx=5)

        text_frame = ctk.CTkFrame(self.tab_reports, fg_color=self.current_colors["bg"])
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.txt_report = ctk.CTkTextbox(text_frame, corner_radius=10, font=("Courier", 11))
        self.txt_report.pack(fill="both", expand=True)

    def setup_analysis_tab(self):
        """Setup analysis dashboard with charts."""
        btn_frame = ctk.CTkFrame(self.tab_analysis, fg_color=self.current_colors["bg"])
        btn_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(btn_frame, text="Student:", text_color=self.current_colors["text"]).pack(side='left', padx=5)
        self.cb_analysis_student = ctk.CTkComboBox(btn_frame, corner_radius=8, state="readonly")
        self.cb_analysis_student.pack(side='left', padx=5)

        ctk.CTkButton(btn_frame, text="📊 Refresh Charts", command=self.refresh_analysis, corner_radius=8, width=150).pack(side="left", padx=10)

        self.canvas_frame = ctk.CTkFrame(self.tab_analysis, fg_color=self.current_colors["bg"])
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def refresh_analysis(self):
        """Refresh and display analysis charts."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        analytics = self.system.get_analytics()

        fig = Figure(figsize=(14, 8), dpi=80, facecolor=self.current_colors["bg"])
        
        # Chart 1
        if analytics["students_per_course"]:
            ax1 = fig.add_subplot(2, 2, 1)
            courses = list(analytics["students_per_course"].keys())
            counts = list(analytics["students_per_course"].values())
            ax1.bar(courses, counts, color="#3498DB", edgecolor="#2C3E50", linewidth=1.5)
            ax1.set_title("Students Enrolled per Course", fontsize=12, fontweight='bold', color=self.current_colors["text"])
            ax1.set_xlabel("Course", color=self.current_colors["text"])
            ax1.set_ylabel("Count", color=self.current_colors["text"])
            ax1.tick_params(axis='x', rotation=45, colors=self.current_colors["text"])
            ax1.tick_params(axis='y', colors=self.current_colors["text"])
            ax1.set_facecolor("#2C3E50" if self.dark_mode else "white")

        # Chart 2
        if analytics["grades_distribution"]:
            ax2 = fig.add_subplot(2, 2, 2)
            order = ['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']
            dist = [analytics["grades_distribution"].get(k, 0) for k in order]
            bars = ax2.bar(order, dist, color="#2ECC71", edgecolor="#27AE60", linewidth=1.5)
            ax2.set_title("Grade Distribution", fontsize=12, fontweight='bold', color=self.current_colors["text"])
            ax2.set_xlabel("Letter Grade", color=self.current_colors["text"])
            ax2.set_ylabel("Count", color=self.current_colors["text"])
            ax2.tick_params(axis='x', rotation=45, colors=self.current_colors["text"])
            ax2.tick_params(axis='y', colors=self.current_colors["text"])
            ax2.set_facecolor("#2C3E50" if self.dark_mode else "white")

        # Chart 3
        if analytics["teacher_workload"]:
            ax3 = fig.add_subplot(2, 2, 3)
            teachers = list(analytics["teacher_workload"].keys())
            workload = list(analytics["teacher_workload"].values())
            ax3.barh(teachers, workload, color="#E74C3C", edgecolor="#C0392B", linewidth=1.5)
            ax3.set_title("Teacher Workload", fontsize=12, fontweight='bold', color=self.current_colors["text"])
            ax3.set_xlabel("Number of Units", color=self.current_colors["text"])
            ax3.tick_params(colors=self.current_colors["text"])
            ax3.set_facecolor("#2C3E50" if self.dark_mode else "white")

        # Chart 4
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.axis('off')
        stats_text = f"SYSTEM STATISTICS\n\n✓ Total Students: {analytics['total_students']}\n✓ Total Courses: {analytics['total_courses']}\n✓ Total Teachers: {analytics['total_teachers']}\n✓ Avg Grade: {analytics['avg_grade']:.1f}%"
        ax4.text(0.5, 0.5, stats_text, fontsize=12, ha='center', va='center',
                family='monospace', color=self.current_colors["text"],
                bbox=dict(boxstyle='round', facecolor='#3498DB', alpha=0.7, pad=1))

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ========== CRUD OPERATIONS ==========

    def add_student(self):
        sid = self.ent_sid.get().strip()
        name = self.ent_sname.get().strip()
        email = self.ent_semail.get().strip()
        
        if not sid or not name or not email:
            messagebox.showwarning("Warning", "All fields are required")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
            return
            
        try:
            self.system.add_student(sid, name, email)
            self.system.save_data()
            self.refresh_student_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "✓ Student added successfully!")
            self.ent_sid.delete(0, 'end')
            self.ent_sname.delete(0, 'end')
            self.ent_semail.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_course(self):
        cid = self.ent_cid.get().strip()
        name = self.ent_cname.get().strip()
        
        if not cid or not name:
            messagebox.showwarning("Warning", "Course ID and Name are required")
            return
            
        try:
            credits = int(self.ent_ccredits.get())
            self.system.add_course(cid, name, credits)
            self.system.save_data()
            self.refresh_course_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "✓ Course added successfully!")
            self.ent_cid.delete(0, 'end')
            self.ent_cname.delete(0, 'end')
            self.ent_ccredits.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_teacher(self):
        tid = self.ent_tid.get().strip()
        name = self.ent_tname.get().strip()
        email = self.ent_temail.get().strip()
        dept = self.ent_tdept.get().strip()
        
        if not tid or not name or not email or not dept:
            messagebox.showwarning("Warning", "All fields are required")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
            return
            
        try:
            self.system.add_teacher(tid, name, email, dept)
            self.system.save_data()
            self.refresh_teacher_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "✓ Teacher added successfully!")
            self.ent_tid.delete(0, 'end')
            self.ent_tname.delete(0, 'end')
            self.ent_temail.delete(0, 'end')
            self.ent_tdept.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def is_unit_id_taken(self, cid, uid, current_editing_id=None):
        """Check if unit ID is already taken in course."""
        course = self.system.courses.get(cid)
        if not course:
            return False
        
        for u in course.units:
            if u['unit_id'] == uid and u['unit_id'] != current_editing_id:
                return True
        return False

    def add_unit_to_course(self):
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Select a course first")
            return
        
        uid = self.ent_unit_id.get().strip()
        uname = self.ent_unit_name.get().strip()
        
        if not uid or not uname:
            messagebox.showwarning("Warning", "Unit ID and Name are required")
            return
        
        if self.is_unit_id_taken(self.selected_course_id, uid):
            messagebox.showerror("Error", f"Unit ID '{uid}' already exists in this course!")
            return
            
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
            messagebox.showinfo("Success", f"✓ Unit {uid} added to course")
            
            self.ent_unit_id.delete(0, 'end')
            self.ent_unit_name.delete(0, 'end')
            self.ent_unit_credits.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("Warning", "Select a student to update")
            return
        name = self.ent_sname.get().strip()
        email = self.ent_semail.get().strip()
        
        if not name or not email:
            messagebox.showwarning("Warning", "Name and email are required")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
            return
            
        try:
            self.system.update_student(self.selected_student_id, name, email)
            self.system.save_data()
            self.refresh_student_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "✓ Student updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_course(self):
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Select a course to update")
            return
        name = self.ent_cname.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Course name is required")
            return
            
        try:
            credits = int(self.ent_ccredits.get())
            self.system.update_course(self.selected_course_id, name, credits)
            self.system.save_data()
            self.refresh_course_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "✓ Course updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_teacher(self):
        if not self.selected_teacher_id:
            messagebox.showwarning("Warning", "Select a teacher to update")
            return
        name = self.ent_tname.get().strip()
        email = self.ent_temail.get().strip()
        dept = self.ent_tdept.get().strip()
        
        if not name or not email or not dept:
            messagebox.showwarning("Warning", "Name, email, and department are required")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
            return
            
        try:
            self.system.update_teacher(self.selected_teacher_id, name, email, dept)
            self.system.save_data()
            self.refresh_teacher_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", "✓ Teacher updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("Warning", "Select a student to delete")
            return
        if not messagebox.askyesno("Confirm", "Delete selected student?"):
            return
        try:
            self.system.delete_student(self.selected_student_id)
            self.system.save_data()
            self.refresh_student_list()
            self.refresh_enrollment_list()
            self.update_comboboxes()
            self.clear_student_form()
            messagebox.showinfo("Success", "✓ Student deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_course(self):
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Select a course to delete")
            return
        if not messagebox.askyesno("Confirm", "Delete selected course and all enrollments?"):
            return
        try:
            self.system.delete_course(self.selected_course_id)
            self.system.save_data()
            self.refresh_student_list()
            self.refresh_course_list()
            self.refresh_enrollment_list()
            self.refresh_teacher_list()
            self.update_comboboxes()
            self.clear_course_form()
            messagebox.showinfo("Success", "✓ Course deleted successfully!")
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
            messagebox.showinfo("Success", "✓ Teacher deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ========== SELECTION HANDLERS ==========

    def on_student_select(self, event):
        selected = self.tree_students.selection()
        if not selected:
            return
        values = self.tree_students.item(selected[0], 'values')
        self.selected_student_id = values[0]
        self.ent_sid.delete(0, 'end')
        self.ent_sid.insert(0, values[0])
        self.ent_sname.delete(0, 'end')
        self.ent_sname.insert(0, values[1])
        self.ent_semail.delete(0, 'end')
        self.ent_semail.insert(0, values[2])

    def on_course_select(self, event):
        selected = self.tree_courses.selection()
        if not selected:
            return
        values = self.tree_courses.item(selected[0], 'values')
        self.selected_course_id = values[0]
        self.ent_cid.delete(0, 'end')
        self.ent_cid.insert(0, values[0])
        self.ent_cname.delete(0, 'end')
        self.ent_cname.insert(0, values[1])
        self.ent_ccredits.delete(0, 'end')
        self.ent_ccredits.insert(0, values[2])

    def on_teacher_select(self, event):
        selected = self.tree_teachers.selection()
        if not selected:
            return
        values = self.tree_teachers.item(selected[0], 'values')
        self.selected_teacher_id = values[0]
        self.ent_tid.delete(0, 'end')
        self.ent_tid.insert(0, values[0])
        self.ent_tname.delete(0, 'end')
        self.ent_tname.insert(0, values[1])
        self.ent_temail.delete(0, 'end')
        self.ent_temail.insert(0, values[2])
        self.ent_tdept.delete(0, 'end')
        self.ent_tdept.insert(0, values[3])

    def on_enrollment_select(self, event):
        selected = self.tree_enrollments.selection()
        if not selected:
            self.selected_enrollment = None
            return
        values = self.tree_enrollments.item(selected[0], 'values')
        sid = values[0].split(' - ')[0]
        cid = values[1].split(' - ')[0]
        uid = values[2].split(' - ')[0]
        self.selected_enrollment = (sid, cid, uid)

    def on_cb_course_selected(self, event=None):
        try:
            current = self.cb_courses.get()
            if current:
                cid = current.split(" - ")[0]
                course = self.system.courses.get(cid)
                if course:
                    units_text = "\n".join([f"{u.get('unit_id')} - {u.get('name')}" for u in course.units])
                    self.lb_units.delete("1.0", "end")
                    self.lb_units.insert("1.0", units_text if units_text else "No units in this course")
        except Exception:
            pass

    def on_assign_course_selected(self, event=None):
        try:
            course_str = self.cb_assign_course.get()
            if not course_str:
                return
            cid = course_str.split(' - ')[0]
            course = self.system.courses.get(cid)
            vals = []
            if course:
                vals = [f"{str(u.get('unit_id'))} - {u.get('name')}" for u in course.units]
            self.cb_assign_unit.configure(values=vals)
        except Exception:
            pass

    # ========== ASSIGNMENT OPERATIONS ==========

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
            messagebox.showinfo("Success", f"✓ Teacher {teacher_id} assigned to course {course_id}")
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
            unit_id = str(unit_str.split(" - ")[0])

            self.system.assign_teacher_to_unit(teacher_id, course_id, unit_id)
            self.system.save_data()
            self.refresh_course_list()
            self.refresh_teacher_list()
            messagebox.showinfo("Success", f"✓ Teacher {teacher_id} assigned to unit {unit_id} in {course_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ========== ENROLLMENT OPERATIONS ==========

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
            messagebox.showinfo("Success", f"✓ {student_str} enrolled in {course_str}")
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
            
            # Get selected units from textbox
            units_text = self.lb_units.get("1.0", "end-1c")
            selected_units = []
            for line in units_text.split('\n'):
                if line.strip():
                    uid = line.split(" - ")[0]
                    selected_units.append(uid)
            
            if not selected_units:
                messagebox.showwarning("Warning", "Select at least one unit to enroll")
                return
                
            for uid in selected_units:
                self.system.enroll_student_unit(sid, cid, uid)
            self.system.save_data()
            self.refresh_enrollment_list()
            messagebox.showinfo("Success", f"✓ Enrolled in {len(selected_units)} unit(s)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def assign_grade(self):
        try:
            if not self.selected_enrollment:
                messagebox.showwarning("Warning", "Select an enrollment row to assign grade")
                return
            sid, cid, uid = self.selected_enrollment
            grade = float(self.ent_grade.get())
            if grade < 0 or grade > 100:
                messagebox.showerror("Error", "Grade must be between 0 and 100")
                return
            self.system.assign_unit_grade(sid, cid, uid, grade)
            self.system.save_data()
            self.refresh_enrollment_list()
            messagebox.showinfo("Success", "✓ Grade assigned successfully!")
            self.ent_grade.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Grade must be a number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def assign_grade_to_selected_unit(self):
        try:
            if not self.selected_enrollment:
                messagebox.showwarning("Warning", "Select an enrollment row to assign grade to")
                return
            sid, cid, uid = self.selected_enrollment
            grade = float(self.ent_grade.get())
            self.system.assign_unit_grade(sid, cid, uid, grade)
            self.system.save_data()
            self.refresh_enrollment_list()
            messagebox.showinfo("Success", "✓ Grade assigned successfully!")
            self.ent_grade.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Grade must be a number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_enrollment(self):
        if not self.selected_enrollment:
            messagebox.showwarning("Warning", "Select an enrollment to remove")
            return
        if not messagebox.askyesno("Confirm", "Remove selected enrollment?"):
            return
        student_id, course_id, unit_id = self.selected_enrollment
        try:
            self.system.remove_unit_enrollment(student_id, course_id, unit_id)
            self.system.save_data()
            self.refresh_enrollment_list()
            self.refresh_student_list()
            self.selected_enrollment = None
            messagebox.showinfo("Success", "✓ Enrollment removed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ========== REFRESH & UPDATE OPERATIONS ==========

    def refresh_student_list(self, search_query=""):
        for i in self.tree_students.get_children():
            self.tree_students.delete(i)
        query = search_query.lower()
        for s in self.system.students.values():
            if (query in s.person_id.lower() or query in s.name.lower() or query in s.email.lower()):
                self.tree_students.insert("", "end", values=(s.person_id, s.name, s.email))

    def refresh_course_list(self, search_query=""):
        for i in self.tree_courses.get_children():
            self.tree_courses.delete(i)
        query = search_query.lower()
        for c in self.system.courses.values():
            teacher_name = ""
            if c.teacher_id and c.teacher_id in self.system.teachers:
                teacher_name = self.system.teachers[c.teacher_id].name
            if (query in c.course_id.lower() or query in c.name.lower() or query in teacher_name.lower()):
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
            if (query in t.person_id.lower() or query in t.name.lower() or query in t.email.lower() or query in t.department.lower() or query in courses_str.lower()):
                self.tree_teachers.insert("", "end", values=(t.person_id, t.name, t.email, t.department, courses_str))

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
                        unit_name = unit_id
                        for u in course.units:
                            if u.get('unit_id') == unit_id:
                                unit_name = u.get('name')
                                break
                        unit_label = f"{unit_id} - {unit_name}"
                        self.tree_enrollments.insert("", "end", values=(student_label, course_label, unit_label, grade if grade is not None else "N/A"))

    def update_comboboxes(self):
        s_list = [f"{s.name}" for s in self.system.students.values()]
        c_list = [f"{c.course_id} - {c.name}" for c in self.system.courses.values()]
        t_list = [f"{t.person_id} - {t.name}" for t in self.system.teachers.values()]
        
        self.cb_students.configure(values=s_list)
        self.cb_courses.configure(values=c_list)
        self.cb_report_student.configure(values=s_list)
        self.cb_assign_teacher.configure(values=t_list)
        self.cb_assign_course.configure(values=c_list)
        self.cb_analysis_student.configure(values=s_list)

    # ========== HELPER FUNCTIONS ==========

    def _get_student_id_by_name(self, name):
        """Helper to get student ID by name."""
        for s in self.system.students.values():
            if s.name == name:
                return s.person_id
        raise ValueError(f"Student '{name}' not found")

    def clear_student_form(self):
        self.ent_sid.delete(0, 'end')
        self.ent_sname.delete(0, 'end')
        self.ent_semail.delete(0, 'end')
        self.selected_student_id = None

    def clear_course_form(self):
        self.ent_cid.delete(0, 'end')
        self.ent_cname.delete(0, 'end')
        self.ent_ccredits.delete(0, 'end')
        self.selected_course_id = None

    def clear_teacher_form(self):
        self.ent_tid.delete(0, 'end')
        self.ent_tname.delete(0, 'end')
        self.ent_temail.delete(0, 'end')
        self.ent_tdept.delete(0, 'end')
        self.selected_teacher_id = None

    def open_manage_units_dialog(self):
        messagebox.showinfo("Info", "Unit management dialog - select a course and add units from the main form")

    def generate_report(self):
        try:
            student_name = self.cb_report_student.get()
            if not student_name:
                messagebox.showwarning("Warning", "Please select a student")
                return
            sid = self._get_student_id_by_name(student_name)
            report = self.system.generate_student_report(sid)
            self.txt_report.delete("1.0", "end")
            self.txt_report.insert("1.0", report)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_report_pdf(self):
        try:
            student_name = self.cb_report_student.get()
            if not student_name:
                messagebox.showwarning("Warning", "Please select a student")
                return
            sid = self._get_student_id_by_name(student_name)
            report_content = self.system.generate_student_report(sid)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "STUDENT REPORT", ln=True, align="C")
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 5, report_content)
            pdf.output(f"report_{sid}.pdf")
            messagebox.showinfo("Success", f"✓ Report exported to report_{sid}.pdf")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_summary(self):
        try:
            self.system.export_courses_summary("courses_summary_report.csv")
            messagebox.showinfo("Success", "✓ Course summary exported successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export summary: {str(e)}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = EduManageGUI(root)
    root.mainloop()
