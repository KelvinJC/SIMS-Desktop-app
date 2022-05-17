# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 11:35:32 2022

@author: KAIZEN
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models.database import db


class MyClasses(tk.Frame):
    def __init__(self, parent): # I doubt this root arg is required
        tk.Frame.__init__(self, parent)

        # Function that puts mainframe on screen (this is probably going to be cut and put as the callable function in a classs button)
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
        tree_frame.pack(fill=tk.X, anchor=tk.N, padx=(20, 0))

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
        self.my_tree['columns'] = ('ID', 'Class', 'R.Id', 'First name', 'Middle name', 'Last name')

        # Format our columns
        self.my_tree.column("#0", width=20, stretch=tk.NO)
        self.my_tree.column("ID", anchor=tk.CENTER, stretch=tk.NO, width=0)
        self.my_tree.column("Class", anchor=tk.W, width=50)
        self.my_tree.column("R.Id", anchor=tk.W, width=30)
        self.my_tree.column("First name", anchor=tk.W, width=200)
        self.my_tree.column("Middle name", anchor=tk.W, width=200)
        self.my_tree.column("Last name", anchor=tk.W, width=1000)

        # Create Column headings
        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading("Class", text="Class", anchor=tk.W)
        self.my_tree.heading("R.Id", text="R.Id", anchor=tk.W)
        self.my_tree.heading("First name", text="First name", anchor=tk.W)
        self.my_tree.heading("Middle name", text="Middle name", anchor=tk.W)
        self.my_tree.heading("Last name", text="Last name", anchor=tk.W)

        # Create striped Treeview rows
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="#f3f3f4")

        # Create Add class frame
        self.add_class_frame = tk.LabelFrame(self, text="Add class")
        self.add_class_frame.pack(fill='x', expand='yes', padx=(20, 17))

        # class widgets: Labels & entries
        class_name_label = tk.Label(self.add_class_frame, text="Class")
        class_name_label.grid(row=0, column=0, padx=5)
        self.class_name_entry = tk.Entry(self.add_class_frame, text=class_name_label, width=30)
        self.class_name_entry.grid(row=0, column=1, padx=5)



        # Add Buttons (Buttons are positioned after the combobox to be exposed to destroy function in the addsubject method of NavBar class )
        add_button = ttk.Button(self.add_class_frame, text="Add Class", command= lambda: self.add_record(), width=42)
        add_button.grid(row=0, column=4, padx=10, pady=5, columnspan=2)

        update_button = ttk.Button(self.add_class_frame, text="Update Class", command= lambda: self.update_record(), width=19)
        update_button.grid(row=1, column=4, padx=1, pady=(5,20))

        remove_one_button = ttk.Button(self.add_class_frame, text="Remove Class", command=lambda: self.remove_record(), width=19)
        remove_one_button.grid(row=1, column=5, padx=1, pady=(5, 20))

        # Bind the treeview
        self.my_tree.bind ("<ButtonRelease-1>", self.select_record)

        # Add Other Buttons
        button_frame = tk.LabelFrame(self, text="Commands")
        button_frame.pack(fill='x', expand='yes', padx=(20, 17))

        move_up_button = ttk.Button(button_frame, text="Move Up", command=self.up)
        move_up_button.grid(row=0, column=3,
                            padx=10, pady=10)

        move_down_button = ttk.Button(button_frame, text="Move Down", command=self.down)
        move_down_button.grid(row=0, column=4, padx=10, pady=10)

        clear_entries_button = ttk.Button(button_frame, text="Clear Entry Boxes", command=self.clear_entries)
        clear_entries_button.grid(row=0, column=5, padx=10, pady=10)

        self.populate_treeview()

    # Populate treeview from database
    def populate_treeview(self):
        # Create counter (Treeview stripes)
        self.count = 0
        self.count_child_row = 100
        # Labeled R.Id on treeview for brevity. Serves to ennumerate students in each class. Self.count_student not used since each iid must be unique and ennumeration by its nature must repeat numbers used
        student_roll_index = 1
        # Loop through records from database
        for record in db.fetch_class():

            if self.count % 2 == 0:
                # Insert even color striped records into treeview
               self.my_tree.insert(parent="",
                                   index="end",
                                   iid=self.count,
                                   open=True,
                                   values=(record[0], record[1]), # record[0] = class_id 'from database', record[1]= class_name
                                   tags=("evenrow",)
                                   )
                # Insert students as child rows of each class.
               for rec in db.fetch_students_in_class(record[1]):
                   # Cast tuple to list to prepare for is_None middle name assignment
                   rec = list(rec)
                   # Check if middle name is None
                   if rec[2] is None:
                       rec[2] = ''
                   # Check if number of rows is even. For coloring of rows
                   if self.count_child_row % 2 == 0:
                       self.my_tree.insert(parent=self.count,
                                           index="end",
                                           iid=self.count_child_row,
                                           values=('', '', student_roll_index, rec[1], rec[2], rec[3]),
                                           tags=("oddrow",)
                                           )
                   else:
                       self.my_tree.insert(parent=self.count,
                                           index="end",
                                           iid=self.count_child_row,
                                           values=('', '', student_roll_index, rec[1], rec[2], rec[3]),
                                           tags=("evenrow",)
                                           )
                   self.count_child_row += 1
                   student_roll_index += 1
            else:
                # Insert odd color striped records into treeview
               self.my_tree.insert(parent="", index="end", iid=self.count, values=(record[0], record[1]), tags=("oddrow",))  # record[0] = class_id 'from database', record[1]= class_name
               # Insert students as child rows of each class.
               for rec in db.fetch_students_in_class(record[1]):
                   # Cast tuple to list to prepare for is_None middle name assignment
                   rec = list(rec)
                   # Check if middle name is None
                   if rec[2] is None:
                       rec[2] = ''
                   if self.count_child_row % 2 == 0:
                       self.my_tree.insert(parent=self.count,
                                           index="end",
                                           iid=self.count_child_row,
                                           values=('', '', student_roll_index, rec[1], rec[2], rec[3]),
                                           tags=("evenrow",)
                                           )
                   else:
                       self.my_tree.insert(parent=self.count,
                                           index="end",
                                           iid=self.count_child_row,
                                           values=('', '', student_roll_index, rec[1], rec[2], rec[3]),
                                           tags=("oddrow",)
                                           )
                   self.count_child_row += 1
                   student_roll_index += 1

            self.count += 1
            # Reset student count for next class
            student_roll_index = 1

    def add_record(self):
        if self.class_name_entry.get() == "":
            messagebox.showerror("", "Class name field is required.")
            return
        db.insert_class(self.class_name_entry.get())
        # Clear Treeview
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
         # Clear entries
        self.clear_entries()
         # Populate treeview
        self.populate_treeview()

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
        # Clear entries
        self.clear_entries()
        # Grab record number
        selected =self.my_tree.focus()
        # Grab record values
        values =self.my_tree.item(selected, 'values')
        # Output to entry boxes
        try:
            self.class_name_entry.insert(0, values[1])
        except:
            pass

    def update_record(self):
        if self.class_name_entry.get() == "":
            messagebox.showerror("", "Select class to update.")
            return
        self.class_name_entry.get()
        # Grab record
        selected =self.my_tree.focus()
        # Grab record values
        values =self.my_tree.item(selected, 'values')
        # Update class record in database
        db.update_class(values[0], self.class_name_entry.get()) # values[0] = class_id
        # Clear entries
        self.clear_entries()
        # Clear Treeview
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
        # Populate treeview
        self.populate_treeview()

    def remove_record(self):
        if self.class_name_entry.get() == "":
            messagebox.showerror("", "Select class to remove.")
            return
        else:
            if messagebox.askokcancel("", "Are you sure you want to remove this class?\n\nNOTE: \nAll the records of students in this class will also be removed."):
                # Grab record
                selected =self.my_tree.focus()
                # Grab record values
                values =self.my_tree.item(selected, 'values')
                # Delete class record from database
                db.remove_class(values[0]) # values[0] = class_id
                # Delete all students in the above deleted class record. If cascade is setup, this fxn becomes redundant
                db.remove_students_in_selected_class(self.class_name_entry.get())
                # Clear entries
                self.clear_entries()
                # Clear Treeview
                for record in self.my_tree.get_children():
                    self.my_tree.delete(record)
                # Populate treeview
                self.populate_treeview()

    def clear_entries(self):
        self.class_name_entry.delete(0, tk.END)

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
