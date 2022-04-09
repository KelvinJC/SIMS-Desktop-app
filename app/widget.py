# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 15:13:04 2022

@author: KAIZEN
"""


import tkinter as tk
from tkinter import ttk

from model.db_sims_sqlite import Database
db = Database('new_single_user3.db')

class Filter(tk.Frame):
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        self.pack(side='left', fill='y')
        
        sess_holder_frame = tk.Frame(self) # wraps around session and course frames to keep them aligned
        sess_holder_frame.pack(side='left', fill='y', pady=26, padx=15)
        
        session_frame = tk.LabelFrame(sess_holder_frame, bg='white', borderwidth=0)
        session_frame.pack(side='top', fill='x', anchor=tk.N)
        
        # Create session dropdown menu
        session_label = tk.Label(session_frame, text="Academic Year", bg='white')
        session_label.grid(row=0,column=0, pady=(10, 20), padx=10, sticky='W')
        self.session_select = tk.StringVar()
        session_dropdown_list = ["Select session"] 
         # Get list of sessions from database
        #db_fetch_session_list = [session[1] for session in db.fetch_session()]
         # Concatenate both lists 
        #session_dropdown_list += db_fetch_session_list
        session_dropdown_menu = ttk.OptionMenu(session_frame, self.session_select, *session_dropdown_list)
        session_dropdown_menu.grid(row=1, column=0, pady=(0,30), padx=10)
        
        # Create term dropdown menu
        term_label=tk.Label(session_frame, text="Term", bg='white')
        term_label.grid(row=2, column=0, pady=(20, 10), padx=10, sticky='W')
        self.term_select = tk.StringVar()
        self.term_dropdown_list = ["Select term", "1", "2", "3"]
        term_dropdown_menu = ttk.OptionMenu(session_frame, self.term_select, *self.term_dropdown_list)
        term_dropdown_menu.grid(row=3, column=0, pady=(5,80), padx=10)
        
        # Create course frame
        course_frame = tk.LabelFrame(sess_holder_frame, bg='white', borderwidth=0)
        course_frame.pack(side='bottom', fill='both', expand=True, pady=(15,0))
        # Create course dropdown menu as attribute of course frame.
        self.course_label = tk.Label(course_frame, text="Course", bg='white')
        self.course_label.grid(row=0,column=0, padx=10, sticky='W')# labeled as self so I can destroy in Chart class when filter is by class
        
        self.course_select = tk.StringVar()
        self.course_dropdown_list = ["Select course"]
        # Get list of courses from database
        db_fetch_course_list = [course[1] + "  " + course[2] for course in db.fetch_course()]
        # Concatenate both lists
        self.course_dropdown_list += db_fetch_course_list
        # Create dropdown menu of courses
        self.course_dropdown_menu = ttk.OptionMenu(course_frame, self.course_select, *self.course_dropdown_list)
        self.course_dropdown_menu.grid(row=1, column=0, pady=(5,30), padx=10) # labeled as self so I can destroy in Chart class when filter is by class
                
        # Create class dropdown menu as attribute of course frame.
        class_label=tk.Label(course_frame, text="Class", bg='white')
        class_label.grid(row=2, column=0, pady=(100,0), padx=10, sticky='W')
        # Initiate class_list variable
        self.class_select = tk.StringVar()
        self.class_list = ['Select Class']
        # Get list of classes from database
        db_fetch_class_list = [class_pick[1] for class_pick in db.fetch_class()]
        # Concatenate both lists
        self.class_list += db_fetch_class_list
        # Create dropdown menu of classes
        self.class_dropdown_menu = ttk.Combobox(course_frame, value=self.class_list, state='readonly')#self.class_select, *self.class_list)
        self.class_dropdown_menu.grid(row=3, column=0, pady=(5,80), padx=10)
        '''
        holder_frame = tk.Frame(self) # wraps around assessment frame
        holder_frame.pack(side='left', fill='both', pady=26)
        
        # Create assessment frame
        assessment_frame = tk.LabelFrame(holder_frame, bg='white', borderwidth=0)
        assessment_frame.pack(side='top',fill='both', expand=True)
        # Create assessment type dropdown menu
        assessment_label = tk.Label(assessment_frame, text="Assessment type", bg='white')
        assessment_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), padx=10, sticky='W')
        # Set assessment variables and create checkboxes
        self.assessment_select = tk.StringVar()
        checkbox1 = ttk.Checkbutton(assessment_frame, text="First test", variable=self.assessment_select, onvalue="First test", offvalue="")
        checkbox1.grid(row=1, column=0, pady=(5,10), padx=10, sticky=tk.W)
        checkbox2 = ttk.Checkbutton(assessment_frame, text="Second test", variable=self.assessment_select, onvalue="Second test", offvalue="")
        checkbox2.grid(row=2, column=0, pady=(5,10), padx=10, sticky=tk.W)
        checkbox3 = ttk.Checkbutton(assessment_frame, text="Third test", variable=self.assessment_select, onvalue="Third test", offvalue="")
        checkbox3.grid(row=3, column=0, pady=(5,10), padx=10, sticky=tk.W)
        checkbox4 = ttk.Checkbutton(assessment_frame, text="Project", variable=self.assessment_select, onvalue="Project", offvalue="")
        checkbox4.grid(row=4, column=0, pady=(5,10), padx=10, sticky=tk.W)      
        checkbox5 = ttk.Checkbutton(assessment_frame, text="Assignment", variable=self.assessment_select, onvalue="Assignment", offvalue="")
        checkbox5.grid(row=5, column=0, pady=(5,10), padx=10, sticky=tk.W)
        checkbox6 = ttk.Checkbutton(assessment_frame, text="Home work", variable=self.assessment_select, onvalue="Home work", offvalue="")
        checkbox6.grid(row=6, column=0, pady=(5,10), padx=10, sticky=tk.W)
        checkbox7 = ttk.Checkbutton(assessment_frame, text="Laboratory", variable=self.assessment_select, onvalue="Laboratry", offvalue="")
        checkbox7.grid(row=7, column=0, pady=(5,10), padx=10, sticky=tk.W)
        checkbox8 = ttk.Checkbutton(assessment_frame, text="Examination", variable=self.assessment_select, onvalue="Examination", offvalue="")
        checkbox8.grid(row=8, column=0, pady=(5,10), padx=10, sticky=tk.W)
        # Set other_assessment variable and combobox
        self.other_assessment_select = tk.StringVar()
        self.other_assessment_list = ["Enter other assessment"]
        other_assessments = ttk.Combobox(assessment_frame, values=self.other_assessment_list, width=25)
        other_assessments.grid(row=9, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W)
        other_assessments.set(self.other_assessment_list[0])
        '''
        