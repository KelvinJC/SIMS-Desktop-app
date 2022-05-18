# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 12:11:04 2021
@author: KAIZEN6
"""

import tkinter as tk

from auth import StartPage, SignUp, Login
from views.dashboard import Dashboard

class SIMSApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, *kwargs)
        tk.Tk.wm_title(self, 'SIMSApp')
        tk.Tk.state(self, 'zoomed') # Maximise the app window from get go
        #tk.Tk.iconbitmap(self, default='png-to-ico.ico')
        # Make the app window fill the screen. To account for different PC screens.
        # TBD: a fix needed because app screen doesn't maximise on loading.
        w= tk.Tk.winfo_screenwidth(self)
        h= tk.Tk.winfo_screenheight(self)
        tk.Tk.geometry(self, '%dx%d' %(w,h))
        #tk.Tk.resizable(self, width= False, height = False)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create an empty dictionary. It will contain all pages' names as keys and their respective frame objects as values.
        self.frames = {}
        # Loop through to create instances of the frame objects
        # Pass in the parent and controller values as arguments and assign the page to a variable frame
        for page in (StartPage, SignUp, Login, Dashboard):
            frame = page(parent=container, controller=self)

            self.frames[page] = frame # e.g self.frames[StartPage] = StartPage(parent=container, controller=self)
            # at this point self.frames becomes = {
                                                 # StartPage: StartPage(parent=container, controller=self),
                                                 # SignUp: SignUp(parent=container, controller=self),
                                                 # Login: Login(parent=container, controller=self),
                                                 # Dashboard: Dashboard(parent=container, controller=self)
                                                 # }

            frame.grid(row=0, column=0, sticky='nsew') # e.g StartPage(parent=container, controller=self).grid(row=0, column=0, sticky='nsew)

        self.show_frame(StartPage)

    def show_frame(self, page_name):
        frame = self.frames[page_name] # means assign to frame variable the value of self.frames[page_name] key. The frame from init fxn is a dictionary key mapping to a frame object as its value
        frame.tkraise()
        # Add menu bar of frame
        menubar = frame.menubar(self)
        self.configure(menu=menubar)

# That green. #2da44e

# Create an instance of the class SIMSApp and assign it to a variable app
app = SIMSApp()
# Call the mainloop method on app to keep it running in a continuous loop
app.mainloop()
