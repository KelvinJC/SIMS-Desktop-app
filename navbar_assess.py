# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 08:55:41 2022

@author: KAIZEN
"""

import tkinter as tk
from tkinter import ttk

from assessments import AssessmentTreeview, AssessmentCombined
from widget import Filter

class NavBarAssessment(tk.Frame):
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent, bg = '#394552')

        self.parent = parent
        self.pack(side='left', fill='both', pady=26)
              
        nav_button=tk.Button(self, text='Assessments', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#394552',
                          command=lambda: self.show_assessments())
        nav_button.grid(row=0, column=0, sticky=tk.W, pady=(10, 0), padx=10)
        
        nav_button=tk.Button(self, text='Create Assessments', width=20, bg='#394552', bd=0, fg='white', font=('Calibri', 12), anchor=tk.W,
                          command=lambda: self.create_assessment())
        nav_button.grid(row=1, column=0, sticky=tk.W, padx=30, pady=10)
        nav_button=tk.Button(self, text='Record Assessments', width=20, bg='#394552', fg='white', bd=0, font=('Calibri', 12), anchor=tk.W,
                          command=lambda: self.enroll())
        nav_button.grid(row=2, column=0, sticky=tk.W, padx=30, pady=10)        
        enroll_button=tk.Button(self, text='Evaluation', width=20, bg='#394552', bd=0, fg='white', font=('Calibri', 12), anchor=tk.W,
                          command=lambda: self.our_command)
        enroll_button.grid(row=3, column=0, sticky=tk.W, padx=30, pady=10)
        nav_button=tk.Button(self, text='Emotional Quotient', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#394552', bd=0,
                          command=lambda: self.our_command)
        nav_button.grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        nav_button=tk.Button(self, text='Notes', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#394552', bd=0,
                          command=lambda: self.our_command)
        nav_button.grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        nav_button=tk.Button(self, text='Reports', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#394552', bd=0,
                          command=lambda: self.our_command)
        nav_button.grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)
            
    def show_assessments(self):
        '''
        Clear widgets currently on screen so as to display new widgets
        '''          
        # Check if user is already on Assessments. 
        # Use of in operator instead of == operator as caution against prior observation that when a course/class was selected, 
        # clicking on assessments reloaded frame
        
        if '.!frame.!dashboard.!assessmentcombined' in str(self.parent.winfo_children()[1]): 
            return
        else:
            for widget in self.parent.winfo_children():
                if '.!navbarassessment' not in repr(widget): # To avoid deleting the navbar widget
                    # Clear all widgets off screen
                    widget.destroy()
            # Create assess frame and assessment treeview as attributes of navbar's parent object i.e Dashboard
            self.parent.assess_frame = AssessmentCombined(self.parent)
            self.parent.treeview = AssessmentTreeview(self.parent)
            
    def create_assessment(self):
        '''
        Clear widgets currently on screen so as to display new widgets          
        '''
        # Check if user is already on Create Assessments. 
        # Use of in operator instead of == operator as caution against prior observation that when a course/class was selected, 
        # clicking on create assessments reloaded the frame
        
        if '.!frame.!dashboard.!filter' in str(self.parent.winfo_children()[1]): 
            return
        else:
            for widget in self.parent.winfo_children():
                if '.!navbarassessment' not in repr(widget): # To avoid deleting the navbar widget
                    # Clear all widgets off screen
                    widget.destroy()
            # Create 'create_assessment' frame as an attribute of navbar's parent object i.e Dashboard
            self.parent.filter_frame = Filter(self.parent)
            self.parent.treeview = AssessmentTreeview(self.parent)
            # Remove searchbox
            #self.parent.treeview.search_box.destroy()
            # Override tree_frame pack function. Polymorphism. Ha!
           # self.parent.treeview.tree_frame.pack(side=tk.RIGHT, fill=tk.Y, pady=(26,0))
     
    def enroll(self):
        pass
        
    def add_student(self):
        # Clear off whichever frame is currently displayed
        self.parent.winfo_children()[1].destroy()
        # Create student treeview frame
        self.parent.treeview = StudentTreeview(self.parent)
    
    def upload_student(self):
        # Clear off whichever frame is currently displayed
        self.parent.winfo_children()[1].destroy()
        # Create student treeview frame
        self.parent.treeview = UploadStudentTreeview(self.parent)
    
    # Click command
    def our_command(self):
        pass 
        

    