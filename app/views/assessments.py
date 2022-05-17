# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 09:31:19 2022

@author: KAIZEN
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from PIL import ImageTk, Image

from utils.widget import Filter
from models.database import db

class Assessments(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.pack(side='top', fill='both', expand=True)
        self.filter = Filter(self)
        self.filter.class_dropdown_menu.bind('<<ComboboxSelected>>', self.populate_treeview)
        self.filter.subject_dropdown_menu.bind('<<ComboboxSelected>>', self.populate_treeview)

        # Create dropdown menu of assessments
        self.assessment_dropdown_list = ["Select assessment", "First test", "Second test", "Third test", "Project", "Assignment", "Homework", "Laboratory", "Examination"]

        self.assessment_dropdown_menu = ttk.Combobox(self.filter.holder_frame, value=self.assessment_dropdown_list, width=30, state='readonly')
        self.assessment_dropdown_menu.grid(row=10, column=0, pady=(100,5), padx=10)
        self.assessment_dropdown_menu.current(0)
        self.assessment_dropdown_menu.bind('<<ComboboxSelected>>', self.populate_treeview)

        # Create class dropdown menu as attribute of subject frame.

        # Add Search Box (Rememeber to implement 'Search' showing in bar )
        self.search_box = tk.Entry(self, width=60)
        self.search_box.pack(pady=4, padx=2, anchor=tk.NE)

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
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.X, anchor=tk.N)

        # Treeview Scrollbar
        tree_scroll = tk.Scrollbar(self.tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=(2,0))

        # Create Treeview
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended', height=25)
        # Pack to the screen
        self.my_tree.pack(fill=tk.X)

        # Configure scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Define our columns. Reserve two extra null columns for subsequent child rows i.e student first and last names
        self.my_tree['columns'] = ('ID', 'R.Id', 'First name', 'Middle name', 'Last name', 'Class', 'Subject', 'Assessment', 'Score')

        # Format our columns
        self.my_tree.column("#0", stretch=tk.NO, width=0)
        self.my_tree.column("ID", anchor=tk.CENTER, stretch=tk.NO, width=0)
        self.my_tree.column("R.Id", anchor=tk.W, stretch=tk.NO, width=30)
        self.my_tree.column("First name", anchor=tk.W, width=200)
        self.my_tree.column("Middle name", anchor=tk.W, width=150)
        self.my_tree.column("Last name", anchor=tk.W, width=200)
        self.my_tree.column("Class", anchor=tk.W, width=50)
        self.my_tree.column("Subject", anchor=tk.W, width=200)
        self.my_tree.column("Assessment", anchor=tk.W, width=100)
        self.my_tree.column("Score", anchor=tk.W, width=800)

        # Create Column headings
        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading("R.Id", text="R.Id", anchor=tk.W)
        self.my_tree.heading("First name", text="First name", anchor=tk.W)
        self.my_tree.heading("Middle name", text="Middle name", anchor=tk.W)
        self.my_tree.heading("Last name", text="Last name", anchor=tk.W)
        self.my_tree.heading("Class", text="Class", anchor=tk.W)
        self.my_tree.heading("Subject", text="Subject", anchor=tk.W)
        self.my_tree.heading("Assessment", text="Assessment", anchor=tk.W)
        self.my_tree.heading("Score", text="Score", anchor=tk.W)

        # Create striped Treeview rows
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="#f3f3f4")

        # Create data entry frame
        entry_frame = tk.Frame(self) # wraps around entries labelframe
        entry_frame.pack(side='top', fill='both', expand=True, pady=(15,26))
        entries_label_frame = tk.LabelFrame(entry_frame, bg='white', borderwidth=0)
        entries_label_frame.pack(side='top',fill='both', expand=True)

        # Data entry widgets: Labels & entries
        name_label = tk.Label(entries_label_frame, text="Name", bg='#ffffff')
        name_label.grid(row=0, column=0, pady=(10,0), padx=5, sticky=tk.W)
        n_entryframe = tk.Frame(entries_label_frame, bg='#dedede', borderwidth=1)
        n_entryframe.grid(row=0, column=1, pady=(10,0), padx=5)
        self.first_name_entry = tk.Entry(n_entryframe, text=name_label, width=50, bg='#f1f1f1', bd=0)
        self.first_name_entry.grid()

        score_label = tk.Label(entries_label_frame, text="Score", bg='#ffffff')
        score_label.grid(row=1, column=0, padx=5, sticky=tk.W)
        # Place frame around entrybox
        s_entryframe = tk.Frame(entries_label_frame, bg='#dedede', borderwidth=1)
        s_entryframe.grid(row=1, column=1, padx=5, sticky='W')
        self.score_entry = tk.Entry(s_entryframe, text=score_label, width=10, bg='#f1f1f1', bd=0)
        self.score_entry.grid()

        # Add Buttons
        add_button = ttk.Button(entries_label_frame, text="Add Score", command= lambda: self.add_record(), width=42)
        add_button.grid(row=0, column=3, padx=10,  pady=(10,5), columnspan=2)

        update_button = ttk.Button(entries_label_frame, text="Update Score", command= lambda: self.update_record(), width=19)
        update_button.grid(row=1, column=3, padx=1, pady=5)

        remove_one_button = ttk.Button(entries_label_frame, text="Remove Score", command=lambda: self.remove_record(), width=19)
        remove_one_button.grid(row=1, column=4, padx=1, pady=5)

        current_session_label = tk.Label(entries_label_frame, text="Current session", bg='#ffffff')
        current_session_label.grid(row=2, column=0, pady=(10,0), padx=5, sticky=tk.W)
        self.current_session_entry = tk.Entry(entries_label_frame, text='First session', width=30, bg='#dedede', bd=0)
        self.current_session_entry.grid(row=2, column=1, pady=(10,0), padx=5, sticky=tk.W)

        current_term_label = tk.Label(entries_label_frame, text="Current term", bg='#ffffff')
        current_term_label.grid(row=3, column=0, pady=(10,0), padx=5, sticky=tk.W)
        self.current_term_entry = tk.Entry(entries_label_frame, text=current_term_label, width=30, bg='#dedede', bd=0)
        self.current_term_entry.grid(row=3, column=1, pady=(10,0), padx=5, sticky=tk.W)

        # Set other_assessment variable and combobox
        self.other_assessment_select = tk.StringVar()
        self.other_assessment_list = ["Enter other assessment"]
        other_assessments = ttk.Combobox(entries_label_frame, values=self.other_assessment_list, width=25)
        other_assessments.grid(row=1, column=2, pady=10, padx=10, sticky=tk.W)
        other_assessments.set(self.other_assessment_list[0])

        # TBD:
        # Add validation for assessment entry to prevent multiple records in the same assessment
        # msg showbox error, this student already has a record in first test. To change the record, click Update the record instead

    def populate_treeview(self, e):
        if self.filter.class_dropdown_menu.get() != 'Select class' and self.filter.subject_dropdown_menu.get() != 'Select subject' \
        and self.assessment_dropdown_menu.get() != 'Select assessment':
            # Assign filter selections to variables
            class_select = self.filter.class_dropdown_menu.get()
            subject_select = self.filter.subject_dropdown_menu.get()
            assessment_select = self.assessment_dropdown_menu.get()
            # Clear tree currently in view
            self.my_tree.delete(*self.my_tree.get_children())
            # Create counter (Treeview stripes)
            count = 0
            # Loop through records from database
            for student in db.fetch_students_in_class(self.filter.class_dropdown_menu.get()):
                # Cast tuple to list to prepare for is_None middle name assignment
                student = list(student)
                # Check if middle name is None
                if student[2] is None:
                    student[2] = ''
                if count % 2 == 0: # To shade treeview correctly
                    # Insert records into treeview
                    self.my_tree.insert(parent="",
                                        index="end",
                                        iid=count,
                                        values=(student[0], count+1, student[1], student[2], student[3], # student[0] = student_id 'from database', student[1]= student_first_name
                                                class_select, subject_select, assessment_select),
                                        tags=("evenrow",))
                else:
                    self.my_tree.insert(parent="",
                                        index="end",
                                        iid=count,
                                        values=(student[0], count+1, student[1], student[2], student[3], # student[0] = student_id 'from database', student[1]= student_first_name
                                                class_select, subject_select, assessment_select),
                                        tags=("oddrow",))
                count += 1
        else:
            self.my_tree.delete(*self.my_tree.get_children())





    #    def






class AssessmentCombined(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.pack(side='left', fill='both', expand=True)

        holder_frame = tk.Frame(self) # wraps around session and assessment frames to keep them aligned
        holder_frame.pack(side='left', fill='both', pady=26, padx=(17,0))

        subject_frame = tk.LabelFrame(holder_frame, bg='white', borderwidth=0)
        subject_frame.pack(side='top', fill='x', anchor=tk.N)

        # Create subject dropdown menu as attribute of subject frame.
        subject_label = tk.Label(subject_frame, text="Subject", bg='white')
        subject_label.grid(row=0,column=0, padx=10, sticky='W')

        self.subject_select = tk.StringVar()
        self.subject_dropdown_list = ["Select subject"]
        # Get list of subjects from database
        db_fetch_subject_list = [subject[1] for subject in db.fetch_subject()]
        # Concatenate both lists
        self.subject_dropdown_list += db_fetch_subject_list
        # Create dropdown menu of subjects
        subject_dropdown_menu = ttk.OptionMenu(subject_frame, self.subject_select, *self.subject_dropdown_list)
        subject_dropdown_menu.grid(row=1, column=0, pady=(5,30), padx=10)

        # Create class dropdown menu as attribute of subject frame.
        class_label=tk.Label(subject_frame, text="Class", bg='white')
        class_label.grid(row=2, column=0, pady=(20,0), padx=10, sticky='W')
        # Initiate class_list variable
        self.class_select = tk.StringVar()
        self.class_list = ['Select Class']
        # Get list of classes from database
        db_fetch_class_list = [class_pick[1] for class_pick in db.fetch_class()]
        # Concatenate both lists
        self.class_list += db_fetch_class_list
        # Create dropdown menu of classes
        class_dropdown_menu = ttk.OptionMenu(subject_frame, self.class_select, *self.class_list)
        class_dropdown_menu.grid(row=3, column=0, pady=(5,80), padx=10)

        # Create assessment frame
        assessment_frame = tk.LabelFrame(holder_frame, bg='white', borderwidth=0)
        assessment_frame.pack(side='bottom',fill='both', expand=True, pady=(15,0))
        # Create assessment type dropdown menu
        assessment_label = tk.Label(assessment_frame, text="Assessment type", bg='white')
        assessment_label.grid(row=3, column=0, columnspan=2, pady=(40, 20), padx=10, sticky='W')
        self.assessment_select = tk.StringVar()
        self.assessment_list = ["Select assessment"]
        assessment_dropdown_menu = ttk.OptionMenu(assessment_frame, self.assessment_select, *self.assessment_list)
        assessment_dropdown_menu.grid(row=4, column=0, columnspan=2, pady=(5,10), padx=10)

        self.assessment_select1 = tk.StringVar()
        self.assessment_list1 = ["Select assessment"]
        assessment_dropdown_menu1 = ttk.OptionMenu(assessment_frame, self.assessment_select1, *self.assessment_list1)
        assessment_dropdown_menu1.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

        self.assessment_select2 = tk.StringVar()
        self.assessment_list2 = ["Select assessment"]
        assessment_dropdown_menu2 = ttk.OptionMenu(assessment_frame, self.assessment_select2, *self.assessment_list2)
        assessment_dropdown_menu2.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

        self.assessment_select3 = tk.StringVar()
        self.assessment_list3 = ["Select assessment"]
        assessment_dropdown_menu3 = ttk.OptionMenu(assessment_frame, self.assessment_select3, *self.assessment_list3)
        assessment_dropdown_menu3.grid(row=7, column=0, columnspan=2, pady=10, padx=10)

        self.assessment_select4 = tk.StringVar()
        self.assessment_list4 = ["Select assessment"]
        assessment_dropdown_menu4 = ttk.OptionMenu(assessment_frame, self.assessment_select4, *self.assessment_list4)
        assessment_dropdown_menu4.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

        score= tk.Label(assessment_frame, text="Score", bg='white')
        score.grid(row=3, column=3, padx=20, pady=(40, 20))
        score_box = tk.Entry(assessment_frame, text=score, width=15, borderwidth=0, bg='#f3f3f4')
        score_box.grid(row=4, column=3, pady=(0,10), padx=20)
        score_box1 = tk.Entry(assessment_frame, text=score, width=15, borderwidth=0, bg='#f3f3f4')
        score_box1.grid(row=5, column=3, pady=10, padx=20)
        score_box2 = tk.Entry(assessment_frame, text=score, width=15, borderwidth=0, bg='#f3f3f4')
        score_box2.grid(row=6, column=3, pady=10, padx=20)
        score_box3 = tk.Entry(assessment_frame, text=score, width=15, borderwidth=0, bg='#f3f3f4')
        score_box3.grid(row=7, column=3, pady=10, padx=20)
        score_box4 = tk.Entry(assessment_frame, text=score, width=15, borderwidth=0, bg='#f3f3f4')
        score_box4.grid(row=8, column=3, pady=10, padx=20)

        # Add photo # Will make much smaller. Perhaps with an icon on the button rather than words. Icon-ed may still need label beside it tho
        add_photo_button = ttk.Button(assessment_frame, text="Add Photo", command=lambda: self.add_profile_picture(), width=15)
        add_photo_button.grid(row=2, column=3, padx=10, pady=20)

    def add_profile_picture(self):
        '''
        Add an image file from PC as profile picture
        Returns
        -------
        None.

        '''
        filename = filedialog.askopenfilename(
            initialdir = "C:/Documents",
            title = "Open A File",
            filetype = (("jpeg files", "*.jpg"), ("png files", "*.png"))
            )
        if filename:
            try:
                filename = r"{}".format(filename)
                self.img = Image.open(filename)
                self.img = self.img.resize((58,48))
                # There is the need to specify the master tk instance since ImageTK is a second instance of tkinter
                self.img = ImageTk.PhotoImage(self.img, master=self)

            except(ValueError):
                messagebox.showerror("File Error", "File could not be opened... try again!")
            except FileNotFoundError:
                messagebox.showerror("File Error", "File could not be found... try again!")

        # Define canvas
        self.my_canvas = tk.Canvas(self.assessment_frame, width=60, height=50)
        self.my_canvas.grid(row=0, column = 0, rowspan=2, pady=5, padx=10)
        # Put the image on the canvas
        self.my_canvas.create_image(0,0, image=self.img, anchor='nw')
