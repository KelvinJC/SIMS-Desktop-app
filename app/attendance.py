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


from widget import Filter
from model.db_sims_sqlite import Database
db = Database('new_single_user3.db')

# Attendance and PresentButton objects communicate with each other. 
# Attendance feeds each student's data into a PresentButton object.
# When clicked, the PresentButton calls appends the student's data to Attendance.log dict attribute. 
# Dictionary since all that's really needed is the last value.
# A list would suit the needs of event logging.


# A Frame object holding and displaying students in a selected class (or course?)
class Attendance(tk.Frame):
    log = {}
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side='top', fill='both', expand=True)
        self.filter = Filter(self)
        self.filter.class_dropdown_menu.bind('<<ComboboxSelected>>', self.show_students)
        
        # Create a frame 
        holder_frame = tk.Frame(self)
        holder_frame.pack(side='top', fill='both', expand=True)
        # Create a canvas
        self.holder_canvas = tk.Canvas(holder_frame)
        self.holder_canvas.pack(side='left', fill='both', expand=True)
        # Create scrollbar. Scrollbar is placed in the holder frame but set to control the canvas
        canvas_scrollbar = ttk.Scrollbar(holder_frame, orient='vertical', command = self.holder_canvas.yview)
        canvas_scrollbar.pack(side='right', fill='y')
        # Configure the canvas with the yscrollcommand
        self.holder_canvas.configure(yscrollcommand=canvas_scrollbar.set)
        self.holder_canvas.bind('<Configure>', lambda e: self.holder_canvas.configure(scrollregion= self.holder_canvas.bbox('all')))
        # Create another frame inside the canvas
        self.inner_frame = tk.Frame(self.holder_canvas)
        # Add that new frame to a window in the canvas
        self.holder_canvas.create_window((0,15), window=self.inner_frame, anchor='nw')
        save_button = ttk.Button(self, text='Save', width = 20, command = lambda: self.store_log_dict())
        self.holder_canvas.create_window((700,50), window=save_button, anchor='nw')
        self.one_more_frame = tk.Frame(self.inner_frame)
        self.one_more_frame.pack(side='top', fill='both', expand=True)
        
        #another_frame = tk.Frame(self)
        #another_frame.pack(side= 'top', fill='x', expand=True)
        #test_button = tk.Button(another_frame, text='Test')
        #test_button.pack()
        
        

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
        attendance_log = reversed(Attendance.log) # So that most recent data returned is first in sequence
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
        print('m')
        self.one_more_frame.destroy()
        
        # Create list of students in selected class
        if self.filter.class_select.get() != 'Select Class':
            self.one_more_frame = tk.Frame(self.inner_frame)
            self.one_more_frame.pack(side='top', fill='both', expand=True)

            self.students_list = [student for student in db.fetch_students_in_class(self.filter.class_select.get())] # remember to replace SS3 with reference to class. .get() function probably
            student_coordinates = self.get_screen_position()
            
        
            # TBD List of students initially displayed should be all students from db.fetch_students
            # Consider a label of "List of students in all classes." UX for clarity and quick understanding
            # Perhaps move the list comprehension generator for a selected class into the get_screen_position function. Get selected class from 'filter'
                    
            for student in student_coordinates:
                # Create a labelframe for each student
                self.student_frame = tk.LabelFrame(self.one_more_frame, bg='white', borderwidth=0)
                self.student_frame.grid(row=student[3], column=student[4], pady=10, padx=10)
                # Add name and class labels
                student_label=tk.Label(self.student_frame, text=student[1] +' '+ student[2], font=('Calibri', 10, 'bold'), bg='white')
                student_label.grid(row=2, column=0, pady=10, padx=10, sticky='W')
                class_label = tk.Label(self.student_frame, text=self.filter.class_select.get(), bg='white') # remember to replace SS3 with reference to class. .get() function probably
                class_label.grid(row=3, column=0, pady=(0, 10), padx=10, sticky='W')
                # Add placeholder for profile photo
                #self.photo_placeholder()
                # Create button frame. To define the border of the button and communicate 'this is a button'
                button_frame = tk.Frame(self.student_frame, bg='#076cf7', borderwidth=1)
                button_frame.grid(row=7, column=0, pady=10,padx=10)
                # Pass in student id as argument while creating an instance of class PresentButton
                click_present = PresentButton(button_frame, student[0])
                click_present.grid() 
        
    def store_log_dict(self):
        '''
        Attendance for a student is recorded per course. Only one attendance record in a course can be stored each day

        '''
        
        
        # Check if data has been stored in attendance log
        if Attendance.log:
            # Confirm course has been selected
            if self.filter.course_select.get() == 'Select course':
                messagebox.showerror('Selection Error', 'Select a course to continue.')
            else:
                # Get the current date
                date = datetime.date.today()
                        # time = datetime.datetime.now().time() for inclusion in course_engagement
                # Get name of course 
                course_name = self.filter.course_select.get()
                # Remove course code from course name
                course_name = course_name.split('  ')[0]
                # Fetch course id from database
                course_id = db.fetch_course_id(course_name)[0][0]
                # Store attendance record
                for student in Attendance.log:
                    db.insert_attendance(course_id, student, date)
                # Remove duplicate records
                db.remove_duplicate_attendance()
                print(db.fetch_all_attendance())

                
            

            
# Create a button which has hover effect and changes colour to indicate it has been clicked. 
# Stores the student's data passed in as arguments for onward tranfer to attendance object
class PresentButton(tk.Button):
    def __init__(self, parent, student_id): # master will become parent ....name, id_number, class_idorname
        tk.Button.__init__(self, parent, width=15, text= "Present",
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
        Attendance.log[self.student_id] = self.log
        print(Attendance.log)
        #print(db.fetch_course_id('Physics')[0][0])
        
    
