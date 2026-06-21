import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from system import EducationSystem
import re
import os
from datetime import datetime

# Set appearance and default theme
ctk.set_appearance_mode("light")
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
        self.dark_mode = False  # Track true light/dark mode

        # Define Colors for light and dark modes
        self.light_colors = {
            "primary": "#0F4C81",
            "secondary": "#2AA7A1",
            "bg": "#F4F7FB",
            "accent": "#F28C6F",
            "text": "#1F2937",
            "panel": "#FFFFFF",
            "input": "#EEF3F9",
            "highlight": "#2563EB",
            "muted": "#D8E2EE"
        }

        self.dark_colors = {
            "primary": "#111827",
            "secondary": "#1F2937",
            "bg": "#0B1220",
            "accent": "#06B6D4",
            "text": "#E5E7EB",
            "panel": "#111827",
            "input": "#1F2937",
            "highlight": "#3B82F6",
            "muted": "#374151"
        }

        self.current_colors = self.dark_colors if self.dark_mode else self.light_colors
        
        self.root.configure(fg_color=self.current_colors["bg"])
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Apply consistent TTK styles for treeviews/scrollbars matching the current theme."""
        tv_bg  = self.current_colors["panel"]
        tv_fg  = self.current_colors["text"]
        hdr_bg = self.current_colors["primary"]
        sel_bg = self.current_colors["highlight"]

        style = ttk.Style()
        style.theme_use("clam")

        # ── Treeview body ──────────────────────────────────────────────────────────
        style.configure("Treeview",
                        background=tv_bg,
                        foreground=tv_fg,
                        fieldbackground=tv_bg,
                        rowheight=38,
                        font=("Segoe UI", 15),
                        borderwidth=0,
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", sel_bg)],
                  foreground=[("selected", "#ffffff")])

        # ── Treeview headings ──────────────────────────────────────────────────────
        style.configure("Treeview.Heading",
                        background=hdr_bg,
                        foreground="#ffffff",
                        font=("Segoe UI", 15, "bold"),
                        relief="flat",
                        padding=(10, 9))
        style.map("Treeview.Heading",
                  background=[("active", sel_bg)],
                  relief=[("active", "flat")])

        # ── Scrollbars ─────────────────────────────────────────────────────────────
        sb_bg = self.current_colors["secondary"]
        sb_tr = self.current_colors["muted"]
        for orientation in ("Vertical", "Horizontal"):
            style.configure(f"{orientation}.TScrollbar",
                            background=sb_bg, troughcolor=sb_tr,
                            bordercolor=sb_tr, arrowcolor="#aaaaaa",
                            relief="flat")

    def validate_email(self, email):
        """Validate email format using regex pattern."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def _button_palette(self):
        """Centralized button colors for a cohesive UI language."""
        return {
            "primary": ("#2563EB", "#1D4ED8"),
            "info": ("#0EA5E9", "#0284C7"),
            "accent": ("#7C3AED", "#6D28D9"),
            "success": ("#10B981", "#059669"),
            "warning": ("#F59E0B", "#D97706"),
            "danger": ("#EF4444", "#DC2626"),
            "neutral": ("#64748B", "#475569"),
        }

    def _btn(self, parent, text, command, kind="primary", **kwargs):
        """Create styled buttons with shared defaults and palette-driven variants."""
        fg, hover = self._button_palette().get(kind, self._button_palette()["primary"])
        defaults = {
            "fg_color": fg,
            "hover_color": hover,
            "corner_radius": 10,
            "height": 34,
            "font": ("Segoe UI", 14, "bold"),
        }
        defaults.update(kwargs)
        return ctk.CTkButton(parent, text=text, command=command, **defaults)

    def toggle_theme(self):
        """Toggle between light and dark modes and rebuild tab content."""
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
                                    fg_color=self.current_colors["primary"], height=54)
        self._header.pack(fill="x", pady=(0, 4), padx=10)
        self._header.pack_propagate(False)
        self._header.configure(corner_radius=12)

        ctk.CTkLabel(
            self._header,
            text="\t\t\t\t🎓 EduManage — Advanced Education Management System",
            font=("Segoe UI", 19, "bold"),
            text_color="white"
        ).pack(side="left", padx=16)

        self.theme_toggle_btn = ctk.CTkButton(
            self._header,
            text="🌙 Dark",
            command=self.toggle_theme,
            width=110, height=30,
            fg_color="#F97316", hover_color="#EA580C",
            text_color="white", corner_radius=6,
            font=("Segoe UI", 12, "bold")
        )
        self.theme_toggle_btn.pack(side="right", padx=12)

        self.backup_btn = ctk.CTkButton(
            self._header,
            text="💾 Backup",
            command=self.create_backup_archive,
            width=100, height=30,
            fg_color="#10B981", hover_color="#059669",
            text_color="white", corner_radius=6,
            font=("Segoe UI", 12, "bold")
        )
        self.backup_btn.pack(side="right", padx=6)

        self._build_tabs_area()

    def _build_tabs_area(self):
        """Create (or recreate on theme toggle) the notebook and all tab contents."""
        self.notebook = ctk.CTkTabview(
            self._main_container,
            segmented_button_fg_color=self.current_colors["secondary"],
            segmented_button_selected_color=self.current_colors["highlight"],
            segmented_button_selected_hover_color=self.current_colors["primary"],
            text_color=self.current_colors["text"],
            text_color_disabled="#9CA3AF",
        )
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(2, 8))

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
        self._sync_auto_id_fields()

    def create_input_frame(self, parent, title):
        """Create a styled input frame."""
        frame = ctk.CTkFrame(
            parent,
            fg_color=self.current_colors["panel"],
            border_width=1,
            border_color=self.current_colors["muted"],
            corner_radius=14
        )
        frame.pack(fill="x", padx=10, pady=(8, 6))

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 15, "bold"),
            text_color=self.current_colors["primary"]
        ).pack(pady=(10, 2))

        inner_frame = ctk.CTkFrame(frame, fg_color=self.current_colors["bg"], corner_radius=10)
        inner_frame.pack(fill="x", padx=12, pady=(6, 12))

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

        self._btn(btn_frame, "➕ Add Student", self.add_student, "primary", width=128).pack(side="left", padx=5)
        self._btn(btn_frame, "✏️ Update", self.update_student, "warning", width=108).pack(side="left", padx=5)
        self._btn(btn_frame, "🗑️ Delete", self.delete_student, "danger", width=108).pack(side="left", padx=5)
        self._btn(btn_frame, "🔄 Clear", self.clear_student_form, "neutral", width=108).pack(side="left", padx=5)

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

        self._btn(btn_frame, "➕ Add Course", self.add_course, "primary", width=128).pack(side="left", padx=5)
        self._btn(btn_frame, "✏️ Update", self.update_course, "warning", width=108).pack(side="left", padx=5)
        self._btn(btn_frame, "🗑️ Delete", self.delete_course, "danger", width=108).pack(side="left", padx=5)
        self._btn(btn_frame, "📥 Save Course Summary", self.export_summary, "success", width=108).pack(side="left", padx=5)

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
        self._btn(title_row, "⚙️ Manage Course-Units",
              self.open_manage_units_dialog,
              "accent", width=160, height=30).pack(side="right", padx=4)

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

        self._btn(unit_form, "➕ Add", self.add_unit_to_course, "primary", width=90).grid(row=0, column=6, padx=4, pady=4)
        self._btn(unit_form, "✏️ Update", self.update_unit_in_course, "warning", width=100).grid(row=0, column=7, padx=4, pady=4)
        self._btn(unit_form, "🗑️ Delete", self.delete_unit_from_course, "danger", width=100).grid(row=0, column=8, padx=4, pady=4)
        self._btn(unit_form, "🔄 Clear", self._clear_unit_form, "neutral", width=90).grid(row=0, column=9, padx=4, pady=4)

        courses_pane.add(units_outer, minsize=220)
        # Keep both panes visible on initial render so the units table is not collapsed.
        self.root.after(60, lambda: courses_pane.sash_place(0, 0, 260))

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

        self._btn(btn_frame, "➕ Add Teacher", self.add_teacher, "primary", width=128).pack(side="left", padx=5)
        self._btn(btn_frame, "✏️ Update", self.update_teacher, "warning", width=108).pack(side="left", padx=5)
        self._btn(btn_frame, "🗑️ Delete", self.delete_teacher, "danger", width=108).pack(side="left", padx=5)
        self._btn(btn_frame, "🔄 Clear", self.clear_teacher_form, "neutral", width=108).pack(side="left", padx=5)

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

        self._btn(assign_btn, "Assign Course", self.assign_course_only, "info", width=128).pack(side="left", padx=5)
        self._btn(assign_btn, "Assign Unit", self.assign_unit_only, "success", width=128).pack(side="left", padx=5)

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
        ctrl_bg = self.current_colors["panel"]
        ctrl_card = ctk.CTkFrame(
            top_outer,
            fg_color=ctrl_bg,
            border_width=1,
            border_color=self.current_colors["muted"],
            corner_radius=12
        )
        ctrl_card.pack(fill="x", padx=0, pady=(0, 6))

        ctk.CTkLabel(ctrl_card, text="Enroll Student & Assign Grade",
                     font=("Segoe UI", 14, "bold"), text_color=self.current_colors["primary"]).pack(pady=(8, 0))

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

        self._btn(row1, "📝 Enroll Course", self.enroll_student,
              "info", width=144).grid(row=0, column=4, padx=8, pady=6)

        row1.columnconfigure((1, 3), weight=1)

        row2 = ctk.CTkFrame(ctrl_inner, fg_color=self.current_colors["bg"])
        row2.pack(fill="x", padx=6, pady=(0, 6))

        ctk.CTkLabel(row2, text="Grade (0-100):", text_color=self.current_colors["text"]).pack(side="left", padx=5)
        self.ent_grade = ctk.CTkEntry(row2, placeholder_text="Enter grade", width=100, corner_radius=8)
        self.ent_grade.pack(side="left", padx=5)
        self._btn(row2, "✔️ Assign Grade", self.assign_grade,
              "success", width=144).pack(side="left", padx=5)
        self._btn(row2, "🗑️ Remove Enrollment", self.delete_enrollment,
              "danger", width=164).pack(side="left", padx=5)

        # Units listbox row
        units_card = ctk.CTkFrame(
            top_outer,
            fg_color=ctrl_bg,
            border_width=1,
            border_color=self.current_colors["muted"],
            corner_radius=12
        )
        units_card.pack(fill="x", padx=0, pady=(0, 4))

        ctk.CTkLabel(units_card, text="Course Units  —  select units then click Enroll Units",
                     font=("Segoe UI", 14, "bold"), text_color=self.current_colors["primary"]).pack(pady=(8, 0))

        units_inner = tk.Frame(units_card, bg=self.current_colors["bg"],
                               highlightthickness=1,
                               highlightbackground=self.current_colors["secondary"])
        units_inner.pack(fill="x", padx=10, pady=8, ipady=2)

        self.lb_units = tk.Listbox(
            units_inner,
            selectmode=tk.MULTIPLE,
            bg=self.current_colors["panel"],
            fg=self.current_colors["text"],
            selectbackground=self.current_colors["highlight"],
            activestyle="none",
            highlightthickness=0,
            relief="flat",
            exportselection=False,
            height=5,
            font=("Segoe UI", 13)
        )
        self.lb_units.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)

        lb_scroll = tk.Scrollbar(units_inner, orient="vertical", command=self.lb_units.yview)
        lb_scroll.pack(side="right", fill="y", padx=(0, 4), pady=4)
        self.lb_units.configure(yscrollcommand=lb_scroll.set)

        units_btns = tk.Frame(units_card, bg=self.current_colors["panel"])
        units_btns.pack(fill="x", padx=10, pady=(0, 8))
        self._btn(units_btns, "📝 Enroll Selected Units",
              self.enroll_selected_units, "info", width=192).pack(side="left", padx=4)
        self._btn(units_btns, "✔️ Grade Selected Unit",
              self.assign_grade_to_selected_unit, "success", width=192).pack(side="left", padx=4)

        enroll_pane.add(top_outer, minsize=160)

        # ── Bottom pane: enrollments table ─────────────────────────────────────────
        bottom_outer = tk.Frame(enroll_pane, bg=self.current_colors["bg"])

        tbl_title = tk.Frame(bottom_outer, bg=self.current_colors["primary"])
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

        self._btn(inner, "📄 Generate", self.generate_report, "primary", width=130).pack(side="left", padx=5)
        self._btn(inner, "📥 Export PDF", self.export_report_pdf, "accent", width=140).pack(side="left", padx=5)

        ctk.CTkLabel(
            report_frame,
            text="Preview is plain text for speed and readability. Final branded styling is applied in exported PDF.",
            font=("Segoe UI", 11),
            text_color=self.current_colors["text"],
            wraplength=980,
            justify="left"
        ).pack(fill="x", padx=8, pady=(2, 8))

        text_frame = ctk.CTkFrame(self.tab_reports, fg_color=self.current_colors["bg"])
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.txt_report = ctk.CTkTextbox(text_frame, corner_radius=10, font=("Consolas", 13))
        self.txt_report.pack(fill="both", expand=True)

    def setup_analysis_tab(self):
        """Setup analysis dashboard with charts."""
        btn_frame = ctk.CTkFrame(self.tab_analysis, fg_color=self.current_colors["bg"])
        btn_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(btn_frame, text="Student:", text_color=self.current_colors["text"]).pack(side='left', padx=5)
        self.cb_analysis_student = ctk.CTkComboBox(btn_frame, corner_radius=8, state="readonly")
        self.cb_analysis_student.pack(side='left', padx=5)

        ctk.CTkLabel(btn_frame, text="Teacher:", text_color=self.current_colors["text"]).pack(side='left', padx=8)
        self.cb_analysis_teacher = ctk.CTkComboBox(btn_frame, corner_radius=8, state="readonly")
        self.cb_analysis_teacher.pack(side='left', padx=5)

        self._btn(btn_frame, "📊 Refresh Charts", self.refresh_analysis, "primary", width=164).pack(side="left", padx=10)
        self._btn(btn_frame, "↺ Clear Selection", self.clear_analysis_selection, "neutral", width=164).pack(side="left", padx=4)

        self.canvas_frame = ctk.CTkFrame(self.tab_analysis, fg_color=self.current_colors["bg"])
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def refresh_analysis(self):
        """Refresh and display analysis charts."""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        analytics = self.system.get_analytics()

        fig = Figure(figsize=(14, 8), dpi=90, facecolor=self.current_colors["bg"])
        
        # Chart 1
        if analytics["students_per_course"]:
            ax1 = fig.add_subplot(2, 2, 1)
            courses = list(analytics["students_per_course"].keys())
            counts = list(analytics["students_per_course"].values())
            ax1.bar(courses, counts, color="#3B82F6", edgecolor="#1D4ED8", linewidth=1.5)
            ax1.set_title("Students Enrolled per Course", fontsize=16, fontweight='bold', color=self.current_colors["text"])
            ax1.set_xlabel("Course", fontsize=14, color=self.current_colors["text"])
            ax1.set_ylabel("Count", fontsize=14, color=self.current_colors["text"])
            ax1.tick_params(axis='x', labelsize=14, rotation=45, colors=self.current_colors["text"])
            ax1.tick_params(axis='y', labelsize=14, colors=self.current_colors["text"])
            ax1.set_facecolor(self.current_colors["panel"])

        # Chart 2
        if analytics["grades_distribution"]:
            ax2 = fig.add_subplot(2, 2, 2)
            order = ['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']
            dist = [analytics["grades_distribution"].get(k, 0) for k in order]
            bars = ax2.bar(order, dist, color="#10B981", edgecolor="#059669", linewidth=1.5)
            ax2.set_title("Grade Distribution", fontsize=16, fontweight='bold', color=self.current_colors["text"])
            ax2.set_xlabel("Letter Grade", fontsize=14, color=self.current_colors["text"])
            ax2.set_ylabel("Count", fontsize=14, color=self.current_colors["text"])
            ax2.tick_params(axis='x', labelsize=14, rotation=45, colors=self.current_colors["text"])
            ax2.tick_params(axis='y', labelsize=14, colors=self.current_colors["text"])
            ax2.set_facecolor(self.current_colors["panel"])

        # Chart 3
        if analytics["teacher_workload"]:
            ax3 = fig.add_subplot(2, 2, 3)
            teachers = list(analytics["teacher_workload"].keys())
            workload = list(analytics["teacher_workload"].values())
            ax3.barh(teachers, workload, color="#F97316", edgecolor="#EA580C", linewidth=1.5)
            ax3.set_title("Teacher Workload", fontsize=16, fontweight='bold', color=self.current_colors["text"])
            ax3.set_xlabel("Number of Units", fontsize=14, color=self.current_colors["text"])
            ax3.tick_params(axis='x', labelsize=14, colors=self.current_colors["text"])
            ax3.tick_params(axis='y', labelsize=14, colors=self.current_colors["text"])
            ax3.set_facecolor(self.current_colors["panel"])

        # Chart 4
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.axis('off')
        stats_text = f"SYSTEM STATISTICS\n\n✓ Total Students: {analytics['total_students']}\n✓ Total Courses: {analytics['total_courses']}\n✓ Total Teachers: {analytics['total_teachers']}\n✓ Avg Grade: {analytics['avg_grade']:.1f}%"

        student_pick = (self.cb_analysis_student.get() or "").strip()
        teacher_pick = (self.cb_analysis_teacher.get() or "").strip()

        if student_pick:
            sid = student_pick.split(" - ")[0]
            student = self.system.students.get(sid)
            if student:
                enrolled = len(student.enrolled_courses)
                grades = []
                for data in student.enrolled_courses.values():
                    for grade in data.get('units', {}).values():
                        if grade is not None:
                            grades.append(grade)
                avg_grade = (sum(grades) / len(grades)) if grades else 0.0
                stats_text += (
                    f"\n\nSTUDENT SNAPSHOT\n"
                    f"• {student.name} ({student.person_id})\n"
                    f"• Enrolled Courses: {enrolled}\n"
                    f"• Graded Units: {len(grades)}\n"
                    f"• Current Avg: {avg_grade:.1f}%"
                )

        if teacher_pick:
            tid = teacher_pick.split(" - ")[0]
            teacher = self.system.teachers.get(tid)
            if teacher:
                taught_course_count = len(getattr(teacher, 'taught_units', {}) or {})
                unit_count = 0
                for units in (getattr(teacher, 'taught_units', {}) or {}).values():
                    unit_count += len(units)
                stats_text += (
                    f"\n\nTEACHER SNAPSHOT\n"
                    f"• {teacher.name} ({teacher.person_id})\n"
                    f"• Department: {teacher.department}\n"
                    f"• Courses Assigned: {taught_course_count}\n"
                    f"• Units Assigned: {unit_count}"
                )

        ax4.text(0.5, 0.5, stats_text, fontsize=14, ha='center', va='center',
                family='monospace', color=self.current_colors["text"],
            bbox=dict(boxstyle='round', facecolor=self.current_colors["highlight"], alpha=0.2, pad=1))

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ========== CRUD OPERATIONS ==========

    def add_student(self):
        name = self.ent_sname.get().strip()
        email = self.ent_semail.get().strip()
        
        if not name or not email:
            messagebox.showwarning("Warning", "Name and email are required")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
            return
            
        try:
            sid = self.system.next_student_id()
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
        name = self.ent_cname.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Course name is required")
            return
            
        try:
            credits = int(self.ent_ccredits.get())
            cid = self.system.next_course_id()
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
            tid = self.system.next_teacher_id()
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
        
        uname = self.ent_unit_name.get().strip()
        
        if not uname:
            messagebox.showwarning("Warning", "Unit name is required")
            return
            
        try:
            ucredits = float(self.ent_unit_credits.get())
        except Exception:
            messagebox.showerror("Error", "Unit credits must be a number")
            return
            
        try:
            uid = self.system.next_unit_id()
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
                self.cb_assign_unit.configure(values=[])
                self.cb_assign_unit.set("")
                return
            cid = course_str.split(' - ')[0]
            course = self.system.courses.get(cid)
            vals = []
            if course:
                vals = [f"{str(u.get('unit_id'))} - {u.get('name')}" for u in course.units]
            self.cb_assign_unit.configure(values=vals)
            self.cb_assign_unit.set("")
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

            course = self.system.courses.get(course_id)
            if not course or unit_id not in {str(u.get('unit_id')) for u in course.units}:
                messagebox.showwarning("Warning", "Please select a unit that belongs to the selected course.")
                return

            self.system.assign_teacher_to_unit(teacher_id, course_id, unit_id)
            self.system.save_data()
            self.refresh_course_list()
            self.refresh_teacher_list()
            self.on_assign_course_selected()
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
                    unit_label = ", ".join(units)
                    parts.append(f"{cid}({unit_label})")
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
        s_list = [f"{s.person_id} - {s.name}" for s in self.system.students.values()]
        c_list = [f"{c.course_id} - {c.name}" for c in self.system.courses.values()]
        t_list = [f"{t.person_id} - {t.name}" for t in self.system.teachers.values()]
        
        self.cb_students.configure(values=s_list)
        self.cb_courses.configure(values=c_list)
        self.cb_report_student.configure(values=s_list)
        self.cb_assign_teacher.configure(values=t_list)
        self.cb_assign_course.configure(values=c_list)
        self.cb_analysis_student.configure(values=s_list)
        self.cb_analysis_teacher.configure(values=t_list)

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

        self._sync_auto_id_fields()

    # ========== HELPER FUNCTIONS ==========

    def _get_student_id_by_name(self, name):
        """Helper to get student ID by name."""
        for s in self.system.students.values():
            if name in {s.name, f"{s.person_id} - {s.name}"}:
                return s.person_id
        raise ValueError(f"Student '{name}' not found")

    def clear_analysis_selection(self):
        try:
            self.cb_analysis_student.set("")
            self.cb_analysis_teacher.set("")
        except Exception:
            pass
        self.refresh_analysis()

    def _sync_auto_id_fields(self):
        """Populate the ID inputs with the next generated IDs so users do not type them manually."""
        try:
            self.ent_sid.delete(0, 'end')
            self.ent_sid.insert(0, self.system.next_student_id())
        except Exception:
            pass
        try:
            self.ent_cid.delete(0, 'end')
            self.ent_cid.insert(0, self.system.next_course_id())
        except Exception:
            pass
        try:
            self.ent_tid.delete(0, 'end')
            self.ent_tid.insert(0, self.system.next_teacher_id())
        except Exception:
            pass
        try:
            self.ent_unit_id.delete(0, 'end')
            if self.selected_course_id:
                self.ent_unit_id.insert(0, self.system.next_unit_id())
        except Exception:
            pass

    def clear_student_form(self):
        self.ent_sid.delete(0, 'end')
        self.ent_sname.delete(0, 'end')
        self.ent_semail.delete(0, 'end')
        self.selected_student_id = None
        self._sync_auto_id_fields()

    def clear_course_form(self):
        self.ent_cid.delete(0, 'end')
        self.ent_cname.delete(0, 'end')
        self.ent_ccredits.delete(0, 'end')
        self.selected_course_id = None
        self._sync_auto_id_fields()

    def clear_teacher_form(self):
        self.ent_tid.delete(0, 'end')
        self.ent_tname.delete(0, 'end')
        self.ent_temail.delete(0, 'end')
        self.ent_tdept.delete(0, 'end')
        self.selected_teacher_id = None
        self._sync_auto_id_fields()

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
        TV_BG   = self.current_colors["panel"]
        TV_FG   = self.current_colors["text"]
        HDR_BG  = self.current_colors["primary"]
        ENT_BG  = self.current_colors["input"]
        ENT_FG  = self.current_colors["text"]
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
                         highlightcolor=self.current_colors["highlight"])
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

        def _dialog_btn(parent, text, cmd, kind="primary", side="left"):
            b = self._btn(parent, text, cmd, kind, height=36, width=122)
            b.pack(side=side, padx=5)
            return b

        _dialog_btn(btn_bar, "\u2795 Add", add_unit, "info")
        _dialog_btn(btn_bar, "\u270f\ufe0f Update", update_unit, "warning")
        _dialog_btn(btn_bar, "\ud83d\uddd1\ufe0f Delete", delete_unit, "danger")
        _dialog_btn(btn_bar, "\ud83d\udd04 Clear", lambda: clear_form(unlock_id=True), "neutral")
        _dialog_btn(btn_bar, "\u2715 Close", dlg.destroy, "neutral", side="right")

        tree.bind("<<TreeviewSelect>>", on_select)
        refresh_tree()

    def _format_report_text(self, report):
        lines = []
        lines.append("=" * 86)
        lines.append(" " * 29 + "ACADEMIC REPORT CARD (PREVIEW)")
        lines.append("=" * 86)
        lines.append("")
        lines.append(f"Student Name : {report['student_name']}")
        lines.append(f"Student ID   : {report['student_id']}")
        lines.append(f"Generated On : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("Note: Export PDF for full branding, color badges, and signature/footer sections.")
        lines.append("")
        lines.append("-" * 86)
        lines.append("COURSE DETAILS")
        lines.append("-" * 86)

        for course in report['courses']:
            lines.append(f"Course: {course['course_name']}   |   Course GPA: {course['course_gpa']:.2f}")
            lines.append(f"{'#':<3} {'Unit Name':<24} {'Credit':<8} {'Grade':<8} {'Letter':<8} {'Points':<8} {'Instructor':<20}")
            lines.append("-" * 86)
            
            for i, unit in enumerate(course['units'], 1):
                grade = unit.get('grade') if unit.get('grade') is not None else 'N/A'
                letter = unit.get('letter', 'N/A')
                point = f"{unit.get('point'):.1f}" if isinstance(unit.get('point'), (int, float)) else 'N/A'
                teacher = unit.get('teacher', 'Unassigned')[:20]
                unit_name = unit.get('unit_name', '')[:24]
                credits = unit.get('credits', 'N/A')
                lines.append(
                    f"{i:<3} {unit_name:<24} {str(credits):<8} {str(grade):<8} {letter:<8} {point:<8} {teacher:<20}"
                )
            lines.append("-" * 86)
            lines.append("")

        lines.append("=" * 86)
        lines.append(f"OVERALL CUMULATIVE GPA (CGPA): {report['cgpa']:.2f}")
        lines.append("=" * 86)
        
        return "\n".join(lines)

    def _report_pdf_palette(self):
        """Centralized report PDF palette for quick branding updates."""
        return {
            "primary": "#0F4C81",
            "secondary": "#F28C6F",
            "light": "#EEF3F9",
            "slate": "#334155",
            "border": "#CBD5E1",
            "grid": "#94A3B8",
            "header_box": "#1E3A8A",
            "cgpa_box": "#FB7185",
        }

    def _find_report_logo_path(self):
        """Return first available institutional logo path, else None."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, "images", "institution_logo.png"),
            os.path.join(base_dir, "images", "school_logo.png"),
            os.path.join(base_dir, "images", "logo.png"),
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

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
            student_name = self.cb_report_student.get()
            if not student_name:
                messagebox.showwarning("Warning", "Please generate a report first")
                return

            sid = self._get_student_id_by_name(student_name)
            report = self.system.get_student_report(sid)

            try:
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import A4
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import mm
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
            except ImportError:
                messagebox.showerror(
                    "Missing Dependency",
                    "ReportLab is required for styled PDF export.\n\nInstall with:\n  pip install reportlab"
                )
                return

            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Report as PDF"
            )
            if not filepath:
                return

            palette = self._report_pdf_palette()
            primary = colors.HexColor(palette["primary"])
            secondary = colors.HexColor(palette["secondary"])
            light = colors.HexColor(palette["light"])
            slate = colors.HexColor(palette["slate"])

            def grade_badge_style(grade_value, letter_value):
                """Return (background, text_color) for grade cells."""
                if isinstance(grade_value, (int, float)):
                    if grade_value >= 85:
                        return colors.HexColor("#16A34A"), colors.white
                    if grade_value >= 70:
                        return colors.HexColor("#2563EB"), colors.white
                    if grade_value >= 60:
                        return colors.HexColor("#EA580C"), colors.white
                    return colors.HexColor("#DC2626"), colors.white

                letter = str(letter_value).upper()
                if letter in {"A+", "A", "A-"}:
                    return colors.HexColor("#16A34A"), colors.white
                if letter in {"B+", "B", "B-"}:
                    return colors.HexColor("#2563EB"), colors.white
                if letter in {"C+", "C", "C-"}:
                    return colors.HexColor("#EA580C"), colors.white
                if letter in {"D", "E", "F"}:
                    return colors.HexColor("#DC2626"), colors.white
                return colors.HexColor("#E2E8F0"), slate

            def draw_page_chrome(canvas, doc_obj):
                """Draw page-level footer with document metadata and page number."""
                canvas.saveState()
                canvas.setStrokeColor(colors.HexColor(palette["border"]))
                canvas.setLineWidth(0.8)
                canvas.line(12 * mm, 10 * mm, A4[0] - 12 * mm, 10 * mm)
                canvas.setFont("Helvetica", 8)
                canvas.setFillColor(colors.HexColor("#64748B"))
                canvas.drawString(12 * mm, 6.2 * mm, "EduManage Confidential Academic Report")
                canvas.drawRightString(A4[0] - 12 * mm, 6.2 * mm, f"Page {doc_obj.page}")
                canvas.restoreState()

            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                leftMargin=12 * mm,
                rightMargin=12 * mm,
                topMargin=12 * mm,
                bottomMargin=12 * mm
            )

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "TitleStyle",
                parent=styles["Title"],
                fontName="Helvetica-Bold",
                fontSize=18,
                alignment=1,
                textColor=colors.white,
                backColor=primary,
                spaceAfter=8,
                leading=22,
            )
            subtitle_style = ParagraphStyle(
                "SubtitleStyle",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=10,
                alignment=1,
                textColor=colors.HexColor("#334155"),
                spaceAfter=8,
            )
            section_style = ParagraphStyle(
                "SectionStyle",
                parent=styles["Heading3"],
                fontName="Helvetica-Bold",
                fontSize=11,
                textColor=primary,
                spaceBefore=6,
                spaceAfter=5,
            )

            logo_path = self._find_report_logo_path()
            if logo_path:
                header_left = Image(logo_path, width=16 * mm, height=16 * mm)
            else:
                header_left = "EM"

            story = []
            header_data = [[header_left, "ACADEMIC REPORT CARD\nEduManage Education Management System"]]
            header_table = Table(header_data, colWidths=[20 * mm, 160 * mm])
            header_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), primary),
                ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
                ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (0, 0), 13),
                ("ALIGN", (0, 0), (0, 0), "CENTER"),
                ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
                ("BACKGROUND", (1, 0), (1, 0), primary),
                ("TEXTCOLOR", (1, 0), (1, 0), colors.white),
                ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (1, 0), (1, 0), 14),
                ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
                ("LEFTPADDING", (1, 0), (1, 0), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor(palette["header_box"])),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 8))

            story.append(Paragraph("Term: Current Session", subtitle_style))

            info_data = [
                ["Student Name", report["student_name"]],
                ["Student ID", report["student_id"]],
                ["Generated On", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ]
            info_table = Table(info_data, colWidths=[36 * mm, 140 * mm])
            info_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), light),
                ("TEXTCOLOR", (0, 0), (0, -1), primary),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor(palette["grid"])),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor(palette["border"])),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(info_table)
            story.append(Spacer(1, 8))
            story.append(Paragraph("Course and Unit Performance", section_style))

            table_rows = [["Course", "Unit", "Cr", "Grade", "Letter", "Points", "Teacher"]]
            grade_badge_commands = []
            current_row = 1
            for course in report["courses"]:
                first_row = True
                for unit in course["units"]:
                    grade = unit.get("grade") if unit.get("grade") is not None else "N/A"
                    letter = unit.get("letter", "N/A")
                    point = f"{unit.get('point'):.1f}" if isinstance(unit.get("point"), (int, float)) else "N/A"
                    teacher = unit.get("teacher", "Unassigned")
                    table_rows.append([
                        course["course_name"] if first_row else "",
                        str(unit.get("unit_name", "")),
                        str(unit.get("credits", "N/A")),
                        str(grade),
                        str(letter),
                        str(point),
                        str(teacher),
                    ])

                    badge_bg, badge_fg = grade_badge_style(unit.get("grade"), letter)
                    grade_badge_commands.extend([
                        ("BACKGROUND", (3, current_row), (3, current_row), badge_bg),
                        ("TEXTCOLOR", (3, current_row), (3, current_row), badge_fg),
                        ("BACKGROUND", (4, current_row), (4, current_row), badge_bg),
                        ("TEXTCOLOR", (4, current_row), (4, current_row), badge_fg),
                        ("FONTNAME", (3, current_row), (4, current_row), "Helvetica-Bold"),
                    ])

                    first_row = False
                    current_row += 1

                table_rows.append([
                    f"Course GPA: {course['course_gpa']:.2f}",
                    "", "", "", "", "", ""
                ])
                current_row += 1

            perf_table = Table(
                table_rows,
                colWidths=[34 * mm, 44 * mm, 12 * mm, 16 * mm, 16 * mm, 18 * mm, 40 * mm],
                repeatRows=1,
            )

            base_style = [
                ("BACKGROUND", (0, 0), (-1, 0), primary),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (2, 1), (5, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor(palette["grid"])),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor(palette["border"])),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]

            for i in range(1, len(table_rows)):
                if str(table_rows[i][0]).startswith("Course GPA:"):
                    base_style.extend([
                        ("BACKGROUND", (0, i), (-1, i), colors.HexColor("#E2E8F0")),
                        ("TEXTCOLOR", (0, i), (-1, i), slate),
                        ("FONTNAME", (0, i), (0, i), "Helvetica-Bold"),
                        ("SPAN", (0, i), (-1, i)),
                        ("ALIGN", (0, i), (-1, i), "LEFT"),
                    ])
                elif i % 2 == 0:
                    base_style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F8FAFC")))

            base_style.extend(grade_badge_commands)
            perf_table.setStyle(TableStyle(base_style))
            story.append(perf_table)
            story.append(Spacer(1, 10))

            cgpa_table = Table(
                [[f"OVERALL CUMULATIVE GPA (CGPA): {report['cgpa']:.2f}"]],
                colWidths=[180 * mm],
            )
            cgpa_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), secondary),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 1.0, colors.HexColor(palette["cgpa_box"])),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]))
            story.append(cgpa_table)
            story.append(Spacer(1, 14))

            signature_table = Table(
                [["Prepared By", "Verified By", "Registrar Signature"],
                 ["________________________", "________________________", "________________________"]],
                colWidths=[60 * mm, 60 * mm, 60 * mm],
            )
            signature_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 0), (-1, 0), primary),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("FONTSIZE", (0, 1), (-1, 1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(signature_table)

            story.append(Spacer(1, 4))
            footer_note = Paragraph(
                "<para align='center'><font size='8' color='#64748B'>"
                "This report is system-generated and intended for official academic use only."
                "</font></para>"
            )
            story.append(footer_note)

            doc.build(story, onFirstPage=draw_page_chrome, onLaterPages=draw_page_chrome)
            messagebox.showinfo("Success", "✓ Report exported successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_summary(self):
        try:
            self.system.export_courses_summary("courses_summary_report.csv")
            messagebox.showinfo("Success", "✓ Course summary saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export summary: {str(e)}")

    def create_backup_archive(self):
        try:
            backup_path = self.system.create_backup_zip()
            filename = os.path.basename(backup_path)
            messagebox.showinfo(
                "Backup Successful",
                f"✓ Database backed up successfully!\n\nArchive name:\n{filename}\n\nSaved under Data_Storage(CSV)/Backups/"
            )
        except Exception as e:
            messagebox.showerror("Backup Error", f"Failed to create backup: {str(e)}")


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
