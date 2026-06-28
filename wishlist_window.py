import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Button
from PIL import Image, ImageTk
import os
import json  # For saving/loading wishlist as JSON
import csv  # For reading the last logged-in user's username

# Path to the directory where user-specific wishlist JSONs will be stored
USER_DATA_DIR = "user_data"
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)


# Get the username from the last_login.csv file
def get_last_logged_in_user():
    try:
        with open('last_login.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Assuming the CSV contains [username, password] on the first row
            for row in reader:
                return row[0]  # Return the username (first column)
    except FileNotFoundError:
        print("Error: last_login.csv not found.")
        return None
    except Exception as e:
        print(f"Error reading last_login.csv: {e}")
        return None


# Get the current logged-in username
current_username = get_last_logged_in_user()
print(f"Current logged-in user: {current_username}")  # Debug print

# Initialize wishlist (load data if available)
wishlist = []


# Load the wishlist for the logged-in user
def load_wishlist():
    """Load the wishlist from the JSON file for the current user."""
    global wishlist
    if current_username:
        wishlist_file = os.path.join(USER_DATA_DIR, f"{current_username}_wishlist.json")
        print(f"Looking for wishlist file: {wishlist_file}")  # Debug print

        if os.path.exists(wishlist_file):
            try:
                with open(wishlist_file, mode="r", encoding="utf-8") as file:
                    wishlist = json.load(file)
                    print(f"Wishlist loaded: {wishlist}")  # Debug print
            except Exception as e:
                print(f"Error loading wishlist: {e}")
        else:
            # If the file doesn't exist, create it with an empty wishlist
            print(f"No wishlist found for {current_username}. Creating a new wishlist.")
            save_wishlist()  # Create an empty wishlist JSON file
    else:
        print("No user logged in.")


# Save the wishlist for the logged-in user
def save_wishlist():
    """Save the wishlist to the JSON file for the current user."""
    if current_username:
        wishlist_file = os.path.join(USER_DATA_DIR, f"{current_username}_wishlist.json")
        print(f"Saving wishlist to: {wishlist_file}")  # Debug print
        try:
            with open(wishlist_file, mode="w", encoding="utf-8") as file:
                json.dump(wishlist, file, indent=4)
                print(f"Wishlist saved: {wishlist}")  # Debug print
        except Exception as e:
            print(f"Error saving wishlist: {e}")


def open_wishlist_window(parent, open_movie_details_callback):
    """Open a new window displaying wishlist movies with options to delete."""
    wishlist_window = tk.Toplevel(parent)
    wishlist_window.title("My Wishlist")
    wishlist_window.geometry("1000x800")
    style = Style(theme="darkly")

    # Frame for wishlist content
    content_frame = Frame(wishlist_window, padding=10)
    content_frame.pack(fill="both", expand=True)

    # Big Heading
    heading_label = Label(
        content_frame, text="My Wishlist",
        font=("Helvetica", 24, "bold"),
        bootstyle="primary"
    )
    heading_label.pack(pady=20)

    # Frame for movie posters and delete buttons
    movie_frame = Frame(content_frame)
    movie_frame.pack(fill="both", expand=True)

    # Display the wishlist content in the movie_frame
    display_wishlist_content(movie_frame, open_movie_details_callback)

    # Save the wishlist when the window is closed
    wishlist_window.protocol("WM_DELETE_WINDOW", lambda: close_wishlist_window(wishlist_window))



def display_wishlist_content(movie_frame, open_movie_details_callback):
    """Display movies in the wishlist in the given frame."""
    # Clear the frame before updating
    for widget in movie_frame.winfo_children():
        widget.destroy()

    if not wishlist:
        empty_label = Label(movie_frame, text="Your wishlist is empty.", font=("Helvetica", 16))
        empty_label.pack(pady=20)
        return

    for index, movie in enumerate(wishlist):
        # Frame for each movie
        movie_container = Frame(movie_frame, padding=5, bootstyle="secondary")
        movie_container.grid(row=index // 4, column=index % 4, padx=20, pady=20)

        # Movie Poster
        poster_path = movie.get("Poster", "placeholder.png")
        img = load_image(poster_path, (150, 225))
        if img:
            poster_label = Label(movie_container, image=img, cursor="hand2")
            poster_label.image = img
            poster_label.pack()
            poster_label.bind("<Button-1>", lambda e, title=movie["Title"]: open_movie_details_callback(title))

        # Movie Title
        title_label = Label(movie_container, text=movie["Title"], font=("Helvetica", 12, "bold"), wraplength=150)
        title_label.pack(pady=5)

        # Delete Button
        delete_button = Button(
            movie_container,
            text="Delete",
            bootstyle="danger-outline",
            command=lambda movie=movie: delete_movie(movie, movie_frame, open_movie_details_callback),
        )
        delete_button.pack()


def delete_movie(movie, movie_frame, open_movie_details_callback):
    """Delete a movie from the wishlist and refresh the frame."""
    global wishlist
    wishlist.remove(movie)  # Remove the movie from the wishlist
    save_wishlist()  # Save the updated wishlist
    display_wishlist_content(movie_frame, open_movie_details_callback)  # Refresh the frame content


def load_image(path, size):
    """Function to load and resize an image."""
    try:
        if not os.path.exists(path):
            path = "placeholder.png"  # Fallback to placeholder image
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None


# Close window and save wishlist
def close_wishlist_window(wishlist_window):
    """Save the wishlist when the window is closed."""
    save_wishlist()  # Save wishlist before closing
    wishlist_window.destroy()


# Initial loading of the wishlist
# load_wishlist()
