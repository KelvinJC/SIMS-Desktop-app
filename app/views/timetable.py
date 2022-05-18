import tkinter as tk
from tkinter import ttk



class Timetable(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side='top', fill='both', expand=True, pady=(30, 30))

        for i in range(5):
            # Create a frame
            self.holder_frame = tk.LabelFrame(self)
            self.holder_frame.pack(side='top', fill='x', expand=True, pady=(0, 10), padx=(10))

            self._num_periods = 4

            for p in range(self.num_periods):
                # Create a labelframe for each
                self.l_frame = tk.LabelFrame(self.holder_frame, bg='white', borderwidth=0)
                self.l_frame.grid(row=0, column=p, pady=(0,0), padx=(0,15))
                # Add name and class labels
                subject_label=tk.Label(self.l_frame, text='Subject', font=('Calibri', 10, 'bold'), bg='white')
                subject_label.grid(row=2, column=0, columnspan = 2, pady=(10,0), padx=5, sticky='W')

                class_label = tk.Label(self.l_frame, text='Class', bg='white')
                class_label.grid(row=4, column=0, pady=(0, 10), padx=(10,25), sticky='W')

                time_label = tk.Label(self.l_frame, text='Time', bg='white')
                time_label.grid(row=5, column=0, pady=(0, 10), padx=(10,25), sticky='W')

    @property
    def num_periods(self):
        return self._num_periods

    @num_periods.setter
    def num_periods(self, num):
        self._num_periods += num

    def add_subject(self):
        pass

    def add_period(self):
        per = Period(self, )

class Period(tk.LabelFrame):
    def __init__(self, parent, col):
        tk.LabelFrame.__init__(self, parent)
        self.grid(row=0, column=col, padx=5)
        # Add name and class labels
        subject_label=tk.Label(self.l_frame, text='S', font=('Calibri', 10, 'bold'), bg='white')
        subject_label.grid(row=0, column=0, columnspan = 2, pady=(10, 10), padx=10, sticky='W')

        class_label = tk.Label(self.l_frame, text='C', bg='white')
        class_label.grid(row=1, column=0, pady=(0, 10), padx=(10,25), sticky='W')

        time_label = tk.Label(self.l_frame, text='T', bg='white')
        time_label.grid(row=2, column=0, pady=(0, 10), padx=(10,25), sticky='W')
