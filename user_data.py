import os
import json
import csv

USER_DATA_DIR = "user_data"
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

current_username = None
wishlist = []


def get_last_logged_in_user():
    """Fetch the last logged-in user from the CSV file."""
    try:
        with open('last_login.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                return row[0]  # Return the username
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading last_login.csv: {e}")
        return None


def set_current_user(username):
    """Set the current logged-in user and load their wishlist."""
    global current_username
    current_username = username
    load_wishlist()


def load_wishlist():
    """Load the wishlist for the current user."""
    global wishlist
    if current_username:
        wishlist_file = os.path.join(USER_DATA_DIR, f"{current_username}_wishlist.json")
        if os.path.exists(wishlist_file):
            try:
                with open(wishlist_file, mode="r", encoding="utf-8") as file:
                    wishlist = json.load(file)
            except Exception as e:
                print(f"Error loading wishlist: {e}")
        else:
            wishlist = []
            save_wishlist()  # Create an empty wishlist JSON file


def save_wishlist():
    """Save the wishlist for the current user."""
    if current_username:
        wishlist_file = os.path.join(USER_DATA_DIR, f"{current_username}_wishlist.json")
        try:
            with open(wishlist_file, mode="w", encoding="utf-8") as file:
                json.dump(wishlist, file, indent=4)
        except Exception as e:
            print(f"Error saving wishlist: {e}")
