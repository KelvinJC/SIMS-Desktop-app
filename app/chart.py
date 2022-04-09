# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 13:44:41 2022

@author: KAIZEN
"""
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from PIL import ImageTk, Image

from widget import Filter

from model.db_sims_sqlite import Database
db = Database('new_single_user3.db')


class Chart(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side='top', fill='both', expand=True)
        self.filter = Filter(self)
        
        self.filter.course_label.destroy() # remove filter course label. Feels strenuous. Find another way. Probably create custom filters for this object
        self.filter.course_dropdown_menu.destroy() # femove filter by course dropdown. Same as above. Find another way.
        
        
        
        holder_frame = tk.Frame(self, pady=15)
        holder_frame.pack(side='top', fill='both', expand=True)
        f = Figure(figsize=(5, 3), dpi=70)
        a = f.add_subplot(111)
        num_males_in_class = db.fetch_student_count_by_gender('SS3', 'Male')[0][0]
        num_females_in_class = db.fetch_student_count_by_gender('SS3', 'Female')[0][0]
       
        gender_distribution = [num_females_in_class, num_males_in_class]
        keys = ['Percentage of female students', 'Percentage of male students',]
        a.pie(gender_distribution, labels = keys, autopct= '%0.0f%%', shadow=True, explode=[0, 0.15], startangle=300, colors=['orange', 'b'])
        
        canvas = FigureCanvasTkAgg(f, holder_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)
               
        
        # Create a holder frame for the pie chart
        pie_chart_frame = tk.Frame(self)
        pie_chart_frame.pack(side='bottom', fill='both', expand=True, pady=(0,26), padx=(0,15))
        # Set figure size and subplot
        f = Figure(figsize=(5, 3), dpi=70)
        a = f.add_subplot(111)
        # Pull data from database
        num_males_in_class = db.fetch_student_count_by_gender('SS3', 'Male')[0][0]
        num_females_in_class = db.fetch_student_count_by_gender('SS3', 'Female')[0][0]
        # Insert data into list
        gender_distribution = [num_females_in_class, num_males_in_class]
        # Create label keys for pie chart
        keys = ['Percentage of female students', 'Percentage of male students',]
        # Plot pie chart
        a.pie(gender_distribution, labels = keys, autopct= '%0.0f%%', shadow=True, explode=[0, 0.15], startangle=300, colors=['orange', 'b'])
        # a.title('Percentage of students by gender') this line gives TypeError: 'Text' object is not callable
        
        canvas = FigureCanvasTkAgg(f, pie_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='left', fill='both', expand=True)
        
       # toolbar = NavigationToolbar2Tk(canvas, root)
       # toolbar.update()
        # canvas._tkcanvas.pack(side='top', fill='both', expand = True)
        
        # Convert data from database to pandas dataframe
        attendance_records = db.fetch_all_attendance() # Pulls the records from attendance table in db. Output is a list of tuples.
        # Cast the list of tuples to a pandas dataframe
        df = pd.DataFrame(attendance_records, columns=['attendance_id', 'course_id', 'student_id', 'date'])
        # Convert date column to date type
        # Use np.where to sort dataframe into Below average attendance, Average/Above average attendance and Perfect attendance. See notes for formulae
        # Plot number of students by attendance grouping
        
        
        # NOTES:
        # I now realise that if you're going to take attendance by course, you will need to know the total number of lessons (or lesson days) in the course
        # I would say now that what is essential is student's name or id and the date of attendance, term and session
        # When records go into session table request number of days or deduct from date begin to date end
        # Ask school principal for such data if building customised db
        # In app, user input of term and session not required since: 
            # Method 1: Dropdown menu has session and term pre-selected
            # Method 2: App makes database query on current term and session
        
        # Could turn current attendance table as it is to course_engagement table. Its own metric

    