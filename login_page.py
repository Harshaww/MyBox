from tkinter import PhotoImage
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
from PIL import Image, ImageTk
import csv  # Importing the CSV module
import os
from user_data import set_current_user, load_wishlist

class LoginWindow:
    def __init__(self, parent, navigate_to_page):
        """
        Initialize the login window.

        :param parent: The parent frame or container.
        :param navigate_to_page: Function to navigate to specific pages.
        """
        self.parent = parent

        # Theme variable for toggle
        self.theme_var = ttk.StringVar(value="dark")  # Default theme is dark
        style = self.parent.master.style
        style.theme_use("darkly")

        # Top Frame: Date, Time, Theme Toggle
        self.top_frame = ttk.Frame(self.parent)
        self.top_frame.pack(fill=X, pady=10)
        self.datetime_label = ttk.Label(self.top_frame, font=("Arial", 10))
        self.datetime_label.pack(side=LEFT, padx=20)
        self.update_datetime()

        self.theme_toggle = ttk.Checkbutton(
            self.top_frame,
            text="Light Mode",
            variable=self.theme_var,
            onvalue="light",
            offvalue="dark",
            command=self.toggle_theme
        )
        self.theme_toggle.pack(side=RIGHT, padx=20)

        # Center Container: Logo and Login Form
        self.center_container = ttk.Frame(self.parent)
        self.center_container.pack(expand=True)

        # Logo Frame
        self.logo_frame = ttk.Frame(self.center_container)
        self.logo_frame.pack(pady=20)

        try:
            logo_path = r"C:\\Users\\harsh\\OneDrive\\Desktop\\final_project\\Screenshot_20241116_102301_Samsung Notes.jpg"
            image = Image.open(logo_path)
            max_size = (400, 400)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(image)
            self.logo_label = ttk.Label(self.logo_frame, image=self.logo_img)
            self.logo_label.pack()
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo_label = ttk.Label(self.logo_frame, text="IMDB LOGO")
            self.logo_label.pack()

        # Login Frame
        self.login_frame = ttk.Frame(self.center_container)
        self.login_frame.pack(pady=20)

        # Login Label
        ttk.Label(
            self.login_frame,
            text="Login",
            font=("Arial", 24, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username
        ttk.Label(self.login_frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        self.add_placeholder(self.username_entry, "Enter Username")

        # Password
        ttk.Label(self.login_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.login_frame, show="*", width=30)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        self.add_placeholder(self.password_entry, "Enter Password", is_password=True)

        # Login Button
        ttk.Button(
            self.login_frame,
            text="Login",
            style="primary.TButton",
            width=15,
            command=lambda: self.save_credentials_and_navigate(navigate_to_page)
        ).grid(row=3, column=0, columnspan=2, pady=20)

        # Register Button
        ttk.Button(
            self.login_frame,
            text="New to IMDB? Register now!",
            style="info.TButton",
            width=25,
            command=lambda: navigate_to_page(1)
        ).grid(row=4, column=0, columnspan=2, pady=10)

    def update_datetime(self):
        """Update the date and time label."""
        current_date = datetime.now().strftime("%d %B, %Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        self.datetime_label.config(text=f"{current_date}\n{current_time}")
        self.parent.after(1000, self.update_datetime)

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        style = self.parent.master.style
        if self.theme_var.get() == "light":
            style.theme_use("litera")
            self.theme_toggle.config(text="Dark Mode")
        else:
            style.theme_use("darkly")
            self.theme_toggle.config(text="Light Mode")

    def add_placeholder(self, entry, placeholder, is_password=False):
        """
        Add a placeholder to a ttk.Entry widget.

        :param entry: The entry widget.
        :param placeholder: The placeholder text.
        :param is_password: Whether the entry is a password field.
        """
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                if is_password:
                    entry.config(show="*")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                if is_password:
                    entry.config(show="")

        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def save_credentials_and_navigate(self, navigate_to_page):
        """
        Validate the entered username and password, then save to last_login.csv if correct and navigate to another page.

        :param navigate_to_page: Function to navigate to specific pages.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "Enter Username" or password == "Enter Password" or not username or not password:
            self.show_error("Username or password cannot be empty.")
            return

        if not os.path.exists("username_password.csv"):
            self.show_error("User data file not found. Please register first.")
            return

        try:
            with open("username_password.csv", "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) >= 2:
                        saved_username, saved_password = row[0], row[1]
                        if username == saved_username and password == saved_password:
                            with open("last_login.csv", "w", newline="") as last_login_file:
                                writer = csv.writer(last_login_file)
                                writer.writerow([username, password])
                            # Set the global `current_username` and load the wishlist
                            global current_username
                            current_username = username
                            load_wishlist()

                            print("Login successful! Credentials saved to last_login.csv.")
                            navigate_to_page(2)
                            return
                self.show_error("Incorrect username or password.")
        except Exception as e:
            self.show_error(f"An error occurred: {e}")


    def show_error(self, message):
        """
        Display an error message below the login form.

        :param message: The error message to display.
        """
        if hasattr(self, "error_label"):
            self.error_label.config(text=message)
        else:
            self.error_label = ttk.Label(
                self.login_frame,
                text=message,
                font=("Arial", 10),
                foreground="red",
                wraplength=300
            )
            self.error_label.grid(row=5, column=0, columnspan=2, pady=10)
