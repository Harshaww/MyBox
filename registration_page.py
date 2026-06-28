from tkinter import PhotoImage, StringVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from datetime import datetime
from PIL import Image, ImageTk
import re
import csv
import os

class RegistrationWindow:
    def __init__(self, parent, navigate_to_page):
        """
        Initialize the Registration Page inside the given parent frame.

        :param parent: The parent frame where widgets will be added.
        :param navigate_to_page: Function to navigate to another page by index.
        """
        self.parent = parent
        self.navigate_to_page = navigate_to_page  # Navigation function

        self.parent.title = "New User Registration"
        # Theme variable for toggle
        self.theme_var = ttk.StringVar(value="light")

        # Configure grid for responsiveness
        for i in range(2):
            self.parent.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.parent.grid_columnconfigure(i, weight=1)

        # Top frame
        self.top_frame = ttk.Frame(self.parent)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        for i in range(2):
            self.top_frame.grid_columnconfigure(i, weight=1)

        # Company logo on the left
        try:
            logo_path = r"C:\Users\harsh\OneDrive\Desktop\final_project\Screenshot_20241116_102301_Samsung Notes.jpg"
            image = Image.open(logo_path)
            max_size = (300, 300)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(image)
            self.logo_label = ttk.Label(self.top_frame, image=self.logo_img)
            self.logo_label.grid(row=0, column=0, sticky="w", padx=20)
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo_label = ttk.Label(self.top_frame, text="Company Logo", font=("Arial", 16))
            self.logo_label.grid(row=0, column=0, sticky="w", padx=20)

        # Page title in the center
        self.title_label = ttk.Label(self.top_frame, text="New User Registration",
                                     font=("Arial", 28, "bold"))
        self.title_label.grid(row=0, column=1, sticky="ew", pady=20)

        # Center container frame
        self.center_container = ttk.Frame(self.parent)
        self.center_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        self.center_container.grid_rowconfigure(0, weight=1)
        self.center_container.grid_columnconfigure(0, weight=1)

        self.theme_toggle = ttk.Checkbutton(
            self.top_frame,
            text="Light Mode",
            variable=self.theme_var,
            onvalue="dark",
            offvalue="light",
            command=self.toggle_theme
        )
        self.theme_toggle.grid(row=0, column=2, sticky="e")

        # Registration form
        self.registration_frame = ttk.Frame(self.center_container)
        self.registration_frame.grid(row=0, column=0, padx=20, pady=20)

        # Labels and input fields
        self.fields = {
            "First Name*:": ttk.Entry(self.registration_frame, width=30),
            "Middle Name:": ttk.Entry(self.registration_frame, width=30),
            "Last Name*:": ttk.Entry(self.registration_frame, width=30),
            "Gender:": ttk.Combobox(self.registration_frame, values=["Keep Private", "Male", "Female", "Other"], width=28),
            "Email ID*:": ttk.Entry(self.registration_frame, width=30),
            "Contact Number*:": ttk.Entry(self.registration_frame, width=30),
            "Date of Birth* (DD/MM/YYYY):": ttk.Entry(self.registration_frame, width=30),
            "Username*:": ttk.Entry(self.registration_frame, width=30),
            "Password*:": ttk.Entry(self.registration_frame, show="*", width=30),
        }

        current_row = 0
        for label_text, widget in self.fields.items():
            label = ttk.Label(self.registration_frame, text=label_text, font=("Arial", 12))
            label.grid(row=current_row, column=0, padx=10, pady=8, sticky="e")
            widget.grid(row=current_row, column=1, padx=10, pady=8, sticky="w")

            # Make the entry fields more prominent
            if isinstance(widget, ttk.Entry):
                widget.configure(font=("Arial", 11))
            elif isinstance(widget, ttk.Combobox):
                widget.configure(font=("Arial", 11))

            current_row += 1

        # Age output box
        self.age_var = StringVar(value="Age will appear here")
        self.age_output = ttk.Entry(
            self.registration_frame,
            textvariable=self.age_var,
            state="readonly",
            width=20,
            font=("Arial", 11)
        )
        self.age_output.grid(row=current_row, column=1, padx=10, pady=8, sticky="w")

        # Bind the date of birth field to validate and update age
        self.fields["Date of Birth* (DD/MM/YYYY):"].bind('<FocusOut>', self.validate_and_update_age)

        current_row += 1

        # Checkbox for terms and conditions
        self.checkbox_var = ttk.IntVar()
        self.terms_checkbox = ttk.Checkbutton(
            self.registration_frame,
            text="I agree to the terms and conditions",
            variable=self.checkbox_var,
            style='primary.TCheckbutton'
        )
        self.terms_checkbox.grid(row=current_row, column=0, columnspan=2, pady=15)

        current_row += 1

        # Submit button
        self.submit_button = ttk.Button(
            self.registration_frame,
            text="Submit",
            style="primary.TButton",
            command=self.submit_form,
            width=20
        )
        self.submit_button.grid(row=current_row, column=0, columnspan=2, pady=15)

        current_row += 1

        # Back to Login button
        self.back_button = ttk.Button(
            self.registration_frame,
            text="Back to Login",
            style="link.TButton",
            command=lambda: self.navigate_to_page(0)  # Navigate to Login Page
        )
        self.back_button.grid(row=current_row, column=0, columnspan=2, pady=10)

        # Error message label
        self.error_label = ttk.Label(
            self.registration_frame,
            text="",
            font=("Arial", 11),
            foreground="red",
            wraplength=400
        )
        self.error_label.grid(row=current_row + 1, column=0, columnspan=2, pady=10)

    def validate_date_format(self, date_str):
        """Validate the date format (DD/MM/YYYY)."""
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            return None

    def validate_and_update_age(self, event=None):
        """Validate date format and update age when date of birth field loses focus."""
        date_str = self.fields["Date of Birth* (DD/MM/YYYY):"].get().strip()
        if date_str:
            date_obj = self.validate_date_format(date_str)
            if date_obj:
                age = self.calculate_age(date_obj)
                if age is not None:
                    if age < 13:
                        self.age_var.set(f"Age: {age} (Must be 13+)")
                    else:
                        self.age_var.set(f"Age: {age} years")
                else:
                    self.age_var.set("Invalid date")
            else:
                self.age_var.set("Invalid format")
        else:
            self.age_var.set("Age will appear here")

    def validate_email(self, email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        """Validate phone number format."""
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None

    def calculate_age(self, birth_date):
        """Calculate age based on the birth date."""
        if birth_date:
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        return None

    def validate_password(self, password):
        """Validate the password requirements."""
        if len(password) < 8:
            return "Password must be at least 8 characters long."
        if not any(char.isupper() for char in password):
            return "Password must have at least one uppercase letter."
        if not any(char.islower() for char in password):
            return "Password must have at least one lowercase letter."
        if not any(char.isdigit() for char in password):
            return "Password must have at least one digit."
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in password):
            return "Password must have at least one special character."
        return None

    def is_username_taken(self, username):
        """Check if the username already exists in the CSV file."""
        try:
            with open("username_password.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == username:
                        return True
        except FileNotFoundError:
            pass
        return False

    def submit_form(self):
        """Handle the form submission."""
        errors = []
        required_fields = ["First Name*:", "Last Name*:", "Email ID*:", "Contact Number*:", "Date of Birth* (DD/MM/YYYY):", "Username*:", "Password*:"]

        # Check for required fields
        for field in required_fields:
            if not self.fields[field].get().strip():
                errors.append(f"{field[:-1]} is required.")

        username = self.fields["Username*:"].get().strip()
        if username and self.is_username_taken(username):
            errors.append("This username is already taken. Please choose another.")

        email = self.fields["Email ID*:"].get().strip()
        if email and not self.validate_email(email):
            errors.append("Invalid email format.")

        phone = self.fields["Contact Number*:"].get().strip()
        if phone and not self.validate_phone(phone):
            errors.append("Invalid phone number.")

        password = self.fields["Password*:"].get().strip()
        password_error = self.validate_password(password)
        if password_error:
            errors.append(password_error)

        age_text = self.age_var.get()
        if age_text.startswith("Age:") and "Must be 13+" in age_text:
            errors.append("You must be at least 13 years old to register.")

        if not self.checkbox_var.get():
            errors.append("You must agree to the terms and conditions.")

        if errors:
            self.error_label.config(text="\n".join(errors))
        else:
            # Save the username and password to the common CSV file
            try:
                with open("username_password.csv", mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([username, password])
            except Exception as e:
                Messagebox.show_error("Error", f"Failed to save user data: {e}")
                return

            # Save individual user data into a file named after the username
            user_data = {
                "First Name": self.fields["First Name*:"].get().strip(),
                "Middle Name": self.fields["Middle Name:"].get().strip(),
                "Last Name": self.fields["Last Name*:"].get().strip(),
                "Gender": self.fields["Gender:"].get(),
                "Email ID": self.fields["Email ID*:"].get().strip(),
                "Contact Number": self.fields["Contact Number*:"].get().strip(),
                "Date of Birth": self.fields["Date of Birth* (DD/MM/YYYY):"].get().strip(),
                "Username": username,
                "Password": password ,
            }

            # Create a directory to store individual user files (if not already existing)
            user_dir = "user_data"
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            # Create a file for the user with the username as filename
            user_file_path = os.path.join(user_dir, f"{username}.txt")

            try:
                with open(user_file_path, mode="w", newline="") as file:
                    for key, value in user_data.items():
                        file.write(f"{key}: {value}\n")
            except Exception as e:
                Messagebox.show_error("Error", f"Failed to save individual user data: {e}")
                return

            Messagebox.show_info("Success", "Registration Successful! Returning to Login.")
            self.navigate_to_page(0)  # Navigate to Login Page

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        if self.theme_var.get() == "dark":
            self.parent.style.theme_use("darkly")
        else:
            self.parent.style.theme_use("flatly")