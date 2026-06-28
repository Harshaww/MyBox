import csv
import os
import tkinter as tk


def show_user_profile(dashboard_frame):
    """
    Display the user's profile in a popup window by dynamically loading data from the corresponding username.txt file.
    Instead of checking username_password.csv, it will check last_login.csv.
    """
    try:
        # Step 1: Get the last username and password from the last_login.csv file
        username = None
        password = None

        # Get the path to the current directory where user_profile.py is stored
        script_directory = os.path.dirname(__file__)  # Current script directory
        last_login_file = os.path.join(script_directory, "last_login.csv")  # Path to last_login.csv

        # Read the CSV file and get the first row (last logged-in username and password)
        if os.path.exists(last_login_file):
            with open(last_login_file, "r") as file:
                reader = csv.reader(file)
                rows = list(reader)
                if rows:
                    # Get the first row (most recent login)
                    username = rows[0][0].strip()  # First column is the username
                    password = rows[0][1].strip()  # Second column is the password
        else:
            print(f"Error: {last_login_file} not found.")
            return

        if not username:
            print("No username found in last_login.csv.")
            return

        # Step 2: Get the path of the 'user_data' directory (where username.txt files are stored)
        user_data_directory = os.path.join(script_directory, 'user_data')  # Path to the user_data folder
        user_file = os.path.join(user_data_directory, f"{username}.txt")  # Path to the username.txt file

        user_data = None
        if os.path.exists(user_file):
            user_data = {}
            with open(user_file, "r") as file:
                for line in file:
                    # Assuming each line in the text file is in the format "key: value"
                    parts = line.strip().split(":")
                    if len(parts) == 2:
                        key, value = parts
                        user_data[key.strip()] = value.strip()
        else:
            print(f"Error: The file {user_file} could not be found.")
            return

        # Step 3: Create a popup window to display the profile in grid format
        profile_window = tk.Toplevel(dashboard_frame)
        profile_window.title("User Profile")
        profile_window.geometry("400x500")  # Adjust size to fit all content
        profile_window.configure(bg="#000000")

        # Title Label
        tk.Label(
            profile_window, text="User Profile", font=("Helvetica", 16, "bold"),
            bg="#000000", fg="white"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Step 4: Display user details dynamically in a grid
        if user_data:
            row = 1
            for key, value in user_data.items():
                tk.Label(
                    profile_window,
                    text=f"{key}: {value}",
                    font=("Helvetica", 12),
                    bg="#000000",
                    fg="white"
                ).grid(row=row, column=0, sticky="w", padx=20, pady=5)
                row += 1


        # Close Button
        tk.Button(
            profile_window,
            text="Close",
            command=profile_window.destroy,
            bg="red",
            fg="white"
        ).grid(row=row + 1, column=0, columnspan=2, pady=10)

    except Exception as e:
        print(f"An error occurred: {e}")