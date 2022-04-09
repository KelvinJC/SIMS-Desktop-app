# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 08:55:41 2022

@author: KAIZEN
"""


import tkinter as tk
from tkinter import ttk

from classtreeview import ClassTreeview
from classtreeviewupdate import ClassTreeviewII
from coursetreeview import CourseTreeview
from student_treeview import StudentTreeview
from student_treeview_upload import UploadStudentTreeview
from attendance import Attendance


class NavBar(tk.Frame):
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent, bg = '#394552')

        self.parent = parent
        self.pack(side='left', fill='both', pady=26)
              
        nav_button=tk.Button(self, text='My Courses', width=25, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#394552',
                          command=lambda: self.show_courses())
        nav_button.grid(row=0, column=0, sticky=tk.W, pady=(10, 0), padx=10)
        nav_button=tk.Button(self, text='My Classes', width=25, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#394552', bd=0,
                          command=lambda: self.show_classes())
        nav_button.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        nav_button=tk.Button(self, text='Add/Edit Students', width=25, fg='white', font=("Calibri", 12), bg='#394552', bd=0, anchor=tk.W,
                          command=lambda: self.add_student())
        nav_button.grid(row=2, column=0, sticky=tk.W, padx=30, pady=10)
        nav_button=tk.Button(self, text='Upload Students List', width=25, fg='white', font=("Calibri", 12), bg='#394552', bd=0, anchor=tk.W,
                          command=lambda: self.upload_student())
        nav_button.grid(row=3, column=0, sticky=tk.W, padx=30, pady=10)        
        enroll_button=tk.Button(self, text='Enroll Class', width=25, fg='white', font=("Calibri", 12), bg='#394552', bd=0, anchor=tk.W,
                          command=lambda: self.enroll_class_in_course())
        enroll_button.grid(row=4, column=0, sticky=tk.W, padx=30, pady=10)
        nav_button=tk.Button(self, text='Timetable', width=25, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#394552', bd=0,
                          command=lambda: self.our_command)
        nav_button.grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        nav_button=tk.Button(self, text='Notes', width=25, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#394552', bd=0,
                          command=lambda: self.our_command)
        nav_button.grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)
        nav_button=tk.Button(self, text='Course Engagement', width=25, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#394552', bd=0,
                          command=lambda: self.attendance())
        nav_button.grid(row=7, column=0, sticky=tk.W, padx=10, pady=10)
            
    def show_courses(self):
        # Check if user is already on My Courses. 
        # Use of in operator instead of == operator as caution against prior observation that when a navbar button was selected, 
        # clicking on reloaded frame
        if '.!frame.!dashboard.!coursetreeview' in str(self.parent.winfo_children()[1]): 
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create class treeview frame
            self.parent.treeview = CourseTreeview(self.parent)

    def show_classes(self):
        # Check if user is already on My Classes. 
        # Use of in operator instead of == operator as caution against prior observation that when a navbar button was selected, 
        # clicking on reloaded frame
        if '.!frame.!dashboard.!classtreeview' in str(self.parent.winfo_children()[1]): 
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create class treeview frame
            self.parent.treeview = ClassTreeview(self.parent)
        
    def enroll_class_in_course(self):
        # Same cautionary move as above
        if '.!frame.!dashboard.!classtreeviewii' in str(self.parent.winfo_children()[1]): 
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create add course treeview frame
            self.parent.treeview = ClassTreeviewII(self.parent)
                    
                    # NOTES:
                    # Might have to build another frame that contains in addition to the remaining widgets, a combobox widget for adding courses
                    # self.parent.winfo_children()[1].destroy()
                    # self.parent.treeview = ClassTreeviewWITHcombobox(self.parent)
                    # Or (and this would be fun) create the replacement widget here: hahahahahaha!!! I thought it would not be possible but it just might work
            
    def add_student(self):
        # Same cautionary move as above
        if '.!frame.!dashboard.!studenttreeview' in str(self.parent.winfo_children()[1]): 
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create student treeview frame
            self.parent.treeview = StudentTreeview(self.parent)
        
    def upload_student(self):
        # Same cautionary move as above
        if '.!frame.!dashboard.!uploadstudenttreeview' in str(self.parent.winfo_children()[1]): 
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create student treeview frame
            self.parent.treeview = UploadStudentTreeview(self.parent)
        
    def attendance(self):
        # Same cautionary move as above
        if '.!frame.!dashboard.!attendance' in str(self.parent.winfo_children()[1]): 
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create attendance frame
            self.parent.attendance = Attendance(self.parent)
        
            
        
    
    # Click command
    def our_command(self):
        pass 
        
    