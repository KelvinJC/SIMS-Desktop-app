
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

from db_sims_sqlite import Database
db = Database('new_single_user3.db')

class ClassTreeviewII(tk.Frame):
    def __init__(self, parent): # I doubt this root arg is required
        tk.Frame.__init__(self, parent)

        # Function that puts mainframe on screen (this is probably going to be cut and put as the callable function in a classs button)
        self.pack(side='right', fill='both', expand=True)

        # Add Search Box (Rememeber to implement 'Search' showing in bar )
        search_box = tk.Entry(self, width=60)
        search_box.pack(pady=4, padx=2, anchor=tk.NE)

        # Add some style
        style = ttk.Style()
        # Pick a theme
        #style.theme_use("default")
        # Configure our treeview colours
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=20,
                        fieldbackground="#D3D3D3"
                        )
        # Change selected colour
        style.map('Treeview',
                  background=[('selected', '#73c2fb')]) #a4bce9

        # Create Treeview Frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.X, anchor=tk.N, padx=(20, 0))

        # Treeview Scrollbar
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=(2,0))

        # Create Treeview
        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended', height=25)
        # Pack to the screen
        self.my_tree.pack(fill=tk.X)

        # Configure scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Define our columns. Reserve two extra null columns for subsequent child rows i.e student first and last names
        self.my_tree['columns'] = ('ID', 'Course', 'Course code', 'Class', 'R.Id', '', '')

        # Format our columns
        self.my_tree.column("#0", stretch=tk.NO, width=50)
        self.my_tree.column("ID", anchor=tk.CENTER, stretch=tk.NO, width=0)
        self.my_tree.column("Course", anchor=tk.W, stretch=tk.NO, width=200)
        self.my_tree.column("Course code", anchor=tk.W, width=100)
        self.my_tree.column("Class", anchor=tk.W, width=50)
        self.my_tree.column("R.Id", anchor=tk.W, width=30)
        self.my_tree.column("", anchor=tk.W, width=800)
        self.my_tree.column("", anchor=tk.W, width=1200)

        # Create Column headings
        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading("Course", text="Course", anchor=tk.W)
        self.my_tree.heading("Course code", text="Course code", anchor=tk.W)
        self.my_tree.heading("Class", text="Class", anchor=tk.W)
        self.my_tree.heading("R.Id", text="R.Id", anchor=tk.W)
        self.my_tree.heading("", text="", anchor=tk.W)
        self.my_tree.heading("", text="", anchor=tk.W)

        # Create striped Treeview rows
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="#f3f3f4")
        
        # Create session frame
        session_frame = tk.LabelFrame(self, text="Enter year")
        session_frame.pack(fill='x', expand='yes', padx=(20, 17), pady=5)
        
        # Create entry boxes for academic year and term     
        session_label = tk.Label(session_frame, text="Academic Year")
        session_label.grid(row=0, column=0, pady=10, padx=5)
        self.session_entry = tk.Entry(session_frame, text=session_label, width=30)
        self.session_entry.grid(row=0, column=1, pady=10, padx=5)
        
        # Create term dropdown menu 
        self.term_select = tk.StringVar()
        self.term_dropdown_list = ["Select term", "1", "2", "3"]
        term_dropdown_menu = ttk.OptionMenu(session_frame, self.term_select, *self.term_dropdown_list)
        term_dropdown_menu.grid(row=0, column=3, pady=10, padx=5)

        # Create Add class frame
        add_class_frame = tk.LabelFrame(self, text="Add class")
        add_class_frame.pack(fill='x', expand='yes', padx=(20, 17))

        # class widgets: Labels & entries
        self.class_select = tk.StringVar()
        self.class_select.set('Select Class')
        # Initiate class_list variable
        self.class_list = ['Select Class']
        # Get list of classes from database
        db_fetch_class_list = [class_pick[1] for class_pick in db.fetch_class()]
        # Concatenate both lists
        self.class_list += db_fetch_class_list
        # Create dropdown menu of classes
        class_dropdown_menu = ttk.OptionMenu(add_class_frame, self.class_select, *self.class_list)
        class_dropdown_menu.grid(row=0, column=2, padx=10, pady=10)

        # Create dropdown menu as attribute of add_class frame.
        self.course_select = tk.StringVar()
        self.course_dropdown_list = ["Select course"]
        # Get list of courses from database
        db_fetch_course_list = [course[1] + "  " + course[2] for course in db.fetch_course()]
        # Concatenate both lists
        self.course_dropdown_list += db_fetch_course_list
        # Create dropdown menu of courses
        course_dropdown_menu = ttk.OptionMenu(add_class_frame, self.course_select, *self.course_dropdown_list)
        course_dropdown_menu.grid(row=0, column=3, pady=10, padx=20)
        
        enroll_button = ttk.Button(add_class_frame, text="Enroll class", command=lambda: self.enroll_class_in_course(), width=42)
        enroll_button.grid(row=0, column=8, padx=10, pady=5, columnspan=2)
        
        self.populate_treeview()


    # Populate treeview from database
    def populate_treeview(self):
        # Clear tree currently in view
        self.my_tree.delete(*self.my_tree.get_children())  
        # Create counter (Treeview stripes)
        self.count = 1000
        self.count_class = 100
        self.count_student = 0
        # Labeled R.Id on treeview for brevity. Serves to ennumerate students in each class. Self.count_student not used since each iid must be unique and ennumeration by its nature must repeat numbers used
        student_roll_index = 1

        # Loop through records from database
        for record in db.fetch_course():
            if self.count % 2 == 0:
                # Insert records into treeview
               self.my_tree.insert(parent="", index="end", iid=self.count, open=True, values=(record[0], record[1], record[2]), tags=("evenrow",)) # record[0] = course_id 'from database', record[1]= course_name, record[2]= course_code if any
               # Insert class as child row of course
               for class_name in db.fetch_enrolments_grouped(record[0]):
                   if self.count_class % 2 == 0:
                       self.my_tree.insert(parent=self.count, index="end", iid=self.count_class, open=True, values=('', '', '', class_name[1]), tags=("oddrow",))
                        # Insert students as child rows of each class.
                       for rec in db.fetch_students_in_class(class_name[1]):
                           if self.count_student % 2 == 0:
                               self.my_tree.insert(parent=self.count_class, index="end", iid=self.count_student, values=('', '', '', '', student_roll_index, rec[1], rec[2]), tags=("evenrow",)) # null value is a 'filler column' included so as to shift student index under class column
                           else:
                               self.my_tree.insert(parent=self.count_class, index="end", iid=self.count_student, values=('', '', '', '', student_roll_index, rec[1], rec[2]), tags=("oddrow",))
                           self.count_student += 1
                           student_roll_index += 1
                   else:
                       self.my_tree.insert(parent=self.count, index="end", iid=self.count_class, values=('', '', '', class_name[1]), tags=("evenrow",))

                       for rec in db.fetch_students_in_class(class_name[1]):
                           if self.count_student % 2 == 0:
                               self.my_tree.insert(parent=self.count_class, index="end", iid=self.count_student, values=('', '', '', '', student_roll_index, rec[1], rec[2]), tags=("oddrow",)) # null value is a 'filler column' included so as to shift student index under class column
                           else:
                               self.my_tree.insert(parent=self.count_class, index="end", iid=self.count_student, values=('', '', '', '', student_roll_index, rec[1], rec[2]), tags=("evenrow",))
                           self.count_student += 1
                           student_roll_index += 1

                   self.count_class += 1
                   # Reset student count to 1 for next class
                   student_roll_index = 1
            else:
               self.my_tree.insert(parent="", index="end", iid=self.count, values=(record[0], record[1], record[2]), tags=("oddrow",))  # record[0] = course_id, record[1]= course_name, record[2]= course_code if any

               # Insert class as child row of course
               for class_name in db.fetch_enrolments_grouped(record[0]):
                   if self.count_class % 2 == 0:
                       self.my_tree.insert(parent=self.count, index="end", iid=self.count_class, values=('', '', '', class_name[1]), tags=("evenrow",))
                        # Insert students as child rows of each class.
                       for rec in db.fetch_students_in_class(class_name[1]):
                           if self.count_student % 2 == 0:
                               self.my_tree.insert(parent=self.count_class, index="end", iid=self.count_student, values=('', '', '', '', student_roll_index, rec[1], rec[2]), tags=("oddrow",)) # null value is a 'filler column' included so as to shift student index under class column
                           else:
                               self.my_tree.insert(parent=self.count_class, index="end", iid=self.count_student, values=('', '', '', '', student_roll_index, rec[1], rec[2]), tags=("evenrow",))
                           self.count_student += 1
                           student_roll_index += 1
                   else:
                       self.my_tree.insert(parent=self.count, index="end", iid=self.count_class, values=('', '', '', class_name[1]), tags=("oddrow",))

                       for rec in db.fetch_students_in_class(class_name[1]):
                           if self.count_student % 2 == 0:
                               self.my_tree.insert(parent=self.count_class, index="end", iid=self.count_student, values=('', '', '', '', student_roll_index, rec[1], rec[2]), tags=("evenrow",)) # null value is a 'filler column' included so as to shift student index under class column
                           else:
                               self.my_tree.insert(parent=self.count_class, index="end", iid=self.count_student, values=('', '', '', '', student_roll_index, rec[1], rec[2]), tags=("oddrow",))
                           self.count_student += 1
                           student_roll_index += 1

                   self.count_class += 1
                   # Reset student count to 1 for next class
                   student_roll_index = 1
            self.count += 1

    # For fun I guess
    # Move Row Up
    def up(self):
        rows = self.my_tree.selection()
        for row in rows:
           self.my_tree.move(row, self.my_tree.parent(row), self.my_tree.index(row)-1)

    # Move Row Down
    def down(self):
        rows = self.my_tree.selection()
        for row in reversed(rows):
           self.my_tree.move(row,self.my_tree.parent(row),self.my_tree.index(row)+1)

    def enroll_class_in_course(self):
        if self.course_select.get() != "Select course" and self.class_select.get() != "Select class":
            # Obtain course id
            course_list = db.fetch_course()
            
            for course in course_list:
                # Compare course entry with course name and course code fetched from database
                if self.course_select.get().split('  ')[0] == course[1] and self.course_select.get().split('  ')[1] == course[2]: # I used a double space when merging both course name and course code. For easier readability
                    # Assign course id to variable cid. Chose not to use course_id as variable name
                    cid = course[0]
            # Check if class has already been enrolled for course.
            for enrolment in db.fetch_enrolments_grouped(cid):
                if enrolment[1] == self.class_select.get() and enrolment[2] == self.course_select.get().split('  ')[0]:
                    messagebox.showinfo("Enrolment.","This class has been enrolled for the course.")
                else:
                     for record in db.fetch_student():
                         # Check for match between class entry and student's class, then create enrolment
                         if record[4] == self.class_select.get():
                             db.insert_enrolment(cid, record[0], self.class_select.get(), datetime.datetime.now())
                             self.populate_treeview()
        else:
            messagebox.showinfo("Selection Incomplete.","Please select class and course.")


   # Will also need a process to reverse enrolment
   # Delete enrolments?
