
import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

from utils.widget import CustomButton
from views.dashboard import Dashboard


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Image import
        self.img = Image.open("images/lib1.jpg")
        # Set size of image to screen size
        self.img = self.img.resize((controller.winfo_screenwidth(), controller.winfo_screenheight()))

        # There is the need to specify the master tk instance since ImageTK is also an instance of tkinter's Tk class
        self.img = ImageTk.PhotoImage(self.img, master=self)

        # Define canvas
        self.my_canvas = tk.Canvas(self)
        self.my_canvas.pack(side='top', fill='both', expand=True)
        # Put the image on the canvas
        self.my_canvas.create_image(0,0, image=self.img, anchor='nw')

        # Add label
        self.my_canvas.create_text(150, 275, text = 'CADE', font=("Arial black", 60, 'bold italic'), fill='white')
        self.my_canvas.create_text(90, 325, text = 'All your records at the click of a button.', font=("Arial black", 12), fill='white', anchor='nw')

        # Add buttons
        login_button = CustomButton(self, 'Login', 25, 1, 12, lambda: controller.show_frame(Login))
        signup_button = CustomButton(self, 'Sign Up', 25, 1, 12, lambda: controller.show_frame(SignUp))
        # Button windows
        login_button_window = self.my_canvas.create_window(540, 370, anchor= 'nw', window=login_button)
        signup_button_window = self.my_canvas.create_window(820, 370, anchor= 'nw', window=signup_button)

        '''
        # Glitches the transition from login screen to dashboard (tiny but noticeable)

        # Binding
        self.bind('<Configure>', self.resizer)

    def resizer(self, e):
        # Open our image
        self.bg1 = Image.open("images/lib1.jpg")
        # Resize the image

        self.resized_bg = self.bg1.resize((e.width, e.height), Image.ANTIALIAS)
        # Define our image again
        self.new_img = ImageTk.PhotoImage(self.resized_bg)
        # Add it back to the canvas
        self.my_canvas.create_image(0,0, image=self.new_img, anchor='nw')
        # Add text back
        self.my_canvas.create_text(180, 330, text = 'SIMS ', font=("Arial black", 40, 'bold italic'), fill='white')
        '''

    def menubar(self, root):
        # Just so this frame doesn't show a menu bar
        menubar = tk.Menu(root)
        return(menubar)

class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Image import
        self.img = Image.open("images/lib2.jpg")
        self.img = self.img.resize((controller.winfo_screenwidth(), controller.winfo_screenheight()))

        # There is the need to specify the master tk instance since ImageTK is also an instance of tkinter's Tk class
        self.img = ImageTk.PhotoImage(self.img, master=self)
        # Define canvas
        self.my_canvas = tk.Canvas(self)
        self.my_canvas.pack(side='top', fill='both', expand=True)
        # Put the image on the canvas
        self.my_canvas.create_image(0,0, image=self.img, anchor='nw')
        # Add labels
        self.my_canvas.create_text(510, 268, text = 'Enter your username.', font=("Arial black", 12, 'italic'), fill='white', anchor='nw')
        self.my_canvas.create_text(510, 338, text = 'Enter your password.', font=("Arial black", 12, 'italic'), fill='white', anchor='nw')
        self.my_canvas.create_text(510, 408, text = 'Retype password.', font=("Arial black", 12, 'bold italic'), fill='white', anchor='nw')

        # Variables
        self.temp_username = tk.StringVar()
        self.temp_password = tk.StringVar()
        self.temp_confirm_password = tk.StringVar()
       # Add entry boxes
        self.username_entry = tk.Entry(self, textvariable=self.temp_username, font=('Helvetica', 18), width=30, fg="#54aeff", bd=0)
        self.password_entry = tk.Entry(self, textvariable=self.temp_password, show='*', font=('Helvetica', 18), width=30, fg="#54aeff", bd=0)
        self.confirm_password_entry = tk.Entry(self, textvariable=self.temp_confirm_password, show='*', font=('Helvetica', 18), width=30, fg="#54aeff", bd=0)
        # Create event binding: Bind confirm_password_entry to <Return> and register function
        self.confirm_password_entry.bind('<Return>', self.register)

        # Add buttons
        sign_up_button=CustomButton(self, 'CREATE ACCOUNT', 48, 2, 12, self.register)
        login_button=ttk.Button(self, text='Login', width=20,
                          command=lambda: controller.show_frame(Login))
        back_to_home_button=ttk.Button(self, text='Back to Home', width=20,
                          command=lambda: controller.show_frame(StartPage))

        # Create button windows
        username_entry_window = self.my_canvas.create_window(510, 290, anchor= 'nw', window=self.username_entry)
        pw_entry_window = self.my_canvas.create_window(510, 360, anchor= 'nw', window=self.password_entry)
        confirm_pw_entry_window = self.my_canvas.create_window(510, 430, anchor= 'nw', window=self.confirm_password_entry)
        sign_up_button_window = self.my_canvas.create_window(510, 500, anchor= 'nw', window=sign_up_button)
        login_button_window = self.my_canvas.create_window(1000, 50, anchor= 'nw', window=login_button)
        back_to_home_button_window = self.my_canvas.create_window(1150, 50, anchor= 'nw', window=back_to_home_button)

    def register(self):
        # Validation
        if self.temp_password.get() != self.temp_confirm_password.get():
            messagebox.showerror('Password Error', 'Your passwords do not match.')
            return

        # Create a list from file names in the directory
        list_of_files = os.listdir()
        # Check if a file named single user has already been created. App's file of login name and passwords will be named single user
        if 'single user' not in list_of_files:
            username_info = self.temp_username.get()
            password_info = self.temp_password.get()
            # Create file to store login name and passwords named single user
            file = open('single user', 'w')
            file.write(username_info+'\n')
            file.write(password_info)
            file.close()
            # Clear user entries
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            messagebox.showinfo('', 'Registration successful. \n \n Click login to log into your account')
        else:
            messagebox.showerror('', 'Registration unsuccessful.')


    def menubar(self, root):
        # Just so this frame doesn't show a menu bar
        menubar = tk.Menu(root)
        return(menubar)

class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Define controller so it can be used in login_check event function
        self.controller = controller
        # Image import
        self.img = Image.open("images/lib3.jpg")
        self.img = self.img.resize((controller.winfo_screenwidth(), controller.winfo_screenheight()))

        # There is the need to specify the master tk instance since ImageTK is also an instance of tkinter's Tk class
        self.img = ImageTk.PhotoImage(self.img, master=self)

        # Define canvas
        self.my_canvas = tk.Canvas(self)
        self.my_canvas.pack(side='top', fill='both', expand=True)

        # Put the image on the canvas
        self.my_canvas.create_image(0,0, image=self.img, anchor='nw')

        # Add label
        self.my_canvas.create_text(510, 256, text = 'Enter your username.', font=("Arial black", 12, 'bold italic'), fill='white', anchor='nw')
        self.my_canvas.create_text(510, 326, text = 'Enter your password.', font=("Arial black", 12, 'bold italic'), fill='white', anchor='nw')

        # Variables
        self.temp_login_name = tk.StringVar()
        self.temp_login_password = tk.StringVar()
        self.login_attempt = 0

        # Add entry
        self.username_entry1 = tk.Entry(self, textvariable=self.temp_login_name, font=('Helvetica', 18), width=30, fg="#54aeff", bd=0)
        self.password_entry1 = tk.Entry(self, textvariable=self.temp_login_password, show='*', font=('Helvetica', 18), width=30, fg="#54aeff", bd=0)
        # Bind password_entry1 to <Return> and login_check function
        # self.password_entry1.bind('<Return>', self.login_check)

        # Buttons
        login_button = CustomButton(self, 'SIGN IN', 48, 2, 12,
                                    lambda : controller.show_frame(Dashboard) if self.verify_login() == 1 else messagebox.showerror('', 'Login Unsuccessful.'))#self.verify_login)
        back_to_home_button=ttk.Button(self, text='Back to Home', width=20,
                          command=lambda: controller.show_frame(StartPage))
        sign_up_button=ttk.Button(self, text='Sign Up', width=20,
                          command=lambda: controller.show_frame(SignUp))

        # Create button windows on canvas
        username_entry_window = self.my_canvas.create_window(510, 278, anchor= 'nw', window=self.username_entry1)
        pw_entry_window = self.my_canvas.create_window(510, 348, anchor= 'nw', window=self.password_entry1)
        login_button_window = self.my_canvas.create_window(510, 448, anchor= 'nw', window=login_button)
        sign_up_button_window = self.my_canvas.create_window(1000, 50, anchor= 'nw', window=sign_up_button)
        back_to_home_button_window = self.my_canvas.create_window(1150, 50, anchor= 'nw', window=back_to_home_button)

    def verify_login(self):
        # check if login username entry matches username and if login password entry matches password
        with open("env", "r") as file:
            file_data = file.read()

        file_data = file_data.split('\n')

        # Validation
        # Check if login name entered matches stored login name
        if self.temp_login_name.get() == file_data[0]:
            # Case where password entered matches stored password
            if self.temp_login_password.get() == file_data[1]:
                # Set the variable to be returned
                self.login_attempt = 1
                # Clear user's entries from input bar after login button is clicked
                self.clear_entry()
            else:
                # Password entered does not match stored password
                messagebox.showerror('Password Error', 'Incorrect password.')
                # Clear user's entries from input bar after message popup button is clicked
                self.clear_entry()
                return

            '''
            For additional user logins

            # Login button will have nested lamda function as command
            command= lambda : controller.show_frame(Dashboard) if self.verify_login() == 1 else (controller.show_frame(Admin) if self.verify_login == 2 else messagebox.showerror('', 'Login Unsuccessful.')))


        elif self.temp_login_name.get() == file_data[2]: # Where second user's name is file_data[2]
            if self.temp_login_password.get() == file_data[3]: # Second user's password is file_data[3]
               self.login_attempt = 2
               # clear user's entries from input bar after login button is clicked
               # self.clear_entry()
            else:
                messagebox.showerror('Password Error', 'Incorrect password.')
                # clear user's entries from input bar after message popup button is clicked
                self.clear_entry()
                return
            '''
        else:
            # Login name entered does not match stored login name
            self.login_attempt = 0
            #messagebox.showerror('Account Error', 'No account found!')
        return self.login_attempt

    def clear_entry(self):
        self.username_entry1.delete(0, tk.END)
        self.password_entry1.delete(0, tk.END)

    def login_check(self, event):
        if self.verify_login() == 1:
            self.controller.show_frame(Dashboard)
        else:
            messagebox.showerror('', 'Login Unsuccessful.')

    def menubar(self, root):
        # Just so this frame doesn't show a menu bar
        menubar = tk.Menu(root)
        return(menubar)
