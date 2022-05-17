# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 08:55:41 2022

@author: KAIZEN
"""



import tkinter as tk
from tkinter import ttk

from .classes import MyClasses
from .class_enrol import EnrolClass
from .subjects import MySubjects
from .edit_students import EditStudents
from .upload_students import UploadStudentsList
from .attendance import LessonAttendance
from .session import NewSession, NewTerm

class NavBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = '#111827')

        self.parent = parent
        self.pack(side='left', fill='both', pady=26)


        btn1=tk.Button(self, text='My Subjects', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#111827', bd=0,
                          command=lambda: self.show_subjects())
        btn1.grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        btn2=tk.Button(self, text='My Classes', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#111827', bd=0,
                          command=lambda: self.show_classes())
        btn2.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        btn3=tk.Button(self, text='Add/Edit Students', width=20, fg='white', font=("Calibri", 12), bg='#111827', bd=0, anchor=tk.W,
                          command=lambda: self.edit_student())
        btn3.grid(row=2, column=0, sticky=tk.W, padx=30, pady=10)
        btn4=tk.Button(self, text='Upload Students List', width=20, fg='white', font=("Calibri", 12), bg='#111827', bd=0, anchor=tk.W,
                          command=lambda: self.upload_student())
        btn4.grid(row=3, column=0, sticky=tk.W, padx=30, pady=10)
        enroll_button=tk.Button(self, text='Enroll Class', width=20, fg='white', font=("Calibri", 12), bg='#111827', bd=0, anchor=tk.W,
                          command=lambda: self.enroll_class_in_subject())
        enroll_button.grid(row=4, column=0, sticky=tk.W, padx=30, pady=10)
        nav_button=tk.Button(self, text='Notes', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#111827', bd=0,
                          command=lambda: self.our_command)
        nav_button.grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        nav_button=tk.Button(self, text='Lesson Attendance', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#111827', bd=0,
                          command=lambda: self.attendance())
        nav_button.grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)


    def show_session(self):
        # Check if user is already on My Calendar.
        # Use of in operator instead of == operator as caution against prior observation that when a navbar button was selected,
        # clicking on reloaded frame
        if '.!frame.!dashboard.!newsession' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create     frame
            self.parent.view = NewSession(self.parent)

    def show_term(self):
        # Check if user is already on My Calendar.
        # Use of in operator instead of == operator as caution against prior observation that when a navbar button was selected,
        # clicking on reloaded frame
        if '.!frame.!dashboard.!newterm' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create     frame
            self.parent.view = NewTerm(self.parent)

    def show_subjects(self):
        # Check if user is already on My Subjects.
        # Use of in operator instead of == operator as caution against prior observation that when a navbar button was selected,
        # clicking on reloaded frame
        if '.!frame.!dashboard.!mysubjects' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create class treeview frame
            self.parent.view = MySubjects(self.parent)

    def show_classes(self):
        # Check if user is already on My Classes.
        # Use of in operator instead of == operator as caution against prior observation that when a navbar button was selected,
        # clicking on reloaded frame
        if '.!frame.!dashboard.!myclasses' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create class treeview frame
            self.parent.view = MyClasses(self.parent)

    def enroll_class_in_subject(self):
        # Same cautionary move as above
        if '.!frame.!dashboard.!enrolclass' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create add course treeview frame
            self.parent.view = EnrolClass(self.parent)

                    # NOTES:
                    # Might have to build another frame that contains in addition to the remaining widgets, a combobox widget for adding courses
                    # self.parent.winfo_children()[1].destroy()
                    # self.parent.treeview = ClassTreeviewWITHcombobox(self.parent)
                    # Or (and this would be fun) create the replacement widget here: hahahahahaha!!! I thought it would not be possible but it just might work

    def edit_student(self):
        # Same cautionary move as above
        if '.!frame.!dashboard.!editstudents' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create student treeview frame
            self.parent.view = EditStudents(self.parent)

    def upload_student(self):
        # Same cautionary move as above
        if '.!frame.!dashboard.!uploadstudentslist' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create student treeview frame
            self.parent.view = UploadStudentsList(self.parent)

    def attendance(self):
        # Same cautionary move as above
        if '.!frame.!dashboard.!attendance' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create attendance frame
            self.parent.view = LessonAttendance(self.parent)




    # Click command
    def our_command(self):
        pass
