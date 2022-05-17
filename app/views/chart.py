# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 13:44:41 2022

@author: KAIZEN
"""

import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

from utils.widget import Filter
from models.database import db


class Chart(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side='top', fill='both', expand=True)
        self.filter = Filter(self)
        self.filter.class_dropdown_menu.bind('<<ComboboxSelected>>', self.show_students_charts)

    def show_students_charts(self, e):
        # Clear holder frame off screen if there's one already to prep for new chart
        try:
            self.holder_frame.pack_forget()
        except AttributeError:
            pass
        # Clear pie frame off screen if there's one already to prep for new chart
        try:
            self.pie_chart_frame.pack_forget()
        except AttributeError:
            pass
        # Create frame to hold chart
        self.holder_frame = tk.Frame(self, pady=15)
        self.holder_frame.pack(side='top', fill='both', expand=True)
        f = Figure(figsize=(5, 3), dpi=70)
        a = f.add_subplot(111)
        # Get data from database
        num_males_in_class = db.fetch_student_count_by_gender(self.filter.class_dropdown_menu.get(), 'Male')[0][0]
        num_females_in_class = db.fetch_student_count_by_gender(self.filter.class_dropdown_menu.get(), 'Female')[0][0]
        #
        gender_distribution = [num_females_in_class, num_males_in_class]
        keys = ['Percentage of female students', 'Percentage of male students',]
        try:
            a.pie(gender_distribution, labels = keys, autopct= '%0.0f%%', shadow=True, explode=[0, 0.15], startangle=300, colors=['orange', '#54aeff'])
            canvas = FigureCanvasTkAgg(f, self.holder_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0)
        except ValueError:
            print('No data from database')

        try:
            # Create a holder frame for the pie chart
            self.pie_chart_frame = tk.Frame(self)
            self.pie_chart_frame.pack(side='bottom', fill='both', expand=True, pady=(0,26), padx=(0,15))
            # Set figure size and subplot
            f = Figure(figsize=(5, 3), dpi=70)
            a = f.add_subplot(111)
            # Pull data from database
            num_males_in_class = db.fetch_student_count_by_gender(self.filter.class_dropdown_menu.get(), 'Male')[0][0]
            num_females_in_class = db.fetch_student_count_by_gender(self.filter.class_dropdown_menu.get(), 'Female')[0][0]
            # Insert data into list
            gender_distribution = [num_females_in_class, num_males_in_class]
            # Create label keys for pie chart
            keys = ['Percentage of female students', 'Percentage of male students',]
            # Plot pie chart
            a.pie(gender_distribution, labels = keys, autopct= '%0.0f%%', shadow=True, explode=[0, 0.15], startangle=300, colors=['orange', '#54aeff'])
            # a.title('Percentage of students by gender') this line gives TypeError: 'Text' object is not callable

            canvas = FigureCanvasTkAgg(f, self.pie_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side='left', fill='both', expand=True)

           # toolbar = NavigationToolbar2Tk(canvas, root)
           # toolbar.update()
            # canvas._tkcanvas.pack(side='top', fill='both', expand = True)
        except ValueError:
            print('No data from database')

        # READ NOTES BELOW!!!


        # Convert data from database to pandas dataframe
        #attendance_records = db.fetch_all_attendance() # Pulls the records from attendance table in db. Output is a list of tuples.
        # Cast the list of tuples to a pandas dataframe
        #df = pd.DataFrame(attendance_records, columns=['attendance_id', 'course_id', 'student_id', 'date'])
        # Convert date column to date type
        # Use np.where to sort dataframe into Below average attendance, Average/Above average attendance and Perfect attendance. See notes for formulae
        # Plot number of students by attendance grouping


        # NOTES:
        # I now realise that if you're going to provide metrics on attendance by course, you will need to know the total number of lessons (or lesson days) in the course
        # I would say now that what is essential is student's name or id and the date of attendance, term and session
        # When records go into session table request number of days or deduct from date begin to date end
        # Ask school principal for such data if building customised db
        # In app, user input of term and session not required since:
            # Method 1: Dropdown menu has session and term pre-selected
            # Method 2: App makes database query on current term and session

        # Could turn current attendance table as it is to course_engagement table. Its own metric
