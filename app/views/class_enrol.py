
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from models.database import db


class EnrolClass(tk.Frame):
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
        self.my_tree['columns'] = ('ID', 'Subject', 'Class', 'R.Id', '', '', '')

        # Format our columns
        self.my_tree.column("#0", stretch=tk.NO, width=50)
        self.my_tree.column("ID", anchor=tk.CENTER, stretch=tk.NO, width=0)
        self.my_tree.column("Subject", anchor=tk.W, stretch=tk.NO, width=300)
        self.my_tree.column("Class", anchor=tk.W, width=50)
        self.my_tree.column("R.Id", anchor=tk.W, width=30)
        self.my_tree.column("", anchor=tk.W, width=800)
        self.my_tree.column("", anchor=tk.W, width=800)
        self.my_tree.column("", anchor=tk.W, width=1200)

        # Create Column headings
        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading("Subject", text="Subject", anchor=tk.W)
        self.my_tree.heading("Class", text="Class", anchor=tk.W)
        self.my_tree.heading("R.Id", text="R.Id", anchor=tk.W)
        self.my_tree.heading("", text="", anchor=tk.W)
        self.my_tree.heading("", text="", anchor=tk.W)
        self.my_tree.heading("", text="", anchor=tk.W)

        # Create striped Treeview rows
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="#f3f3f4")

        # Create Add class frame
        add_class_frame = tk.LabelFrame(self, text="Add class")
        add_class_frame.pack(fill='x', expand='yes', padx=(20, 17))

        # Selection widgets
        # Create class dropdown menu as attribute of add_class_frame.
        # Initiate class_list variable
        self.class_list = ["Select class"]
        # Get list of classes from database
        db_fetch_class_list = [class_pick[1] for class_pick in db.fetch_class()]
        # Concatenate both lists
        self.class_list += db_fetch_class_list
        # Create dropdown menu of classes
        self.class_dropdown_menu = ttk.Combobox(add_class_frame, value=self.class_list, width=30, state='readonly')
        self.class_dropdown_menu.current(0)
        self.class_dropdown_menu.grid(row=0, column=2, padx=10, pady=10)

        # Create subject dropdown menu as attribute of holder frame.
        self.subject_dropdown_list = ["Select subject"]
        # Get list of subjects from database
        db_fetch_subject_list = [subject[1] for subject in db.fetch_subject()]
        # Concatenate both lists
        self.subject_dropdown_list += db_fetch_subject_list
        # Create dropdown menu of subjects
        self.subject_dropdown_menu = ttk.Combobox(add_class_frame, value=self.subject_dropdown_list, width=30, state='readonly')
        self.subject_dropdown_menu.grid(row=0, column=3, pady=10, padx=20)
        self.subject_dropdown_menu.current(0)

        enroll_button = ttk.Button(add_class_frame, text="Enroll class", command=lambda: self.enroll_class_in_subject(), width=42)
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
        for record in db.fetch_subject():
            if self.count % 2 == 0:
                # Insert records into treeview
               self.my_tree.insert(parent="", index="end", iid=self.count, open=True, values=(record[0], record[1]), tags=("evenrow",)) # record[0] = subject_id 'from database', record[1]= subject_name, record[2]= subject_code if any
               # Insert class as child row of subject
               for class_name in db.fetch_enrolments_grouped(record[0]):
                   if self.count_class % 2 == 0:
                       self.my_tree.insert(parent=self.count, index="end", iid=self.count_class, open=True, values=('', '', class_name[1]), tags=("oddrow",))
                   else:
                       self.my_tree.insert(parent=self.count, index="end", iid=self.count_class, values=('', '', class_name[1]), tags=("evenrow",))

                   self.count_class += 1
                   # Reset student count to 1 for next class
                   student_roll_index = 1
            else:
               self.my_tree.insert(parent="", index="end", iid=self.count, values=(record[0], record[1]), tags=("oddrow",))  # record[0] = subject_id, record[1]= subject_name, record[2]= subject_code if any

               # Insert class as child row of subject
               for class_name in db.fetch_enrolments_grouped(record[0]):
                   if self.count_class % 2 == 0:
                       self.my_tree.insert(parent=self.count, index="end", iid=self.count_class, values=('', '', class_name[1]), tags=("evenrow",))
                   else:
                       self.my_tree.insert(parent=self.count, index="end", iid=self.count_class, values=('', '', class_name[1]), tags=("oddrow",))
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

    def enroll_class_in_subject(self):
        '''
        Enrols all the students in a class in a subject

        Returns
        -------
        None.

        '''
        if self.subject_dropdown_menu.get() != "Select subject" and self.class_dropdown_menu.get() != "Select class":
            # Obtain subject id
            subject_list = db.fetch_subject()
            for subject in subject_list:
                # Compare subject entry with subject name fetched from database
                if self.subject_dropdown_menu.get() == subject[1]:
                    # Assign subject id to variable cid. Chose not to use subject_id as variable name
                    cid = subject[0]
                    print(db.fetch_enrolments_grouped(cid))
                    #print(db.fetch_student())
                    print(db.fetch_students_in_class(self.class_dropdown_menu.get()))
                    print(db.fetch_enrolments_grouped(cid))


            # Check if class has already been enrolled for subject.
            if db.fetch_enrolments_grouped(cid):
                for enrolment in db.fetch_enrolments_grouped(cid):
                    if enrolment[1] == self.class_dropdown_menu.get() and enrolment[2] == self.subject_dropdown_menu.get():
                        messagebox.showinfo("Enrolment.","This class has been enrolled for the subject.")
                    else:
                        for record in db.fetch_students_in_class(self.class_dropdown_menu.get()):
                            db.insert_enrolment(cid, 2010, record[0], datetime.datetime.now())

            else:
                 for record in db.fetch_students_in_class(self.class_dropdown_menu.get()):
                     db.insert_enrolment(cid, 2010, record[0], datetime.datetime.now())

        else:
            messagebox.showinfo("Selection Incomplete.","Please select class and subject.")
        self.populate_treeview()

'''
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
'''
