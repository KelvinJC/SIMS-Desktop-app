# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 17:57:55 2022

@author: KAIZEN
"""


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from model.db_sims_sqlite import Database
db = Database('new_single_user3.db')

class StudentTreeview(tk.Frame):
    def __init__(self, parent): # I doubt this root arg is required
        tk.Frame.__init__(self, parent)

        
        # Function that puts mainframe on screen (this is probably going to be cut and put as the callable function in a students button)
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
        self.my_tree['columns'] = ('ID', 'First name', 'Last name', 'Gender', 'Class')
        
        # Format our columns
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("ID", anchor=tk.CENTER, stretch=tk.NO, width=0)
        self.my_tree.column("First name", anchor=tk.W, width=200)
        self.my_tree.column("Last name", anchor=tk.W, width=200)
        self.my_tree.column("Gender", anchor=tk.W, width=200)
        self.my_tree.column("Class", anchor=tk.W, width=600)
  
        # Create Column headings
        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading("First name", text="First name", anchor=tk.W)
        self.my_tree.heading("Last name", text="Last name", anchor=tk.W)
        self.my_tree.heading("Gender", text="Gender", anchor=tk.W)
        self.my_tree.heading("Class", text="Class", anchor=tk.W)
   
        # Create striped Treeview rows
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="#f3f3f4")
       
        # Create Add student frame
        self.add_student_frame = tk.LabelFrame(self, text="Add student")
        self.add_student_frame.pack(fill='x', expand='yes', padx=(20, 17))
        
        # student widgets: Labels & entries
        first_name_label = tk.Label(self.add_student_frame, text="First name")
        first_name_label.grid(row=0, column=0, padx=5)
        self.first_name_entry = tk.Entry(self.add_student_frame, text=first_name_label, width=30)
        self.first_name_entry.grid(row=0, column=1, padx=5)
        
        last_name_label = tk.Label(self.add_student_frame, text="Last name")
        last_name_label.grid(row=0, column=2, padx=5)
        self.last_name_entry = tk.Entry(self.add_student_frame, text=last_name_label, width=30)
        self.last_name_entry.grid(row=0, column=3, padx=5)
        
        self.gender_select = tk.StringVar()
        self.gender_select.set('Select gender')
        
        gender_dropdown_menu = ttk.OptionMenu(self.add_student_frame, self.gender_select, *['Select gender', 'Male', 'Female'])
        gender_dropdown_menu.grid(row=0, column=4, padx=20)
        
        self.class_select = tk.StringVar()
        self.class_select.set('Select Class')
        # Initiate class_list variable
        class_list = ['Select Class'] 
        # Get list of classes from database
        db_fetch_class_list = [class_pick[1] for class_pick in db.fetch_class()]
        # Concatenate both lists 
        class_list += db_fetch_class_list

        class_dropdown_menu = ttk.OptionMenu(self.add_student_frame, self.class_select, *class_list)
        class_dropdown_menu.grid(row=0, column=5, padx=10)
        
        # Add Buttons 
        add_button = ttk.Button(self.add_student_frame, text="Add Record", command= lambda: self.add_record(), width=42)
        add_button.grid(row=0, column=6, padx=10, pady=5, columnspan=2)
        
        update_button = ttk.Button(self.add_student_frame, text="Update Record", command= lambda: self.update_record(), width=19)
        update_button.grid(row=1, column=6, padx=1, pady=5)

        remove_one_button = ttk.Button(self.add_student_frame, text="Remove Record", command=lambda: self.remove_record(), width=19)
        remove_one_button.grid(row=1, column=7, padx=1, pady=5)
               
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
        # Loop through records from database 
        for record in db.fetch_student():
            
            if self.count % 2 == 0:
                # Insert records into treeview
               self.my_tree.insert(parent="", index="end", iid=self.count, values=(record[0], record[1], record[2], record[3], record[4]), tags=("evenrow",)) # record[0] = student_id 'from database', record[1]= student_name
              
            else:
               self.my_tree.insert(parent="", index="end", iid=self.count, values=(record[0], record[1], record[2], record[3], record[4]), tags=("oddrow",))  # record[0] = student_id 'from database', record[1]= student_name
              
            self.count += 1  
                
    def add_record(self):
        
        if self.first_name_entry.get() == "" and self.last_name_entry.get() == "":
            messagebox.showerror("", "Student name fields are required.")
            return
        db.insert_student(self.first_name_entry.get(), self.last_name_entry.get(), self.gender_select.get(), self.class_select.get()) # maybe get class_id from a combo with a function pulling class name first
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
        self.first_name_entry.insert(0, values[1])
        self.last_name_entry.insert(0, values[2])
        #self.gender_entry.insert(0, values[3])
        self.gender_select.set(values[3])
        #self.class_id_entry.insert(0, values[4])
        self.class_select.set(values[4])
        
    def update_record(self):
        # Grab record
        selected =self.my_tree.focus()
        # Grab record values
        values =self.my_tree.item(selected, 'values')
        # Update student record in database
        db.update_student(values[0], self.first_name_entry.get(), self.last_name_entry.get(), self.gender_select.get(), self.class_select.get()) # values[0] = student_id
        # Clear entries
        self.clear_entries()
        # Clear Treeview
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
        # Populate treeview 
        self.populate_treeview() 
    
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
       
    def clear_entries(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.gender_select.set('Select gender')
        self.class_select.set('Select class')

       
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