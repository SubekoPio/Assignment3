import customtkinter as ctk
import tkinter as tk
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
        """Apply consistent TTK styles for treeviews/scrollbars matching the current theme."""
        tv_bg  = "#1e2330" if self.dark_mode else "#ffffff"
        tv_fg  = "#e8eaf6" if self.dark_mode else "#1a1a2e"
        hdr_bg = "#0f3460" if self.dark_mode else "#2C3E50"
        alt_bg = "#232b3e" if self.dark_mode else "#eef2f7"
        sel_bg = "#3498DB"

        style = ttk.Style()
        style.theme_use("clam")

        # ── Treeview body ──────────────────────────────────────────────────────────
        style.configure("Treeview",
                        background=tv_bg,
                        foreground=tv_fg,
                        fieldbackground=tv_bg,
                        rowheight=34,
                        font=("Segoe UI", 12),
                        borderwidth=0,
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", sel_bg)],
                  foreground=[("selected", "#ffffff")])

        # ── Treeview headings ──────────────────────────────────────────────────────
        style.configure("Treeview.Heading",
                        background=hdr_bg,
                        foreground="#ffffff",
                        font=("Segoe UI", 12, "bold"),
                        relief="flat",
                        padding=(10, 7))
        style.map("Treeview.Heading",
                  background=[("active", sel_bg)],
                  relief=[("active", "flat")])

        # ── Scrollbars ─────────────────────────────────────────────────────────────
        sb_bg = hdr_bg
        sb_tr = tv_bg
        for orientation in ("Vertical", "Horizontal"):
            style.configure(f"{orientation}.TScrollbar",
                            background=sb_bg, troughcolor=sb_tr,
                            bordercolor=sb_tr, arrowcolor="#aaaaaa",
                            relief="flat")

    def validate_email(self, email):
        """Validate email format using regex pattern."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def toggle_theme(self):
        """Toggle between light and dark modes, rebuilding the tab area for correct colors."""
        self.dark_mode = not self.dark_mode
        ctk.set_appearance_mode("dark" if self.dark_mode else "light")
        self.current_colors = self.dark_colors if self.dark_mode else self.light_colors
        self.theme_toggle_btn.configure(text="☀️ Light" if self.dark_mode else "🌙 Dark")
        # Sync plain-tk container backgrounds
        self._main_container.configure(fg_color=self.current_colors["bg"])
        self._header.configure(fg_color=self.current_colors["primary"])
        # Reset selections (widgets are about to be recreated)
        self.selected_student_id = None
        self.selected_course_id = None
        self.selected_teacher_id = None
        self.selected_enrollment = None
        # Reapply TTK styles for the new palette, then rebuild all tab contents
        self.setup_styles()
        self.notebook.destroy()
        self._build_tabs_area()

    def create_widgets(self):
        # Main container — stored so _build_tabs_area and toggle_theme can reference it
        self._main_container = ctk.CTkFrame(self.root, fg_color=self.current_colors["bg"])
        self._main_container.pack(fill="both", expand=True)

        # Header — slim bar, fixed height
        self._header = ctk.CTkFrame(self._main_container,
                                    fg_color=self.current_colors["primary"], height=46)
        self._header.pack(fill="x", pady=(0, 4), padx=10)
        self._header.pack_propagate(False)
        self._header.configure(corner_radius=8)

        ctk.CTkLabel(
            self._header,
            text="\t\t\t\t🎓 EduManage — Advanced Education Management System",
            font=("Segoe UI", 17, "bold"),
            text_color="white"
        ).pack(side="left", padx=16)

        self.theme_toggle_btn = ctk.CTkButton(
            self._header,
            text="☀️ Light",
            command=self.toggle_theme,
            width=100, height=28,
            fg_color="#FF9800", hover_color="#F57C00",
            text_color="white", corner_radius=6,
            font=("Segoe UI", 12, "bold")
        )
        self.theme_toggle_btn.pack(side="right", padx=12)

        self._build_tabs_area()

    def _build_tabs_area(self):
        """Create (or recreate on theme toggle) the notebook and all tab contents."""
        self.notebook = ctk.CTkTabview(
            self._main_container,
            segmented_button_fg_color=self.current_colors["secondary"],
            segmented_button_selected_color="#3498DB",
            segmented_button_selected_hover_color="#2980B9",
            text_color="white",
            text_color_disabled="#aaaaaa",
        )
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        self.tab_students = self.notebook.add(" 👥 Students ")
        self.tab_courses  = self.notebook.add(" 📚 Courses ")
        self.tab_teachers = self.notebook.add(" 👨\u200d🏫 Teachers ")
        self.tab_enroll   = self.notebook.add(" 📝 Enrollment & Grades ")
        self.tab_reports  = self.notebook.add(" 📊 Reports ")
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
        frame.pack(fill="x", padx=10, pady=(6, 4))

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        ).pack(pady=(8, 0))

        inner_frame = ctk.CTkFrame(frame, fg_color=self.current_colors["bg"], corner_radius=8)
        inner_frame.pack(fill="x", padx=10, pady=(6, 10))

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

        # Table Frame — plain tk.Frame so Treeview geometry propagates correctly
        table_frame = tk.Frame(self.tab_students, bg=self.current_colors["bg"])
        table_frame.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        stu_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        self.tree_students = ttk.Treeview(table_frame,
                                          columns=("ID", "Name", "Email"),
                                          show="headings", selectmode="browse",
                                          yscrollcommand=stu_scroll.set)
        stu_scroll.config(command=self.tree_students.yview)
        self.tree_students.heading("ID",    text="Student ID")
        self.tree_students.heading("Name",  text="Full Name")
        self.tree_students.heading("Email", text="Email Address")
        self.tree_students.column("ID",    width=110, minwidth=80)
        self.tree_students.column("Name",  width=220, minwidth=140)
        self.tree_students.column("Email", width=320, minwidth=180)
        self.tree_students.pack(side="left", fill="both", expand=True)
        stu_scroll.pack(side="right", fill="y")
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

        # Vertical PanedWindow — top: courses list, bottom: units for selected course
        courses_pane = tk.PanedWindow(self.tab_courses, orient=tk.VERTICAL,
                                       bg=self.current_colors["bg"], sashrelief="raised",
                                       sashwidth=6, relief="flat", bd=0)
        courses_pane.pack(fill="both", expand=True, padx=10, pady=5)

        # ── Top pane: courses treeview ──
        courses_top = tk.Frame(courses_pane, bg=self.current_colors["bg"])
        courses_yscroll = ttk.Scrollbar(courses_top, orient="vertical")
        self.tree_courses = ttk.Treeview(courses_top,
                                          columns=("ID", "Name", "Credits", "Teacher"),
                                          show="headings", selectmode="browse",
                                          yscrollcommand=courses_yscroll.set)
        courses_yscroll.config(command=self.tree_courses.yview)
        self.tree_courses.heading("ID", text="Course ID")
        self.tree_courses.heading("Name", text="Name")
        self.tree_courses.heading("Credits", text="Credits")
        self.tree_courses.heading("Teacher", text="Teacher")
        self.tree_courses.column("ID", width=100)
        self.tree_courses.column("Name", width=220)
        self.tree_courses.column("Credits", width=80)
        self.tree_courses.column("Teacher", width=180)
        self.tree_courses.pack(side="left", fill="both", expand=True)
        courses_yscroll.pack(side="right", fill="y")
        self.tree_courses.bind("<<TreeviewSelect>>", self.on_course_select)
        courses_pane.add(courses_top, minsize=120)
        self.refresh_course_list()

        # ── Bottom pane: units for selected course ──
        units_outer = tk.Frame(courses_pane, bg=self.current_colors["bg"])

        # Title row
        title_row = tk.Frame(units_outer, bg=self.current_colors["bg"])
        title_row.pack(fill="x", padx=6, pady=(6, 2))
        self._lbl_units_title = ctk.CTkLabel(title_row,
                                              text="📋 Course Units  —  select a course above",
                                              font=("Segoe UI", 14, "bold"),
                                              text_color=self.current_colors["text"])
        self._lbl_units_title.pack(side="left")
        ctk.CTkButton(title_row, text="⚙️ Manage Course-Units",
                      command=self.open_manage_units_dialog,
                      fg_color="#8E44AD", hover_color="#7D3C98",
                      corner_radius=8, width=130, height=28).pack(side="right", padx=4)

        # Units treeview
        units_tree_frame = tk.Frame(units_outer, bg=self.current_colors["bg"])
        units_tree_frame.pack(fill="both", expand=True, padx=6, pady=(0, 4))
        units_yscroll = ttk.Scrollbar(units_tree_frame, orient="vertical")
        self.tree_course_units = ttk.Treeview(units_tree_frame,
                                               columns=("UnitID", "Name", "Credits", "Teacher"),
                                               show="headings", selectmode="browse",
                                               yscrollcommand=units_yscroll.set)
        units_yscroll.config(command=self.tree_course_units.yview)
        self.tree_course_units.heading("UnitID", text="Unit ID")
        self.tree_course_units.heading("Name", text="Unit Name")
        self.tree_course_units.heading("Credits", text="Credits")
        self.tree_course_units.heading("Teacher", text="Assigned Teacher")
        self.tree_course_units.column("UnitID", width=90)
        self.tree_course_units.column("Name", width=220)
        self.tree_course_units.column("Credits", width=70)
        self.tree_course_units.column("Teacher", width=160)
        self.tree_course_units.pack(side="left", fill="both", expand=True)
        units_yscroll.pack(side="right", fill="y")
        self.tree_course_units.bind("<<TreeviewSelect>>", self.on_unit_select)

        # Inline unit form (Add / Update / Delete)
        unit_form = tk.Frame(units_outer, bg=self.current_colors["bg"])
        unit_form.pack(fill="x", padx=6, pady=(0, 6))

        ctk.CTkLabel(unit_form, text="Unit ID:",
                     text_color=self.current_colors["text"]).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.ent_unit_id = ctk.CTkEntry(unit_form, placeholder_text="ID", corner_radius=8, width=90)
        self.ent_unit_id.grid(row=0, column=1, padx=4, pady=4)

        ctk.CTkLabel(unit_form, text="Unit Name:",
                     text_color=self.current_colors["text"]).grid(row=0, column=2, padx=4, pady=4, sticky="w")
        self.ent_unit_name = ctk.CTkEntry(unit_form, placeholder_text="Name", corner_radius=8, width=200)
        self.ent_unit_name.grid(row=0, column=3, padx=4, pady=4)

        ctk.CTkLabel(unit_form, text="Credits:",
                     text_color=self.current_colors["text"]).grid(row=0, column=4, padx=4, pady=4, sticky="w")
        self.ent_unit_credits = ctk.CTkEntry(unit_form, placeholder_text="Cred", corner_radius=8, width=65)
        self.ent_unit_credits.grid(row=0, column=5, padx=4, pady=4)

        ctk.CTkButton(unit_form, text="➕ Add",
                      command=self.add_unit_to_course,
                      corner_radius=8, width=80).grid(row=0, column=6, padx=4, pady=4)
        ctk.CTkButton(unit_form, text="✏️ Update",
                      command=self.update_unit_in_course,
                      fg_color="#F39C12", hover_color="#E67E22",
                      corner_radius=8, width=90).grid(row=0, column=7, padx=4, pady=4)
        ctk.CTkButton(unit_form, text="🗑️ Delete",
                      command=self.delete_unit_from_course,
                      fg_color="#E74C3C", hover_color="#C0392B",
                      corner_radius=8, width=90).grid(row=0, column=8, padx=4, pady=4)
        ctk.CTkButton(unit_form, text="🔄 Clear",
                      command=self._clear_unit_form,
                      fg_color="#7F8C8D", hover_color="#5D6D7B",
                      corner_radius=8, width=80).grid(row=0, column=9, padx=4, pady=4)

        courses_pane.add(units_outer, minsize=120)

    def setup_teacher_tab(self):
        # Input Frame
        input_frame = self.create_input_frame(self.tab_teachers, "Teacher Details")

        col1 = ctk.CTkFrame(input_frame, fg_color=self.current_colors["bg"])
        col1.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(col1, text="ID:", text_color=self.current_colors["text"]).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_tid = ctk.CTkEntry(col1, placeholder_text="Teacher ID", corner_radius=8)
        self.ent_tid.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(col1, text="Name:", text_color=self.current_colors["text"]).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_tname = ctk.CTkEntry(col1, placeholder_text="Full name", corner_radius=8)
        self.ent_tname.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(col1, text="Email:", text_color=self.current_colors["text"]).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.ent_temail = ctk.CTkEntry(col1, placeholder_text="teacher@example.com", corner_radius=8)
        self.ent_temail.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(col1, text="Department:", text_color=self.current_colors["text"]).grid(row=0, column=6, padx=5, pady=5, sticky="w")
        self.ent_tdept = ctk.CTkEntry(col1, placeholder_text="Department", corner_radius=8)
        self.ent_tdept.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

        col1.columnconfigure((1, 3, 5, 7), weight=1)

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
        self.cb_assign_course = ctk.CTkComboBox(assign_col, corner_radius=8, state="readonly",
                                                  command=self.on_assign_course_selected)
        self.cb_assign_course.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

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

        # Table Frame — use plain tk.Frame so pack geometry propagates correctly
        table_frame = tk.Frame(self.tab_teachers, bg=self.current_colors["bg"])
        table_frame.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        teachers_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        self.tree_teachers = ttk.Treeview(table_frame,
                                           columns=("ID", "Name", "Email", "Department", "Courses"),
                                           show="headings", selectmode="browse",
                                           yscrollcommand=teachers_scroll.set)
        teachers_scroll.config(command=self.tree_teachers.yview)
        self.tree_teachers.heading("ID", text="Teacher ID")
        self.tree_teachers.heading("Name", text="Name")
        self.tree_teachers.heading("Email", text="Email")
        self.tree_teachers.heading("Department", text="Department")
        self.tree_teachers.heading("Courses", text="Courses / Units Taught")
        self.tree_teachers.column("ID", width=90)
        self.tree_teachers.column("Name", width=160)
        self.tree_teachers.column("Email", width=200)
        self.tree_teachers.column("Department", width=130)
        self.tree_teachers.column("Courses", width=180)
        self.tree_teachers.pack(side="left", fill="both", expand=True)
        teachers_scroll.pack(side="right", fill="y")
        self.tree_teachers.bind("<<TreeviewSelect>>", self.on_teacher_select)
        self.refresh_teacher_list()

    def setup_enroll_tab(self):
        # ── PanedWindow: top = controls + units listbox, bottom = enrollments table ──
        enroll_pane = tk.PanedWindow(self.tab_enroll, orient=tk.VERTICAL,
                                     bg=self.current_colors["bg"], sashrelief="raised",
                                     sashwidth=6, relief="flat", bd=0)
        enroll_pane.pack(fill="both", expand=True, padx=10, pady=8)

        # ── Top pane: enroll controls ──────────────────────────────────────────────
        top_outer = tk.Frame(enroll_pane, bg=self.current_colors["bg"])

        # Enroll row
        ctrl_bg = self.current_colors["secondary"]
        ctrl_card = ctk.CTkFrame(top_outer, fg_color=ctrl_bg, corner_radius=10)
        ctrl_card.pack(fill="x", padx=0, pady=(0, 6))

        ctk.CTkLabel(ctrl_card, text="Enroll Student & Assign Grade",
                     font=("Segoe UI", 14, "bold"), text_color="white").pack(pady=(8, 0))

        ctrl_inner = ctk.CTkFrame(ctrl_card, fg_color=self.current_colors["bg"], corner_radius=8)
        ctrl_inner.pack(fill="x", padx=10, pady=8)

        row1 = ctk.CTkFrame(ctrl_inner, fg_color=self.current_colors["bg"])
        row1.pack(fill="x", padx=6, pady=4)

        ctk.CTkLabel(row1, text="Student:", text_color=self.current_colors["text"]).grid(row=0, column=0, padx=5, pady=6, sticky="w")
        self.cb_students = ctk.CTkComboBox(row1, corner_radius=8, state="readonly")
        self.cb_students.grid(row=0, column=1, padx=5, pady=6, sticky="ew")

        ctk.CTkLabel(row1, text="Course:", text_color=self.current_colors["text"]).grid(row=0, column=2, padx=5, pady=6, sticky="w")
        self.cb_courses = ctk.CTkComboBox(row1, corner_radius=8, state="readonly",
                                          command=self.on_cb_course_selected)
        self.cb_courses.grid(row=0, column=3, padx=5, pady=6, sticky="ew")

        ctk.CTkButton(row1, text="📝 Enroll Course", command=self.enroll_student,
                      corner_radius=8, width=130).grid(row=0, column=4, padx=8, pady=6)

        row1.columnconfigure((1, 3), weight=1)

        row2 = ctk.CTkFrame(ctrl_inner, fg_color=self.current_colors["bg"])
        row2.pack(fill="x", padx=6, pady=(0, 6))

        ctk.CTkLabel(row2, text="Grade (0-100):", text_color=self.current_colors["text"]).pack(side="left", padx=5)
        self.ent_grade = ctk.CTkEntry(row2, placeholder_text="Enter grade", width=100, corner_radius=8)
        self.ent_grade.pack(side="left", padx=5)
        ctk.CTkButton(row2, text="✔️ Assign Grade", command=self.assign_grade,
                      fg_color="#27AE60", hover_color="#1E8449", corner_radius=8, width=130).pack(side="left", padx=5)
        ctk.CTkButton(row2, text="🗑️ Remove Enrollment", command=self.delete_enrollment,
                      fg_color="#E74C3C", hover_color="#C0392B", corner_radius=8, width=150).pack(side="left", padx=5)

        # Units listbox row
        units_card = ctk.CTkFrame(top_outer, fg_color=ctrl_bg, corner_radius=10)
        units_card.pack(fill="x", padx=0, pady=(0, 4))

        ctk.CTkLabel(units_card, text="Course Units  —  select units then click Enroll Units",
                     font=("Segoe UI", 14, "bold"), text_color="white").pack(pady=(8, 0))

        units_inner = tk.Frame(units_card, bg=self.current_colors["bg"],
                               highlightthickness=1,
                               highlightbackground=self.current_colors["secondary"])
        units_inner.pack(fill="x", padx=10, pady=8, ipady=2)

        self.lb_units = tk.Listbox(
            units_inner,
            selectmode=tk.MULTIPLE,
            bg="#2b2b2b" if self.dark_mode else "#f5f5f5",
            fg="white" if self.dark_mode else "#1a1a1a",
            selectbackground="#3498DB",
            activestyle="none",
            highlightthickness=0,
            relief="flat",
            exportselection=False,
            height=5,
            font=("Segoe UI", 10)
        )
        self.lb_units.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)

        lb_scroll = tk.Scrollbar(units_inner, orient="vertical", command=self.lb_units.yview)
        lb_scroll.pack(side="right", fill="y", padx=(0, 4), pady=4)
        self.lb_units.configure(yscrollcommand=lb_scroll.set)

        units_btns = tk.Frame(units_card, bg=ctrl_bg)
        units_btns.pack(fill="x", padx=10, pady=(0, 8))
        ctk.CTkButton(units_btns, text="📝 Enroll Selected Units",
                      command=self.enroll_selected_units,
                      fg_color="#2980B9", hover_color="#1F618D", corner_radius=8, width=180).pack(side="left", padx=4)
        ctk.CTkButton(units_btns, text="✔️ Grade Selected Unit",
                      command=self.assign_grade_to_selected_unit,
                      fg_color="#27AE60", hover_color="#1E8449", corner_radius=8, width=180).pack(side="left", padx=4)

        enroll_pane.add(top_outer, minsize=160)

        # ── Bottom pane: enrollments table ─────────────────────────────────────────
        bottom_outer = tk.Frame(enroll_pane, bg=self.current_colors["bg"])

        tbl_title = tk.Frame(bottom_outer, bg=self.current_colors["secondary"])
        tbl_title.pack(fill="x")
        ctk.CTkLabel(tbl_title, text="📋 Current Enrollments",
                     font=("Segoe UI", 14, "bold"), text_color="white").pack(pady=6, padx=10, anchor="w")

        tbl_frame = tk.Frame(bottom_outer, bg=self.current_colors["bg"])
        tbl_frame.pack(fill="both", expand=True, padx=6, pady=6)

        enroll_xscroll = ttk.Scrollbar(tbl_frame, orient="horizontal")
        enroll_yscroll = ttk.Scrollbar(tbl_frame, orient="vertical")
        self.tree_enrollments = ttk.Treeview(
            tbl_frame,
            columns=("Student", "StudentID", "Course", "Unit", "UnitID", "Grade"),
            show="headings",
            selectmode="browse",
            xscrollcommand=enroll_xscroll.set,
            yscrollcommand=enroll_yscroll.set
        )
        enroll_xscroll.config(command=self.tree_enrollments.xview)
        enroll_yscroll.config(command=self.tree_enrollments.yview)

        self.tree_enrollments.heading("Student",   text="Student Name")
        self.tree_enrollments.heading("StudentID", text="Student ID")
        self.tree_enrollments.heading("Course",    text="Course")
        self.tree_enrollments.heading("Unit",      text="Unit Name")
        self.tree_enrollments.heading("UnitID",    text="Unit ID")
        self.tree_enrollments.heading("Grade",     text="Grade")

        self.tree_enrollments.column("Student",   width=160, minwidth=120)
        self.tree_enrollments.column("StudentID", width=90,  minwidth=70)
        self.tree_enrollments.column("Course",    width=180, minwidth=120)
        self.tree_enrollments.column("Unit",      width=180, minwidth=120)
        self.tree_enrollments.column("UnitID",    width=80,  minwidth=60)
        self.tree_enrollments.column("Grade",     width=80,  minwidth=60)

        self.tree_enrollments.grid(row=0, column=0, sticky="nsew")
        enroll_yscroll.grid(row=0, column=1, sticky="ns")
        enroll_xscroll.grid(row=1, column=0, sticky="ew")
        tbl_frame.rowconfigure(0, weight=1)
        tbl_frame.columnconfigure(0, weight=1)

        self.tree_enrollments.bind("<<TreeviewSelect>>", self.on_enrollment_select)
        enroll_pane.add(bottom_outer, minsize=140)
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
            ax1.set_title("Students Enrolled per Course", fontsize=16, fontweight='bold', color=self.current_colors["text"])
            ax1.set_xlabel("Course", fontsize=14, color=self.current_colors["text"])
            ax1.set_ylabel("Count", fontsize=14, color=self.current_colors["text"])
            ax1.tick_params(axis='x', labelsize=14, rotation=45, colors=self.current_colors["text"])
            ax1.tick_params(axis='y', labelsize=14, colors=self.current_colors["text"])
            ax1.set_facecolor("#2C3E50" if self.dark_mode else "white")

        # Chart 2
        if analytics["grades_distribution"]:
            ax2 = fig.add_subplot(2, 2, 2)
            order = ['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']
            dist = [analytics["grades_distribution"].get(k, 0) for k in order]
            bars = ax2.bar(order, dist, color="#2ECC71", edgecolor="#27AE60", linewidth=1.5)
            ax2.set_title("Grade Distribution", fontsize=16, fontweight='bold', color=self.current_colors["text"])
            ax2.set_xlabel("Letter Grade", fontsize=14, color=self.current_colors["text"])
            ax2.set_ylabel("Count", fontsize=14, color=self.current_colors["text"])
            ax2.tick_params(axis='x', labelsize=14, rotation=45, colors=self.current_colors["text"])
            ax2.tick_params(axis='y', labelsize=14, colors=self.current_colors["text"])
            ax2.set_facecolor("#2C3E50" if self.dark_mode else "white")

        # Chart 3
        if analytics["teacher_workload"]:
            ax3 = fig.add_subplot(2, 2, 3)
            teachers = list(analytics["teacher_workload"].keys())
            workload = list(analytics["teacher_workload"].values())
            ax3.barh(teachers, workload, color="#E74C3C", edgecolor="#C0392B", linewidth=1.5)
            ax3.set_title("Teacher Workload", fontsize=16, fontweight='bold', color=self.current_colors["text"])
            ax3.set_xlabel("Number of Units", fontsize=14, color=self.current_colors["text"])
            ax3.tick_params(axis='x', labelsize=14, colors=self.current_colors["text"])
            ax3.tick_params(axis='y', labelsize=14, colors=self.current_colors["text"])
            ax3.set_facecolor("#2C3E50" if self.dark_mode else "white")

        # Chart 4
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.axis('off')
        stats_text = f"SYSTEM STATISTICS\n\n✓ Total Students: {analytics['total_students']}\n✓ Total Courses: {analytics['total_courses']}\n✓ Total Teachers: {analytics['total_teachers']}\n✓ Avg Grade: {analytics['avg_grade']:.1f}%"
        ax4.text(0.5, 0.5, stats_text, fontsize=14, ha='center', va='center',
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
            self.refresh_course_units_panel()
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
        self._clear_unit_form()
        self.refresh_course_units_panel()

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
        # columns: Student, StudentID, Course, Unit, UnitID, Grade
        sid = values[1]                          # StudentID
        cid = values[2].split(' - ')[0]          # CourseID from "CID - Name"
        uid = values[4]                          # UnitID
        self.selected_enrollment = (sid, cid, uid)

    def on_cb_course_selected(self, event=None):
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

            selected_indices = self.lb_units.curselection()
            selected_units = [self.lb_units.get(i).split(" - ")[0] for i in selected_indices]
            
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
                    course_label = f"{course.course_id} - {course.name}"
                    for unit_id, grade in data.get('units', {}).items():
                        unit_name = unit_id
                        for u in course.units:
                            if u.get('unit_id') == unit_id:
                                unit_name = u.get('name')
                                break
                        self.tree_enrollments.insert("", "end", values=(
                            student.name,
                            student.person_id,
                            course_label,
                            unit_name,
                            unit_id,
                            grade if grade is not None else "N/A"
                        ))

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

        try:
            self.refresh_course_units_panel()
        except Exception:
            pass

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
        cid = self.selected_course_id or self.ent_cid.get().strip()
        if not cid:
            messagebox.showwarning("Warning", "Select a course first to manage units")
            return
        course = self.system.courses.get(cid)
        if not course:
            messagebox.showerror("Error", f"Course {cid} not found")
            return

        # ── palette shorthand ──────────────────────────────────────────────────
        BG      = self.current_colors["bg"]
        PRI     = self.current_colors["primary"]
        SEC     = self.current_colors["secondary"]
        TXT     = self.current_colors["text"]
        TV_BG   = "#1e2330" if self.dark_mode else "#ffffff"
        TV_FG   = "#e8eaf6" if self.dark_mode else "#1a1a2e"
        HDR_BG  = "#0f3460" if self.dark_mode else "#2C3E50"
        ENT_BG  = "#232b3e" if self.dark_mode else "#f5f7fa"
        ENT_FG  = "#e8eaf6" if self.dark_mode else "#1a1a2e"
        FONT    = ("Segoe UI", 14)
        FONT_B  = ("Segoe UI", 14, "bold")
        FONT_LG = ("Segoe UI", 14, "bold")

        dlg = tk.Toplevel(self.root)
        dlg.title(f"Manage Units Under — {cid}: {course.name}")
        dlg.geometry("950x660")
        dlg.configure(bg=BG)
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.resizable(True, True)

        # ── title bar ──────────────────────────────────────────────────
        title_bar = tk.Frame(dlg, bg=PRI, height=46)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar,
                 text=f"\U0001f4cb  Units for  {cid} — {course.name}",
                 bg=PRI, fg="white", font=FONT_LG).pack(side="left", padx=14, pady=0)

        # ── treeview ──────────────────────────────────────────────────
        tv_frame = tk.Frame(dlg, bg=BG)
        tv_frame.pack(fill="both", expand=True, padx=12, pady=(10, 4))

        tv_scroll = ttk.Scrollbar(tv_frame, orient="vertical")
        tree = ttk.Treeview(tv_frame,
                            columns=("UnitID", "Name", "Credits"),
                            show="headings", selectmode="browse",
                            yscrollcommand=tv_scroll.set)
        tv_scroll.config(command=tree.yview)
        tree.heading("UnitID",   text="Unit ID")
        tree.heading("Name",     text="Unit Name")
        tree.heading("Credits",  text="Credits")
        tree.column("UnitID",   width=120, minwidth=80)
        tree.column("Name",     width=420, minwidth=200)
        tree.column("Credits",  width=110, minwidth=70)
        tree.pack(side="left", fill="both", expand=True)
        tv_scroll.pack(side="right", fill="y")

        # ── form ─────────────────────────────────────────────────────
        form_outer = tk.Frame(dlg, bg=SEC)
        form_outer.pack(fill="x", padx=12, pady=(4, 0))
        tk.Label(form_outer, text="Unit Details",
                 bg=SEC, fg="white", font=FONT_B).pack(anchor="w", padx=10, pady=(6, 2))

        form = tk.Frame(form_outer, bg=BG, pady=6)
        form.pack(fill="x", padx=10, pady=(0, 8))

        def _lbl(parent, text):
            return tk.Label(parent, text=text, bg=BG, fg=TXT, font=FONT)

        def _ent(parent, width=18):
            e = tk.Entry(parent, font=FONT, width=width,
                         bg=ENT_BG, fg=ENT_FG,
                         insertbackground=ENT_FG,
                         relief="flat", bd=4,
                         highlightthickness=1,
                         highlightbackground=SEC,
                         highlightcolor="#3498DB")
            return e

        _lbl(form, "Unit ID:").grid(row=0, column=0, padx=(8, 4), pady=6, sticky="w")
        ent_uid = _ent(form, 14)
        ent_uid.grid(row=0, column=1, padx=(0, 12), pady=6)

        _lbl(form, "Unit Name:").grid(row=0, column=2, padx=(4, 4), pady=6, sticky="w")
        ent_uname = _ent(form, 34)
        ent_uname.grid(row=0, column=3, padx=(0, 12), pady=6)

        _lbl(form, "Credits:").grid(row=0, column=4, padx=(4, 4), pady=6, sticky="w")
        ent_ucredits = _ent(form, 8)
        ent_ucredits.grid(row=0, column=5, padx=(0, 8), pady=6)

        # ── inner helpers ──────────────────────────────────────────────
        def refresh_tree():
            for row_id in tree.get_children():
                tree.delete(row_id)
            for unit in course.units:
                tree.insert("", "end",
                            values=(unit.get("unit_id"), unit.get("name"), unit.get("credits")))

        def clear_form(unlock_id=True):
            if unlock_id:
                ent_uid.config(state="normal")
            ent_uid.delete(0, tk.END)
            ent_uname.delete(0, tk.END)
            ent_ucredits.delete(0, tk.END)

        def on_select(event=None):
            selected = tree.selection()
            if not selected:
                return
            vals = tree.item(selected[0], "values")
            clear_form(unlock_id=True)
            ent_uid.insert(0, vals[0])
            ent_uid.config(state="readonly")
            ent_uname.insert(0, vals[1])
            ent_ucredits.insert(0, vals[2])

        def add_unit():
            uid  = ent_uid.get().strip()
            name = ent_uname.get().strip()
            if not uid or not name:
                messagebox.showwarning("Warning", "Unit ID and name are required", parent=dlg)
                return
            try:
                credits = float(ent_ucredits.get())
            except Exception:
                messagebox.showerror("Error", "Credits must be a number", parent=dlg)
                return
            try:
                self.system.add_course_unit(cid, uid, name, credits)
                self.system.save_data()
                refresh_tree()
                self.refresh_course_list()
                self.refresh_course_units_panel()
                self.refresh_enrollment_list()
                self.update_comboboxes()
                self.on_cb_course_selected()
                clear_form(unlock_id=True)
                messagebox.showinfo("Success", f"\u2713 Unit {uid} added", parent=dlg)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dlg)

        def update_unit():
            uid  = ent_uid.get().strip()
            name = ent_uname.get().strip()
            if not uid or not name:
                messagebox.showwarning("Warning", "Select a unit row first", parent=dlg)
                return
            try:
                credits = float(ent_ucredits.get())
            except Exception:
                messagebox.showerror("Error", "Credits must be a number", parent=dlg)
                return
            try:
                self.system.update_course_unit(cid, uid, name=name, credits=credits)
                self.system.save_data()
                refresh_tree()
                self.refresh_course_list()
                self.refresh_course_units_panel()
                self.refresh_enrollment_list()
                self.update_comboboxes()
                self.on_cb_course_selected()
                messagebox.showinfo("Success", f"\u2713 Unit {uid} updated", parent=dlg)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dlg)

        def delete_unit():
            uid = ent_uid.get().strip()
            if not uid:
                messagebox.showwarning("Warning", "Select a unit to delete", parent=dlg)
                return
            if not messagebox.askyesno("Confirm",
                                       f"Delete unit {uid}?\nRelated enrollments will be removed.",
                                       parent=dlg):
                return
            try:
                self.system.delete_course_unit(cid, uid)
                self.system.save_data()
                refresh_tree()
                self.refresh_course_list()
                self.refresh_course_units_panel()
                self.refresh_enrollment_list()
                self.refresh_teacher_list()
                self.update_comboboxes()
                self.on_cb_course_selected()
                clear_form(unlock_id=True)
                messagebox.showinfo("Success", f"\u2713 Unit {uid} deleted", parent=dlg)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dlg)

        # ── action buttons ──────────────────────────────────────────────
        btn_bar = tk.Frame(dlg, bg=BG)
        btn_bar.pack(fill="x", padx=12, pady=8)

        def _btn(parent, text, cmd, fg_color="#3498DB", hover="#2980B9", side="left"):
            b = ctk.CTkButton(parent, text=text, command=cmd,
                              fg_color=fg_color, hover_color=hover,
                              corner_radius=8, height=36, width=120,
                              font=("Segoe UI", 12, "bold"))
            b.pack(side=side, padx=5)
            return b

        _btn(btn_bar, "\u2795 Add",    add_unit,   "#1a6fa8",  "#155a8a")
        _btn(btn_bar, "\u270f\ufe0f Update", update_unit, "#F39C12",  "#E67E22")
        _btn(btn_bar, "\ud83d\uddd1\ufe0f Delete", delete_unit, "#E74C3C",  "#C0392B")
        _btn(btn_bar, "\ud83d\udd04 Clear",  lambda: clear_form(unlock_id=True), "#7F8C8D", "#5D6D7B")
        _btn(btn_bar, "\u2715 Close", dlg.destroy, "#4a5568",  "#374151", side="right")

        tree.bind("<<TreeviewSelect>>", on_select)
        refresh_tree()

    def _format_report_text(self, report):
        lines = []
        lines.append("REPORT CARD")
        lines.append("=" * 110)
        lines.append(f"Name: {report['student_name']}")
        lines.append(f"ID: {report['student_id']}")
        lines.append("")
        lines.append(f"{'Course':<20} {'C.Cred':<7} {'Unit':<18} {'U.Cred':<7} {'Grade':<8} {'Letter':<8} {'Points':<8} {'Teacher':<16}")
        lines.append("-" * 110)

        for course in report['courses']:
            lines.append(f"{course['course_name']} (GPA: {course['course_gpa']:.2f})")
            for unit in course['units']:
                grade = unit.get('grade') if unit.get('grade') is not None else 'N/A'
                letter = unit.get('letter', 'N/A')
                point = f"{unit.get('point'):.1f}" if isinstance(unit.get('point'), (int, float)) else 'N/A'
                teacher = unit.get('teacher', 'Unassigned')
                row = (
                    f"{course['course_name'][:18]:<20} "
                    f"{str(course.get('credits', 0)):<7} "
                    f"{unit.get('unit_name', '')[:16]:<18} "
                    f"{str(unit.get('credits', 'N/A')):<7} "
                    f"{str(grade):<8} {letter:<8} {point:<8} {teacher[:16]:<16}"
                )
                lines.append(row)
            lines.append("")

        lines.append(f"OVERALL CGPA: {report['cgpa']:.2f}")
        return "\n".join(lines)

    def generate_report(self):
        try:
            student_name = self.cb_report_student.get()
            if not student_name:
                messagebox.showwarning("Warning", "Please select a student")
                return
            sid = self._get_student_id_by_name(student_name)
            report = self.system.get_student_report(sid)
            report_text = self._format_report_text(report)
            self.txt_report.delete("1.0", "end")
            self.txt_report.insert("1.0", report_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_report_pdf(self):
        try:
            report_content = self.txt_report.get("1.0", "end").strip()
            if not report_content:
                messagebox.showwarning("Warning", "Please generate a report first")
                return

            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Report as PDF"
            )
            if not filepath:
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Courier", size=10)
            for line in report_content.split('\n'):
                pdf.cell(w=0, h=5, txt=line, ln=True)
            pdf.output(filepath)
            messagebox.showinfo("Success", "✓ Report exported successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_summary(self):
        try:
            self.system.export_courses_summary("courses_summary_report.csv")
            messagebox.showinfo("Success", "✓ Course summary exported successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export summary: {str(e)}")


    # ========== COURSE UNITS PANEL METHODS ==========

    def refresh_course_units_panel(self):
        """Refresh the units treeview in the Courses tab for the currently selected course."""
        for row in self.tree_course_units.get_children():
            self.tree_course_units.delete(row)
        if not self.selected_course_id:
            self._lbl_units_title.configure(text="📋 Course Units  —  select a course above")
            return
        course = self.system.courses.get(self.selected_course_id)
        if not course:
            return
        self._lbl_units_title.configure(text=f"📋 Course Units under: {course.name} ({course.course_id})")
        for u in course.units:
            teacher_name = "Unassigned"
            tid = u.get('teacher_id')
            if tid and tid in self.system.teachers:
                teacher_name = self.system.teachers[tid].name
            self.tree_course_units.insert("", "end", values=(
                u.get('unit_id'), u.get('name'), u.get('credits'), teacher_name
            ))

    def on_unit_select(self, event=None):
        """Populate the inline unit form when a unit row is selected."""
        selected = self.tree_course_units.selection()
        if not selected:
            return
        vals = self.tree_course_units.item(selected[0], 'values')
        self.ent_unit_id.delete(0, 'end')
        self.ent_unit_id.insert(0, str(vals[0]))
        self.ent_unit_name.delete(0, 'end')
        self.ent_unit_name.insert(0, str(vals[1]))
        self.ent_unit_credits.delete(0, 'end')
        self.ent_unit_credits.insert(0, str(vals[2]))

    def _clear_unit_form(self):
        """Clear the inline unit form fields."""
        self.ent_unit_id.delete(0, 'end')
        self.ent_unit_name.delete(0, 'end')
        self.ent_unit_credits.delete(0, 'end')

    def update_unit_in_course(self):
        """Update the selected unit's name/credits for the selected course."""
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Select a course first")
            return
        uid = self.ent_unit_id.get().strip()
        name = self.ent_unit_name.get().strip()
        if not uid or not name:
            messagebox.showwarning("Warning", "Select a unit row, then edit Unit Name / Credits")
            return
        try:
            credits = float(self.ent_unit_credits.get())
        except Exception:
            messagebox.showerror("Error", "Credits must be a number")
            return
        try:
            self.system.update_course_unit(self.selected_course_id, uid, name=name, credits=credits)
            self.system.save_data()
            self.refresh_course_units_panel()
            self.refresh_course_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", f"✓ Unit {uid} updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_unit_from_course(self):
        """Delete the selected unit from the selected course."""
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Select a course first")
            return
        uid = self.ent_unit_id.get().strip()
        if not uid:
            messagebox.showwarning("Warning", "Select a unit row to delete")
            return
        if not messagebox.askyesno("Confirm", f"Delete unit '{uid}'? Related enrollments will be removed."):
            return
        try:
            self.system.delete_course_unit(self.selected_course_id, uid)
            self.system.save_data()
            self._clear_unit_form()
            self.refresh_course_units_panel()
            self.refresh_course_list()
            self.refresh_enrollment_list()
            self.refresh_teacher_list()
            self.update_comboboxes()
            messagebox.showinfo("Success", f"✓ Unit {uid} deleted")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = ctk.CTk()
    app = EduManageGUI(root)
    root.mainloop()
