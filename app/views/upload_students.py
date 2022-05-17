# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 17:57:55 2022

@author: KAIZEN
"""


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from tkinter import ttk, filedialog

from models.database import db


class UploadStudentsList(tk.Frame):
    def __init__(self, parent): # I doubt this root arg is required
        tk.Frame.__init__(self, parent, bg = '#f3f3f4')
        self.pack(side='right', fill='both', expand=True)

        # Add Search Box (Rememeber to implement 'Search' showing in bar )
        search_box = tk.Entry(self, width=60)
        search_box.pack(pady=4, padx=2, anchor=tk.NE)

        # Add some style
        style = ttk.Style()
        # Pick a theme
        #style.theme_use("default")
        # Configure our treeview colours
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=20,
                        fieldbackground="#D3D3D3"
                        )
        # Change selected colour
        style.map('Treeview',
                  background=[('selected', '#73c2fb')]) #a4bce9


        # Create Treeview Frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.X, anchor=tk.N, padx=(20,0))

        # Treeview Scrollbar
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=(2,0))

        # Create Treeview
        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended', height=25)
        # Pack to the screen
        self.my_tree.pack(fill=tk.X)

        # Configure scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Define our columns
        self.my_tree['columns'] = ('ID', 'First name', 'Middle name', 'Last name', 'Gender')

        # Format our columns
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("ID", anchor=tk.CENTER, stretch=tk.NO, width=0)
        self.my_tree.column("First name", anchor=tk.W, width=200)
        self.my_tree.column("Middle name", anchor=tk.W, width=200)
        self.my_tree.column("Last name", anchor=tk.W, width=200)
        self.my_tree.column("Gender", anchor=tk.W, width=600)

        # Create Column headings
        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading("First name", text="First name", anchor=tk.W)
        self.my_tree.heading("Middle name", text="Middle name", anchor=tk.W)
        self.my_tree.heading("Last name", text="Last name", anchor=tk.W)
        self.my_tree.heading("Gender", text="Gender", anchor=tk.W)

        # Create striped Treeview rows
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="#f3f3f4")

        # Bind the treeview
        self.my_tree.bind ("<ButtonRelease-1>", self.select_record)

        # Add Label Frame for dropdowns and buttons
        button_frame = tk.LabelFrame(self, text="Upload list", bg='white')
        button_frame.pack(fill='x', expand='yes', padx=(20, 17))

        # Initiate class_list variable
        class_list = ['Select class']
        # Get list of classes from database
        fetch_class_list = [class_pick[1] for class_pick in db.fetch_class()]
        # Concatenate both lists
        class_list += fetch_class_list

        self.class_dropdown_menu = ttk.Combobox(button_frame, values=class_list, state='readonly')
        self.class_dropdown_menu.current(0)
        self.class_dropdown_menu.grid(row=0, column=1, padx=10, pady=10)

        upload_button = ttk.Button(button_frame, text="Upload", command=lambda: self.read_student_list_from_excel())
        upload_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = ttk.Button(button_frame, text="Move Up", command=self.up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = ttk.Button(button_frame, text="Move Down", command=self.down)
        move_down_button.grid(row=0, column=5, padx=20, pady=10)

        save_button = ttk.Button(button_frame, text="Save", command=lambda: self.save_student_list_to_db())
        save_button.grid(row=0, column=6, padx=10, pady=10)


    def select_record(self, event):
        '''
        Selects a row of records on the treeview. Usually for the purpose of sending row contents to entry boxes.

        Parameters
        ----------
        event : The selection of a row on the treeview by mouse.

        Returns
        -------
        None.

        '''
        # Grab record number
        selected =self.my_tree.focus()
        # Grab record values
        values =self.my_tree.item(selected, 'values')

    def remove_record(self):
        # Grab record
        selected =self.my_tree.focus()
        # Grab record values
        values =self.my_tree.item(selected, 'values')
        # Delete student record from database
        db.remove_student(values[0]) # values[0] = student_id
        # Clear entries
        self.clear_entries()
        # Clear Treeview
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
        # Populate treeview
        self.populate_treeview()

    def read_student_list_from_excel(self):
        '''
        To open an excel file located in system memory and transfer its contents i.e. a table of students with columns first name, middle name, last name and gender
        into a treeview.

        #--------- BUSINESS RULES -------#
            Business rules of this portion of the program:
                The file to be read must be a spreadsheet file
                There must be 4 and only 4 columns First name, Middle name, Last name and Gender
                The middle name column may be null for some students
                The first row must be the title of each column
        '''
        filename = filedialog.askopenfilename(
            initialdir = "C:/Documents",
            title = "Open A File",
            filetype = (("Excel files", "*.xlsx"), ("All Files", "*.*"))
            )

        if filename:
            try:
                filename = r"{}".format(filename)
                df = pd.read_excel(filename)
                # Data cleaning
                # TBD: What to do if all middle name columns are empty i.e null
                df = df.dropna(axis='columns', how='all')
                df = df.dropna(how='all')
                # A measure to prevent none student excel files. Not enough but a start
                # TBD: Leave instructions in docs about how to input spreadsheet. Specify titles must be stated in the right order
                # TBD Add more preventive measures
                if df.loc[0][0].lower() not in ('first name', 'firstname', 'f_name', 'first_name', 'fname'):
                    messagebox.showerror("File Error", "File does not match student list format... try again!")
                    return
                # Check for and remove titles from input spreadsheet TBD: Leave instructions in docs about how to input spreadsheet. Specify titles
                if df.loc[0][0].lower() in ('first name', 'firstname', 'f_name', 'first_name'):
                    df = df.drop(df.index[0])

            except(ValueError):
                messagebox.showerror("File Error", "File could not be opened... try again!")
            except FileNotFoundError:
                messagebox.showerror("File Error", "File could not be found... try again!")
            except UnboundLocalError: # To handle "local variable 'df' referenced before assignment"
                return
            except KeyError:
                messagebox.showerror("File Error", "File could not be opened... try again!")
                return
        # Clear old treeview
        self.clear_tree()

        # Create new treeview
        # Define our columns
        self.my_tree['columns'] = ('First name', 'Middle name', 'Last name', 'Gender')

        # Format our columns
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        #self.my_tree.column("ID", anchor=tk.CENTER, stretch=tk.NO, width=0)
        self.my_tree.column("First name", anchor=tk.W, width=200)
        self.my_tree.column("Middle name", anchor=tk.W, width=200)
        self.my_tree.column("Last name", anchor=tk.W, width=200)
        self.my_tree.column("Gender", anchor=tk.W, width=800)

        # Create Column headings
        self.my_tree.heading("#0", text="", anchor=tk.W)
        #self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading("First name", text="First name", anchor=tk.W)
        self.my_tree.heading("Middle name", text="Middle name", anchor=tk.W)
        self.my_tree.heading("Last name", text="Last name", anchor=tk.W)
        self.my_tree.heading("Gender", text="Gender", anchor=tk.W)

        # Create striped Treeview rows
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="#f3f3f4")

        # Loop through column list
        self.count = 0
        for column in self.my_tree["columns"]:
            # Put data in treeview
            self.df_rows = df.to_numpy().tolist()
        for row in self.df_rows:
            if self.count % 2 == 0:
                # Insert records into treeview rows
               self.my_tree.insert(parent="", index="end", iid=self.count, values=(row), tags=("evenrow",))
            else:
               self.my_tree.insert(parent="", index="end", iid=self.count, values=(row), tags=("oddrow",))
            self.count += 1

    def save_student_list_to_db(self):
        '''
        Save each student's data in the student table of database.
        Returns
        -------
        None.

        '''
        if self.class_dropdown_menu.get() == "Select class":
            messagebox.showerror("Selection Error", "Please select a class.")
            return

        try:
            for row in self.df_rows:
            # Push record into database
                db.insert_student(row[0], row[1], row[2], row[3], self.class_dropdown_menu.get())
        except(IndexError):
            messagebox.showerror("Data Error", "Data in a column is missing. Please check and try again")
        except: # To handle sqlite.3 Integrity error "NOT NULL constraint failed"
            messagebox.showerror("Data Error", "Data in a column is missing. Please check sqlite and try again")

    def clear_tree(self):
        # Clear tree currently in view
        self.my_tree.delete(*self.my_tree.get_children())

    # For fun I guess
    # Move Row Up
    def up(self):
        rows = self.my_tree.selection()
        for row in rows:
          self.my_tree.move(row, self.my_tree.parent(row), self.my_tree.index(row)-1)

    # Move Row Down
    def down(self):
        rows = self.my_tree.selection()
        for row in reversed(rows):
           self.my_tree.move(row,self.my_tree.parent(row),self.my_tree.index(row)+1)
