# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:02:24 2022

@author: KAIZEN
"""
# NOTES:
# I now realise that if you're going to take attendance by course, you will need to know the total number of lessons (or lesson days) in the course
# I would say now that what is essential is student's name or id and the date of attendance, term and session
# When records go into session table request number of days or deduct from date begin to date end
# Ask school principal for such data when building customised db
# In app, user input of term and session not required since:
    # Method 1: Dropdown menu has session and term pre-selected
    # Method 2: App makes database query on current term and session

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime

from utils.widget import Filter, CustomButton
from models.database import db


# Attendance and PresentButton objects communicate with each other.
# Attendance feeds each student's data into a PresentButton object.
# When clicked, the PresentButton calls appends the student's data to Attendance.log dict attribute.
# Dictionary since all that's really needed is the last value.
# A list would suit the needs of event logging.


# A Frame object holding and displaying students in a selected class (or course?)
class LessonAttendance(tk.Frame):
    log = {}
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side='top', fill='both', expand=True)
        self.filter = Filter(self)
        self.filter.class_dropdown_menu.bind('<<ComboboxSelected>>', self.show_students)

    def get_screen_position(self):
        '''
        Generate rows and columns for the placement of each student's display in a grid gallery

        Returns
        A list of tuples where each tuple contains student data concatenated with 2 integers representing the generated row and column
        -------
        '''
        # Count the number of students
        num_students = len(self.students_list)
        # Create a list for 4 columns
        columns = [0, 1, 2, 3]
        # Create the number of rows
        rows = [i for i in range(num_students//4)]
        # Create empty list to hold tuples
        coordinates = []
        # Iterate to generate the tuples. This produces a square matrix. Leaving out the remainder if any
        for i in rows:
            for j in columns:
                a, b = i , j
                coordinates.append((a, b))
        # To handle the remainders if any
        for i in range(num_students % 4):
            a, b = (num_students//4) , i
            coordinates.append((a, b))
        # Concatenate students and coordinates tuples
        student_coord = []
        for i in range((num_students)):
            student_coord.append(self.students_list[i] + coordinates[i])
        return(student_coord)

    #TBD: A fix needed: While the canvas is created in each student, it puts a picture only in last student's frame.
    def photo_placeholder(self):
        # Image import
        self.img = Image.open("images/sims.jpg")
        self.img = self.img.resize((200,100))
        self.img = ImageTk.PhotoImage(self.img, master=self.student_frame) # There is the need to specify the master tk instance since ImageTK is also an instance of tkinter's Tk class
        # Define canvas
        self.my_canvas = tk.Canvas(self.student_frame)
        self.my_canvas.grid(row=4, column=0, rowspan=3, columnspan=2, pady=(0, 10), padx=10, sticky='W')
        # Put the image on the canvas
        self.my_canvas.create_image(0,0, image=self.img, anchor='nw')

    def store_log_list(self):
        '''
        Stores the list of students present in class to database.

        Returns
        -------
        TYPE
            DESCRIPTION.
                Input is a list.
                Intended algorithm for dealing with attendance but I chose store_log_dict instead for its less complex algorithm and lower space complexity.
                An algorithm of this sort would be preferable if intention is to track all clicks made

        '''
        # TBD: Not finished

        # log is a list of tuples (student_id, True) representing the data returned from present button clicks
        attendance_log = reversed(LessonAttendance.log) # So that most recent data returned is first in sequence
        present_students_log = []

        def student_log_search(student_log):
            # Use a linear search on list of present button clicks to determine the most rectent state of 'present button'
            for i in range(0, len(attendance_log)): # Since python keeps track of the length of a list, the len function is a constant time operation
                if attendance_log[i][0] == student_log:
                    return attendance_log[i][1] # returns the first attendance record in the sequence from a linear search of the log which is the last recorded 'present button' click
            return None

        for student in self.students_list:
            present_students_log.append(student_log_search(student))

    def show_students(self, e):
        if self.filter.class_dropdown_menu.get() == 'Select class':
            self.save_button_frame.place_forget()
            #return

        # Create list of students in selected class
        if self.filter.class_dropdown_menu.get() != 'Select class':
            try:
                self.holder_frame.destroy()
            except AttributeError:
                pass


            self.students_list = [student for student in db.fetch_students_in_class(self.filter.class_dropdown_menu.get())] # remember to replace SS3 with reference to class. .get() function probably
            student_coordinates = self.get_screen_position()


            # TBD List of students initially displayed should be all students from db.fetch_students
            # Consider a label of "List of students in all classes." UX for clarity and quick understanding
            # Perhaps move the list comprehension generator for a selected class into the get_screen_position function. Get selected class from 'filter'

            # Create a frame
            self.holder_frame = tk.Frame(self)
            self.holder_frame.pack(side='top', fill='both', expand=True, pady=(0, 30))
            # Create a canvas
            self.holder_canvas = tk.Canvas(self.holder_frame)
            self.holder_canvas.pack(side='left', fill='both', expand=True, pady=(25,0))
            # Create scrollbar. Scrollbar is placed in the holder frame but set to control the canvas
            canvas_scrollbar = ttk.Scrollbar(self.holder_frame, orient='vertical', command = self.holder_canvas.yview)
            canvas_scrollbar.pack(side='right', fill='y')
            # Configure the canvas with the yscrollcommand
            self.holder_canvas.configure(yscrollcommand=canvas_scrollbar.set)
            self.holder_canvas.bind('<Configure>', lambda e: self.holder_canvas.configure(scrollregion= self.holder_canvas.bbox('all')))
            # Create another frame inside the canvas
            self.inner_frame = tk.Frame(self.holder_canvas)
            # Add that new frame to a window in the canvas
            self.holder_canvas.create_window((0,0), window=self.inner_frame, anchor='nw')
            self.save_button_frame = tk.Frame(self, bg='#dedede', borderwidth=1)
            self.save_button_frame.place(x=1080,y=105)
            save_button = CustomButton(self.save_button_frame, 'Save', 20, 1, 12, lambda: self.store_log_dict())
            save_button.grid()
            #self.holder_canvas.create_window((700,50), window=self.save_button, anchor='nw')

            for student in student_coordinates:
                ##
                # Cast tuple to list
                student = list(student)
                # Check if middle name is none then assign null value
                if student[2] is None:
                    student[2] = ''
                # Create a labelframe for each student
                self.student_frame = tk.LabelFrame(self.inner_frame, bg='white', borderwidth=0)
                self.student_frame.grid(row=student[4], column=student[5], pady=(0,15), padx=(0,15))
                # Add name and class labels
                student_lastname_label=tk.Label(self.student_frame, text=student[3], font=('Calibri', 10, 'bold'), bg='white')
                student_lastname_label.grid(row=2, column=0, columnspan = 2, pady=(10,0), padx=5, sticky='W')
                # Check if student has middle name
                if student[2] != '':
                    # Add first name label, initialise middle name. This is a guard against extra long names. An extra-long name would distort the card size
                    student_other_names_label = tk.Label(self.student_frame, text=student[1] +' '+ student[2][0]+'.', font=('Calibri', 10, 'bold'), bg='white')
                    student_other_names_label.grid(row=3, column=0, columnspan = 2, pady=(0,10), padx=10, sticky='W')
                else:
                    student_other_names_label = tk.Label(self.student_frame, text=student[1] +' '+ student[2], font=('Calibri', 10, 'bold'), bg='white')
                    student_other_names_label.grid(row=3, column=0, columnspan = 2, pady=(0,10), padx=10, sticky='W')
                class_label = tk.Label(self.student_frame, text=self.filter.class_dropdown_menu.get(), bg='white')
                class_label.grid(row=4, column=0, pady=(0, 10), padx=(10,25), sticky='W')
                # Add placeholder for profile photo
                #self.photo_placeholder()
                # Create button frame. To define the border of the button and communicate 'this is a button'
                button_frame = tk.Frame(self.student_frame, bg='#076cf7', borderwidth=1)
                button_frame.grid(row=4, column=1, pady=20,padx=10)
                # Pass in student id as argument while creating an instance of class PresentButton
                click_present = PresentButton(button_frame, student[0])
                click_present.grid()

    def store_log_dict(self):
        '''
        Attendance for a student is recorded per subject lesson. Only one attendance record can be stored each day. Duplicate records are deleted.

        '''



        # Check if data has been stored in attendance log
        if LessonAttendance.log:
            # Confirm course has been selected
            if self.filter.subject_dropdown_menu.get() == 'Select subject':
                messagebox.showerror('Selection Error', 'Select a subject to continue.')
            else:
                # Get the current date
                date = datetime.date.today() # or get it from placing a DateEntry calendar in filter. Could be used for generating multiple date attendance data for analytics charts
                time = datetime.datetime.now().time() #for inclusion in course_engagement now known as lesson attendance
                # Get name of subject
                subject_name = self.filter.subject_dropdown_menu.get()
                # Fetch subject id from database
                subject_id = db.fetch_subject_id(subject_name)[0][0]
                # Store attendance record
                for student in LessonAttendance.log:
                    print(student) # check value of student
                    #db.insert_attendance(term_id, subject_id, student, date, time)
                # Remove duplicate records
                db.remove_duplicate_attendance()
                print(db.fetch_all_attendance())
                messagebox.showinfo("", "Attendance saved!")

        else:
            # Notify user to select subject and select present students
            messagebox.showinfo("", "First select a subject.\n\n Then for every student who is present for the lesson, click 'Present'.")
            return

    def our_command(self):
        pass



# Create a button which has hover effect and changes colour to indicate it has been clicked.
# Stores the student's data passed in as arguments for onward tranfer to attendance object
class PresentButton(tk.Button):
    def __init__(self, parent, student_id): # master will become parent ....name, id_number, class_idorname
        tk.Button.__init__(self, parent, width=12, text= "Present",
                                           font=('Calibri', 12, 'bold'),
                                           fg='#076cf7',
                                           bg='white',
                                           border=0,
                                           activeforeground='#f1f1f1',
                                           activebackground='#54aeff',
                                           command=lambda: self.return_log()
                                           )
        #self.place(x=20, y=20)
        self.parent = parent
        # Bind button to enter event
        self.bind('<Enter>', lambda e: self.on_enter('#54aeff', '#f1f1f1'))
        # Bind button to leave event
        self.bind('<Leave>', lambda e: self.on_leave('#076cf7', 'white'))
        # Bind button to click event
        self.bind('<ButtonRelease-1>', lambda e: self.on_click('white', '#076cf7'))

        # Store student data as an attribute
        self.student_id = student_id
        # Create log variable to keep track of button's state
        self.log = False

    def on_enter(self, bcolor, fcolor):
        # Changes button's colour when mouse enters the button
        if self['background']=='#076cf7': # To check if button has been clicked. Here, a clicked button does not change
            return
        else:
            self['background']=bcolor
            self['foreground']=fcolor

    def on_leave(self, bcolor, fcolor):
        # Changes button's colour when mouse leaves the button
        if self['background']=='#076cf7': # To check if button has been clicked. Here, a clicked button does not change
            return
        else:
            self['background']=fcolor
            self['foreground']=bcolor

    def on_click(self, bcolor, fcolor):
        """ Changes button's colour when mouse clicks the button.
            Changes the value of a variable 'log' to reflect student's presence or absence in class """

        if self['background'] == '#076cf7': # To check if button has already been clicked. Here, a clicked button changes to unclicked state
            self['background']=bcolor
            self['foreground']=fcolor
            # self.log = (student_id, class, False) # This indicates student is absent
            self.log = False
        else:
            self['background'] = '#076cf7'
            self['foreground'] = 'white'
            # self.log = (student_id, class, True) # This indicates student is present
            self.log = True

    def return_log(self):
        # The following applies when a list is used to log state

        #print(self.log)
        #Attendance.log.append(self.log)
        #print(Attendance.log)

        print(self.log)
        LessonAttendance.log[self.student_id] = self.log
        print(LessonAttendance.log)
        #print(db.fetch_course_id('Physics')[0][0])
