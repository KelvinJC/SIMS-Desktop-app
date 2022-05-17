# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 08:55:41 2022

@author: KAIZEN
"""

import tkinter as tk
from tkinter import ttk

from utils.widget import Filter
from .chart import Chart


class NavBarAnalytics(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg = '#111827')

        self.parent = parent
        self.pack(side='left', fill='both', pady=26)

        nav_button=tk.Button(self, text='Assessment Reports', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#111827',
                          command=lambda: self.open_assessment_charts())
        nav_button.grid(row=0, column=0, sticky=tk.W, pady=(10, 0), padx=10)
        nav_button=tk.Button(self, text='Student', width=20, bg='#111827', bd=0, fg='white', font=('Calibri', 12), anchor=tk.W,
                          command=lambda: self.our_command)
        nav_button.grid(row=1, column=0, sticky=tk.W, padx=30, pady=10)
        nav_button=tk.Button(self, text='Class', width=20, bg='#111827', bd=0, fg='white', font=('Calibri', 12), anchor=tk.W,
                          command=lambda: self.our_command)
        nav_button.grid(row=2, column=0, sticky=tk.W, padx=30, pady=10)
        nav_button=tk.Button(self, text='Subject', width=20, bg='#111827', bd=0, fg='white', font=('Calibri', 12), anchor=tk.W,
                          command=lambda: self.our_command)
        nav_button.grid(row=3, column=0, sticky=tk.W, padx=30, pady=10)
        nav_button=tk.Button(self, text='Attendance Reports', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#111827', bd=0,
                          command=lambda: self.our_command)
        nav_button.grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        nav_button=tk.Button(self, text='Save Report as PDF', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#111827', bd=0,
                          command=lambda: self.our_command)
        nav_button.grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        nav_button=tk.Button(self, text='Send Report as Email', width=20, anchor=tk.W, fg='white', font=("Calibri", 12, 'bold'), bg='#111827', bd=0,
                          command=lambda: self.our_command)
        nav_button.grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)


    def open_assessment_charts(self):
        # Check if user is already on Assessments
        # Use of in operator instead of == operator as caution against prior observation that when a navbar button was selected,
        # clicking on it reloaded frame
        if '.!frame.!dashboard.!chart' in str(self.parent.winfo_children()[1]):
            return
        else:
            # Clear off whichever frame is currently displayed
            self.parent.winfo_children()[1].destroy()
            # Create class treeview frame
            self.parent.chart = Chart(self.parent)

    # Click command
    def our_command(self):
        pass
