# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 00:37:19 2022

@author: KAIZEN
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkcalendar as tkc # used pip to install
from tkcalendar import DateEntry
import datetime
from datetime import date
from PIL import ImageTk, Image

from models.database import db


'''
Session page will have picture bg
entry bars like login page

Two follow up warnings before a session is deleted.
are you sure you want to delete this session
all records and documents in this academic session will be deleted.
There will be no opportunity to recover deleted session records or documents


use of datetime to track current year, end of current session, end of current term

automatically delete from db any session that's created before the end of current session

navbar name = New Session/Term
'''


'''
class SessionInfo():
    current_academic_year = ''
    current_term = ''
'''

class NewSession(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side='right', fill='both', expand=True)

        holder_frame = tk.Frame(self)
        holder_frame.pack(side='top', fill='both', expand=True, pady=24, padx=15)

        # Image import
        self.img = Image.open("images/dgrey.jpg")
        self.img = self.img.resize((self.winfo_screenwidth(),self.winfo_screenheight()))

        # There is the need to specify the master tk instance since ImageTK is also an instance of tkinter's Tk class
        self.img = ImageTk.PhotoImage(self.img, master=holder_frame)
        # Define canvas
        self.my_canvas = tk.Canvas(holder_frame) # , bg = 'black'
        self.my_canvas.pack(side='top', fill='both', expand=True)
        # Put the image on the canvas
        self.my_canvas.create_image(0,0, image=self.img, anchor='nw')
        # Add labels
        self.my_canvas.create_text(210, 15, text = 'Create Session', font=("Calibri", 21, 'bold italic'), fill='white', anchor='nw')

        self.my_canvas.create_text(410, 68, text = 'Enter session here', font=("Calibri", 13, 'bold'), fill='white', anchor='nw')
        self.my_canvas.create_text(410, 138, text = 'Resumption date', font=("Calibri", 13, 'bold'), fill='white', anchor='nw')
        self.my_canvas.create_text(410, 208, text = 'Closing date', font=("Calibri", 13, 'bold'), fill='white', anchor='nw')

        # Variables
        self.session_name = tk.StringVar()
       # Add entry boxes
        self.session_name_entry = tk.Entry(holder_frame, textvariable=self.session_name, font=('Helvetica', 15), width=28, fg="#076cf7", bd=0)
       # Add calendar
        resume_cal = DateEntry(holder_frame, selectmode='day', width=32, height=20, font=('Calibri', 13), date_pattern="dd/mm/yyyy", state='readonly')
        closing_cal = DateEntry(holder_frame, selectmode='day', width=32, height=20, font=('Calibri', 13), date_pattern="dd/mm/yyyy", state='readonly')

        # Create button windows
        session_name_entry_window = self.my_canvas.create_window(410, 90, anchor= 'nw', window=self.session_name_entry)
        self.session_resumption_entry_window = self.my_canvas.create_window(410, 160, anchor= 'nw', window=resume_cal)
        session_closing_entry_window = self.my_canvas.create_window(410, 230, anchor= 'nw', window=closing_cal)


class NewTerm(tk.Frame):
    current_term = ''
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side='right', fill='both', expand=True)

        holder_frame = tk.Frame(self)
        holder_frame.pack(side='top', fill='both', expand=True, pady=24, padx=15)

        # Image import
        self.img = Image.open("images/dgrey.jpg")
        self.img = self.img.resize((self.winfo_screenwidth(),self.winfo_screenheight()))

        # There is the need to specify the master tk instance since ImageTK is also an instance of tkinter's Tk class
        self.img = ImageTk.PhotoImage(self.img, master=holder_frame)
        # Define canvas
        self.my_canvas = tk.Canvas(holder_frame) # , bg = 'black'
        self.my_canvas.pack(side='top', fill='both', expand=True)
        # Put the image on the canvas
        self.my_canvas.create_image(0,0, image=self.img, anchor='nw')
        # Add labels
        self.my_canvas.create_text(210, 15, text = 'Add New Term', font=("Calibri", 21, 'bold italic'), fill='white', anchor='nw')

        self.my_canvas.create_text(410, 68, text = 'Select term', font=("Calibri", 13, 'bold'), fill='white', anchor='nw')
        self.my_canvas.create_text(410, 188, text = 'Resumption date', font=("Calibri", 13, 'bold'), fill='white', anchor='nw')
        self.my_canvas.create_text(410, 258, text = 'Closing date', font=("Calibri", 13, 'bold'), fill='white', anchor='nw')

        #dt = date(2022,3,1)

        # Variables
        self.term_name = tk.StringVar()
        self.term_resumption= tk.StringVar()
        self.term_closing = tk.StringVar()
        # Add entry boxes
        self.term_name_entry = tk.Entry(holder_frame, textvariable=self.term_name, font=('Helvetica', 18), width=24, fg="#076cf7", bd=0)
        # Create a list of terms
        term_list = ['First term', 'Second term', 'Third term']
        term_combo = ttk.Combobox(holder_frame, value=term_list, width=32, font=('Calibri', 13), state='readonly')
        resume_cal = DateEntry(holder_frame, selectmode='day', width=32, font=('Calibri', 13), date_pattern="dd/mm/yyyy", state='readonly')
        closing_cal = DateEntry(holder_frame, selectmode='day', width=32, font=('Calibri', 13), date_pattern="dd/mm/yyyy", state='readonly')

        # Create button windows
        term_name_entry_window = self.my_canvas.create_window(410, 90, anchor= 'nw', window=term_combo)
        self.term_resumption_entry_window = self.my_canvas.create_window(410, 210, anchor= 'nw', window=resume_cal)
        term_closing_entry_window = self.my_canvas.create_window(410, 280, anchor= 'nw', window=closing_cal)
