# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 15:13:04 2022

@author: KAIZEN
"""


import tkinter as tk
from tkinter import ttk

from models.database import db


class Filter(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.pack(side='left', fill='y')
        self.holder_frame = tk.Frame(self, bg='white') # wraps around session and subject frames to keep them aligned
        self.holder_frame.pack(side='left', fill='y', pady=26, padx=15)

        # Create class dropdown menu as attribute of holder frame.
        # Initiate class_list variable
        self.class_list = ["Select class"]
        # Get list of classes from database
        db_fetch_class_list = [class_pick[1] for class_pick in db.fetch_class()]
        # Concatenate both lists
        self.class_list += db_fetch_class_list
        # Create dropdown menu of classes
        self.class_dropdown_menu = ttk.Combobox(self.holder_frame, value=self.class_list, width=30, state='readonly')
        self.class_dropdown_menu.current(0)
        self.class_dropdown_menu.grid(row=0, column=0, pady=(5,20), padx=10)

        # Create subject dropdown menu as attribute of holder frame.
        self.subject_dropdown_list = ["Select subject"]
        # Get list of subjects from database
        db_fetch_subject_list = [subject[1] for subject in db.fetch_subject()]
        # Concatenate both lists
        self.subject_dropdown_list += db_fetch_subject_list
        # Create dropdown menu of subjects
        self.subject_dropdown_menu = ttk.Combobox(self.holder_frame, value=self.subject_dropdown_list, width=30, state='readonly')
        self.subject_dropdown_menu.grid(row=1, column=0, pady=(100,20), padx=10) # labeled as self so I can destroy in Chart class when filter is by class
        self.subject_dropdown_menu.current(0)



# Create a button which has hover effect and changes colour to indicate it has been clicked.
class CustomButton(tk.Button):
    def __init__(self, parent, text, width, height, fontsize, command):
        tk.Button.__init__(self, parent, width=width, height=height, text=text,
                                           font=('Calibri', fontsize, 'bold'),
                                           fg='#076cf7',
                                           bg='#f3f3f4',
                                           border=0,
                                           activeforeground='#f3f3f4',
                                           activebackground='#54aeff',
                                           command=command
                                           )
        #self.place(x=20, y=20)
        self.parent = parent
        # Bind button to enter event
        self.bind('<Enter>', lambda e: self.on_enter('#54aeff', '#f1f1f1'))
        # Bind button to leave event
        self.bind('<Leave>', lambda e: self.on_leave('#076cf7', '#f3f3f4'))
        # Bind button to click event
        #self.bind('<ButtonRelease-1>', lambda e: self.on_click('white', '#076cf7'))

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

# Create a blue button.
class BlueButton(tk.Button):
    def __init__(self, parent, text, width, height, fontsize, command):
        tk.Button.__init__(self, parent, width=width, height=height, text=text,
                                           font=('Calibri', fontsize, 'bold'),
                                           fg='#f1f1f1',
                                           bg='#54aeff',
                                           border=0,
                                           activeforeground='#f3f3f4',
                                           activebackground='#54aeff',
                                           command=command)
