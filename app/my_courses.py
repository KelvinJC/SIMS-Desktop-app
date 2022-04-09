# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:08:55 2022

@author: KAIZEN
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from dashboard import Dashboard
from db_srms_sqlite import Database1
db1 = Database1('new_single_user2.db')

class ViewCourse(tk.Frame):
    def __init__(self, parent, controller):
        tk.__init__(self, parent)
        
        