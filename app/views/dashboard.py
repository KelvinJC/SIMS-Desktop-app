# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 12:48:43 2022

@author: KAIZEN
"""

import tkinter as tk
import pandas as pd
from tkinter import ttk, filedialog
from PIL import ImageTk, Image

from .navbar import NavBar
from .navbar_assess import NavBarAssessment
from .navbar_analytics import NavBarAnalytics
from .navbar_cal import NavBarCal
from .subjects import MySubjects
from .assessments import Assessments, AssessmentCombined
from .attendance import LessonAttendance
from .chart import Chart
from .session import NewSession

from utils.widget import Filter, BlueButton


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.parent = parent

        holder_frame = tk.Frame(self)
        holder_frame.pack(side='top', fill='both', expand=True)

        # Image import
        img = Image.open("images/login.jpg")
        img = img.resize((self.winfo_screenwidth(),self.winfo_screenheight()))

        # There is the need to specify the master tk instance since ImageTK is also an instance of tkinter's Tk class
        self.img = ImageTk.PhotoImage(img, master=holder_frame)
        # Define canvas
        self.my_canvas = tk.Canvas(holder_frame, bg='#e4e4e4') # , bg = 'black'
        self.my_canvas.pack(side='top', fill='both', expand=True)
        # Put the image on the canvas
        #self.my_canvas.create_image(0,0, image=self.img, anchor='nw')
        # Add labels
        self.my_canvas.create_text(210, 15, text = 'Go Anywhere you choose!', font=("Calibri", 21, 'bold italic'), fill='white', anchor='nw')

        # Menu frame 1
        rec_btn_frame = tk.Frame(holder_frame)
        rec_btn = BlueButton(holder_frame, 'My Notes', 15, 1, 14, lambda: self.open_courses())
        rec_img1 = Image.open("images/teacher.jpg")
        rec_img1 = rec_img1.resize((500,200))
        self.rec_img1 = ImageTk.PhotoImage(rec_img1, master=rec_btn_frame)
        # Define canvas
        rec_canvas = tk.Canvas(rec_btn_frame)
        rec_canvas.pack(side='top', fill='both', expand=True)
        rec_canvas.create_window(0,250, anchor='sw', window=rec_btn)
        # Put the image on the canvas
        rec_canvas.create_image(0,0, image=self.rec_img1, anchor='nw')
        rec_btn_window = self.my_canvas.create_window(90, 90, anchor= 'nw', window=rec_btn_frame)

        # Menu frame 2
        rec_btn_frame = tk.Frame(holder_frame)
        # ---- Change back to tk.Button, remove BlueButton from widgets. No need for it!!
        rec_btn = BlueButton(holder_frame, 'Reports', 15, 1, 14, lambda: self.open_courses())
        rec_img2 = Image.open("images/dgrey.jpg")
        rec_img2 = rec_img2.resize((500,200))
        self.rec_img2 = ImageTk.PhotoImage(rec_img2, master=rec_btn_frame)
        # Define canvas
        rec_canvas = tk.Canvas(rec_btn_frame)
        rec_canvas.pack(side='top', fill='both', expand=True)
        rec_canvas.create_window(0,250, anchor='sw', window=rec_btn)
        # Put the image on the canvas
        rec_canvas.create_image(0,0, image=self.rec_img2, anchor='nw')
        rec_btn_window = self.my_canvas.create_window(580, 90, anchor= 'nw', window=rec_btn_frame)

        # Menu frame 3
        rec_btn_frame = tk.Frame(holder_frame)
        rec_btn = BlueButton(holder_frame, 'Notifications', 15, 1, 14, lambda: self.open_courses())
        rec_img3 = Image.open("images/coco.jpg")
        rec_img3 = rec_img3.resize((500,200))
        self.rec_img3 = ImageTk.PhotoImage(rec_img3, master=rec_btn_frame)
        # Define canvas
        rec_canvas = tk.Canvas(rec_btn_frame)
        rec_canvas.pack(side='top', fill='both', expand=True)
        rec_canvas.create_window(0,0, anchor='nw', window=rec_btn)
        # Put the image on the canvas
        rec_canvas.create_image(0,0, image=self.rec_img3, anchor='nw')
        rec_btn_window = self.my_canvas.create_window(1070, 90, anchor= 'nw', window=rec_btn_frame, height=600)

        # Menu frame 4
        rec_btn_frame = tk.Frame(holder_frame)
        rec_btn = BlueButton(holder_frame, 'My Calendar', 15, 1, 14, lambda: self.open_calendar())
        rec_img4 = Image.open("images/timetable.jpg")
        rec_img4 = rec_img4.resize((500,200))
        self.rec_img4 = ImageTk.PhotoImage(rec_img4, master=rec_btn_frame)
        # Define canvas
        rec_canvas = tk.Canvas(rec_btn_frame)
        rec_canvas.pack(side='top', fill='both', expand=True)
        rec_canvas.create_window(0,250, anchor='sw', window=rec_btn)
        # Put the image on the canvas
        rec_canvas.create_image(0,0, image=self.rec_img4, anchor='nw')
        rec_btn_window = self.my_canvas.create_window(90, 420, anchor= 'nw', window=rec_btn_frame)

        # Menu frame 5
        rec_btn_frame = tk.Frame(holder_frame)
        rec_btn = BlueButton(holder_frame, 'Grade Book', 15, 1, 14, lambda: self.open_assessments())
        rec_img5 = Image.open("images/login.jpg")
        rec_img5 = rec_img5.resize((500,200))
        self.rec_img5 = ImageTk.PhotoImage(rec_img5, master=rec_btn_frame)
        # Define canvas
        rec_canvas = tk.Canvas(rec_btn_frame)
        rec_canvas.pack(side='top', fill='both', expand=True)
        rec_canvas.create_window(0,250, anchor='sw', window=rec_btn)
        # Put the image on the canvas
        rec_canvas.create_image(0,0, image=self.rec_img5, anchor='nw')
        rec_btn_window = self.my_canvas.create_window(580, 420, anchor= 'nw', window=rec_btn_frame)


    def get_name(self):
        # check if login username entry matches username and if login password entry matches password
        with open("env", "r") as file:
            file_data = file.read()

        file_data = file_data.split('\n')
        self.name = file_data[0].title()
        return self.name

    def menubar(self, root):
        # Just so this frame doesn't show a menu bar
        menubar = tk.Menu(root)
        return(menubar)

    def ex_menubar(self, controller):
        menubar = tk.Menu(controller)

        # Create a menu item (Set tearoff  to false to disable detachable submenu)
        fileMenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open", command=lambda: self.file_open())
        fileMenu.add_separator()
        fileMenu.add_command(label="Open last closed", command=self.our_command)
        fileMenu.add_command(label="Open folder", command=self.our_command)

        # Create Edit menu
        editMenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Edit", menu=editMenu)
        # Edit menu items
        editMenu.add_command(label="Cut", command=self.our_command)
        editMenu.add_command(label="Copy", command=self.our_command)

        # Create Options menu
        optionsMenu= tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Options", menu=optionsMenu)
        # Options menu items
        optionsMenu.add_command(label="Add new course", command=self.our_command)
        optionsMenu.add_command(label="Add lecture notes", command=self.our_command)
        optionsMenu.add_command(label="View list", command=self.our_command)

        # Create Subjects to be able to come back here
        subjectMenu = tk.Menu(menubar, tearoff=False)# To be deleted soon
        menubar.add_cascade(label="Records", menu=subjectMenu)
        subjectMenu.add_command(label="Dashboard", command=lambda: self.open_courses())

        # Create Assessments menu
        assessmentsMenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Assessments", menu=assessmentsMenu)
        # records menu items
        assessmentsMenu.add_command(label="Current term", command=lambda: self.open_assessments())
        assessmentsMenu.add_command(label="Previous Academic Sessions", command=self.our_command, state='disabled')

        # Create Analytics menu
        analyticsMenu= tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Analytics", menu=analyticsMenu)
        # Options analytics items
        analyticsMenu.add_command(label="Current term", command=lambda: self.open_charts())
        analyticsMenu.add_command(label="Current session", command=self.our_command)
        analyticsMenu.add_command(label="Term on Term", command=self.our_command, state='disabled')
        analyticsMenu.add_command(label="Academic Year on Year", command=self.our_command, state='disabled')

        # Create Attendance menu
        attendanceMenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Attendance", menu=attendanceMenu)
        # Attendance menu items
        attendanceMenu.add_command(label="New", command=self.our_command)
        attendanceMenu.add_command(label="View log", command=self.our_command)
        attendanceMenu.add_command(label="Add existing log", command=self.our_command)

        # Create Help menu
                # tk.docs says something about help menu. Check it out.
        helpMenu= tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Help", menu=helpMenu)
        # Options help items
        helpMenu.add_command(label="About SRMS", command=self.our_command)
        helpMenu.add_command(label="FAQ", command=self.our_command)
        helpMenu.add_command(label="SRMS documentation", command=self.our_command)
        helpMenu.add_command(label="Tutorial", command=self.our_command)
        helpMenu.add_command(label="Check for updates", command=self.our_command)
        helpMenu.add_command(label="Troubeshooting", command=self.our_command)

        return(menubar)

    # Create file open function
    def file_open(self):
        filename = filedialog.askopenfilename(
            initialdir = "C:/Documents",
            title = "Open A File",
            filetype = (("xlsx files", "*.xlsx"), ("All Files", "*.*"))
            )
        if filename:
            try:
                filename = r"{}".format(filename)
                df = pd.read_excel(filename)

            except(ValueError):
                pass#my_label.config(text="File couldn't be opened... try again!")

            except FileNotFoundError:
                pass#my_label.config(text="File could not be found... try again!")

    # Click command
    def our_command(self):
        pass

    def open_courses(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.navbar = NavBar(self)
        subjects_page = MySubjects(self)

    def open_calendar(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.navbar_ = NavBarCal(self)
        calendar_page = NewSession(self)

    def open_assessments(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.navbar = NavBarAssessment(self)
        assessment_treeview = Assessments(self)

    def open_attendance(self):
        # Check if user is already on Attendance
        # Use of in operator instead of == operator is deliberate as caution against reloading frame
        if '.!frame.!dashboard.!attendance' in str(self.winfo_children()[1]):
            return
        else:
            for widget in self.winfo_children():
                widget.destroy()
            attendance_frame = LessonAttendance(self)

    def open_charts(self):
        # Check if user is already on Analytics current term sub menu
        # Use of in operator instead of == operator is deliberate as caution against reloading frame
        if '.!frame.!dashboard.!chart' in str(self.winfo_children()[1]):
            return
        else:
            for widget in self.winfo_children():
                widget.destroy()
            self.navbar = NavBarAnalytics(self)
            charts_page = Chart(self)
