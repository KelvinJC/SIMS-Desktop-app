# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 08:31:03 2022

@author: KAIZEN
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models.database import db


class MySubjects(tk.Frame):
    def __init__(self, parent): # I doubt this root arg is required
        tk.Frame.__init__(self, parent, bg="#f3f3f4")

        # Function that puts mainframe on screen (this is probably going to be cut and put as the callable function in a subjects button)
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
        self.my_tree['columns'] = ('ID', 'Subject name')

        # Format our columns
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("ID", anchor=tk.CENTER, stretch=tk.NO, width=0)
        self.my_tree.column("Subject name", anchor=tk.W, width=300)

        # Create Column headings
        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading("Subject name", text="Subject name", anchor=tk.W)

        # Create striped Treeview rows
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="#f3f3f4")

        # Create Add subject frame
        add_subject_frame = tk.LabelFrame(self, text="", bg="#f3f3f4")
        add_subject_frame.pack(fill='x', expand='yes', padx=(20, 17))

        # Subject widgets: Labels & entries
        subject_name_label = tk.Label(add_subject_frame, text="Subject name")
        subject_name_label.grid(row=0, column=0, padx=5)
        self.subject_name_entry = tk.Entry(add_subject_frame, text=subject_name_label, width=60)
        self.subject_name_entry.grid(row=0, column=1, padx=5)


        # Add Buttons
        add_button = ttk.Button(add_subject_frame, text="Add Subject", command=lambda: self.add_record(), width=42)
        add_button.grid(row=0, column=4, padx=10, pady=5, columnspan=2)

        update_button = ttk.Button(add_subject_frame, text="Update Subject", width=19, command=lambda: self.update_record())
        update_button.grid(row=1, column=4, padx=1, pady=5)

        remove_one_button = ttk.Button(add_subject_frame, text="Remove Subject", command=lambda: self.remove_record(), width=19)
        remove_one_button.grid(row=1, column=5, padx=1, pady=5)

        # Bind the treeview
        self.my_tree.bind ("<ButtonRelease-1>", self.select_record)

        # Add Other Buttons
        button_frame = tk.LabelFrame(self, text="", bg="#f3f3f4")
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
        # Loop through records from database
        for record in db.fetch_subject():

            if self.count % 2 == 0:
                # Insert records into treeview
               self.my_tree.insert(parent="", index="end", iid=self.count, values=(record[0], record[1]), tags=("evenrow",)) # record[0] = subject_id 'from database', record[1]= subject_name, record[2]= subject_code if any
            else:
               self.my_tree.insert(parent="", index="end", iid=self.count, values=(record[0], record[1]), tags=("oddrow",))  # record[0] = subject_id, record[1]= subject_name, record[2]= subject_code if any

            self.count += 1

    def add_record(self):
        if self.subject_name_entry.get() == "":
            messagebox.showerror("", "Subject name field is required.")
            return
        db.insert_subject(self.subject_name_entry.get())
        # Clear Treeview
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
         # Clear entries
        self.clear_entries()
         # Populate treeview
        self.populate_treeview()

    def select_record(self, event):
        # Clear entries
        self.clear_entries()
        # Grab record number
        selected =self.my_tree.focus()
        # Grab record values
        values =self.my_tree.item(selected, 'values')
        # Output to entry boxes
        try:
            self.subject_name_entry.insert(0, values[1])
        except IndexError:
            pass
    def update_record(self):
        if self.subject_name_entry.get() == "":
            messagebox.showerror("", "Select subject to update.")
            return
        # Grab record number
        selected =self.my_tree.focus()
        # Grab record values
        values =self.my_tree.item(selected, 'values')
        # Update subject record in database
        # In order to do away with id column
        # First obtain record id from database
        # db.fetch_id(values[x])[0]
        # Nope just hide id column abeg. lol
        db.update_subject(values[0], self.subject_name_entry.get()) # values[0] = subject_id
        self.clear_entries()
        # Clear Treeview
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
        # Populate treeview
        self.populate_treeview()

    def remove_record(self):
        if self.subject_name_entry.get() == "":
            messagebox.showerror("", "Select subject to remove.")
            return
        else:
            if messagebox.askokcancel("", "Are you sure you want to remove this subject?"):
                # Grab record
                selected =self.my_tree.focus()
                # Grab record values
                values =self.my_tree.item(selected, 'values')
                # Delete subject record from database
                db.remove_subject(values[0]) # values[0] = subject_id
                # Clear entries
                self.clear_entries()
                # Clear Treeview
                for record in self.my_tree.get_children():
                    self.my_tree.delete(record)
                # Populate treeview
                self.populate_treeview()

    def clear_entries(self):
        self.subject_name_entry.delete(0, tk.END)

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
