# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 08:55:41 2022

@author: KAIZEN
"""



import tkinter as tk
from tkinter import ttk
from .session import NewSession, NewTerm
from .timetable import Timetable
#from .calendar import MyCalendar


class NavBarCal(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = '#111827')

        self.parent = parent
        self.pack(side='left', fill='both', pady=26)

        btn1=tk.Button(self, text='My Calendar', width=20, anchor=tk.W, fg='white',
                              font=("Calibri", 12, 'bold'), bg='#111827',
                              command=lambda: self.our_command)
        btn1.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        btn2=tk.Button(self, text='New Session', width=20, fg='white',
                              font=("Calibri", 12), bg='#111827', bd=0, anchor=tk.W,
                              command=lambda: self.show_session())
        btn2.grid(row=1, column=0, sticky=tk.W, padx=30, pady=10)
        btn3=tk.Button(self, text='New Term', width=20, fg='white',
                              font=("Calibri", 12), bg='#111827', bd=0, anchor=tk.W,
                              command=lambda: self.show_term())
        btn3.grid(row=2, column=0, sticky=tk.W, padx=30, pady=10)
        btn4=tk.Button(self, text='Timetable', width=20, anchor=tk.W, fg='white',
                              font=("Calibri", 12, 'bold'), bg='#111827', bd=0,
                              command=lambda: self.show_timetable())
        btn4.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        btn5=tk.Button(self, text='Add an event or reminders', width=25, anchor=tk.W, fg='white',
                              font=("Calibri", 12, 'bold'), bg='#111827', bd=0,
                              command=lambda: self.our_command)
        btn5.grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)


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

    def show_timetable(self):
        # Check if user is already on timetable.
        # Use of in operator instead of == operator as caution against prior observation that when a navbar button was selected,
        # clicking on reloaded frame
        if '.!frame.!dashboard.!timetable' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create     frame
            self.parent.view = Timetable(self.parent)

    # Click command
    def our_command(self):
        pass
