import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
import json
from line_vis import plot_movie_ratings  # Ensure this is correctly imported
from wishlist_window import wishlist  # Ensure this is correctly imported
from recommendation_window import open_recommendations

class ImageHandler:
    def __init__(self):
        self.default_image_path = "placeholder.png"  # Default image path if poster is missing

    def show_line_graph(self):
        """
        Trigger the line graph visualization by passing movie data.
        """
        try:
            title = self.movie_data.get("Title", "Unknown")
            year = int(self.movie_data.get("Year", 2020))  # Default to 2020 if Year is missing
            base_rating = float(self.movie_data.get("Rating", 5.0))  # Default to 5.0 if Rating is missing

            print(f"Preparing to plot graph for '{title}' ({year}) with base rating {base_rating}...")
            plot_movie_ratings(title, year, base_rating)
        except Exception as e:
            print(f"Error generating line graph: {e}")

    def load_and_resize_image(self, image_path: str, size: tuple) -> ImageTk.PhotoImage:
        """
        Load and resize the image to the specified size.
        """
        try:
            if not os.path.exists(image_path):
                image_path = self.default_image_path  # Use default if file not found
            image = Image.open(image_path)
            resized_image = image.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
        except Exception as e:
            blank = Image.new("RGB", size, "#2b2b2b")  # Fallback to blank image
            return ImageTk.PhotoImage(blank)


class MovieDetailsWindow:
    # Set this to your actual CSV path; dashboard_page.py may override it.
    CSV_PATH: str = r"/mnt/c/Users/sai harsha/Downloads/mybox/final_movie_data.csv"

    def __init__(self, parent, movie_data):
        """
        Initialize the Movie Details Window.
        """
        self.movie_data = movie_data  # Store movie data as instance variable
        self.parent = parent
        self.window = ttk.Toplevel(parent)
        self.window.title(movie_data["Title"])
        self.window.geometry("1250x900")
        self.window.resizable(True, True)  # Allow window to be resizable

        # Define custom styles
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Helvetica", 14), foreground="white", background="#333333")
        style.configure("Title.TLabel", font=("Helvetica", 26, "bold"), foreground="white", background="#333333")
        style.configure("Subtitle.TLabel", font=("Helvetica", 16), foreground="lightgray", background="#333333")
        style.configure("Rating.TLabel", font=("Helvetica", 20, "bold"), foreground="gold", background="#333333")
        style.configure("Genres.TLabel", font=("Helvetica", 14), foreground="lightgray", background="#333333")
        style.configure("Cast.TLabel", font=("Helvetica", 14), foreground="white", background="#333333")
        style.configure("Director.TLabel", font=("Helvetica", 14), foreground="white", background="#333333")
        style.configure("Synopsis.TLabel", font=("Helvetica", 14), foreground="white", background="#333333")

        self.create_ui(movie_data)

    def create_ui(self, movie_data):
        """
        Create the UI elements for the movie details window.
        """
        # Scrollable Content
        canvas = ttk.Canvas(self.window)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(self.window, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Main Frame
        content_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Update scrollregion dynamically
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Title Section
        title_frame = ttk.Frame(content_frame)
        title_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(
            title_frame,
            text=movie_data["Title"],
            style="Title.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(side=LEFT)

        ttk.Label(
            title_frame,
            text=f"({movie_data['Year']})",
            style="Subtitle.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(side=LEFT, padx=10)

        # Content Section
        content_frame_section = ttk.Frame(content_frame)
        content_frame_section.pack(fill=BOTH, expand=YES)

        # Image Section
        image_frame = ttk.Frame(content_frame_section)
        image_frame.grid(row=0, column=0, padx=(0, 20), sticky="nsew")

        movie_photo = ImageHandler().load_and_resize_image(movie_data["Poster"], (400, 600))
        image_label = ttk.Label(image_frame, image=movie_photo)
        image_label.image = movie_photo  # Keep reference
        image_label.pack()

        # Buttons
        ttk.Button(image_frame, text="Add to Wishlist", command=lambda:self.add_to_wishlist(movie_data)).pack(fill=X, pady=5)
        ttk.Button(image_frame, text="Show Line Graph", command=self.show_line_graph).pack(fill=X, pady=5)
        ttk.Button(
            image_frame,
            text="🎬 Similar Movies",
            bootstyle="success",
            command=self.open_recommendations_window,
        ).pack(fill=X, pady=5)

        # Details Section
        details_frame = ttk.Frame(content_frame_section)
        details_frame.grid(row=0, column=1, sticky="nsew")

        # Quick Info
        quick_info = ttk.Frame(details_frame)
        quick_info.pack(fill=X, pady=(0, 20))

        ttk.Label(
            quick_info,
            text=f"⭐ {movie_data['Rating']}",
            style="Rating.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(side=LEFT, padx=(0, 20))

        # Move Duration to a new line (next to Rating)
        ttk.Label(
            quick_info,
            text=f"Duration: {movie_data['Duration']}",
            style="Custom.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(side=LEFT, pady=(10, 0))

        # Additional Information
        additional_info = ttk.Frame(details_frame)
        additional_info.pack(fill=X, pady=(0, 20))

        ttk.Label(
            additional_info,
            text=f"Budget: {movie_data['Budget']}",
            style="Custom.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(anchor=W, pady=2)

        ttk.Label(
            additional_info,
            text=f"Gross: {movie_data['Gross']}",
            style="Custom.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(anchor=W, pady=2)

        ttk.Label(
            additional_info,
            text=f"Votes: {movie_data['Votes']}",
            style="Custom.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(anchor=W, pady=2)

        ttk.Label(
            additional_info,
            text=f"Certificate: {movie_data['Certificate']}",
            style="Custom.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(anchor=W, pady=2)

        # Genres Section
        genres_frame = ttk.Frame(details_frame)
        genres_frame.pack(fill=X, pady=(0, 20))

        for genre in movie_data["Genre"].split(", "):
            ttk.Label(
                genres_frame,
                text=genre,
                style="Genres.TLabel",
                padding=(10, 5),
                wraplength=800,  # Adjust wraplength to make the box responsive
                anchor=W
            ).pack(side=LEFT, padx=(0, 10))

        # Director Section with the same background as Cast
        details_list = ttk.Frame(details_frame)
        details_list.pack(fill=X, pady=(0, 20))

        ttk.Label(
            details_list,
            text=f"Director: {movie_data['Director']}",
            style="Director.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(anchor=W, pady=2)

        ttk.Label(
            details_list,
            text=f"Cast: {movie_data['Cast']}",
            style="Cast.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(anchor=W, pady=2)

        # Synopsis
        ttk.Label(
            details_frame,
            text="Synopsis",
            style="Subtitle.TLabel"
        ).pack(anchor=W, pady=(0, 10))

        ttk.Label(
            details_frame,
            text=movie_data["Synopsis"],
            style="Synopsis.TLabel",
            wraplength=800,  # Adjust wraplength to make the box responsive
            anchor=W
        ).pack(fill=X)

    def open_recommendations_window(self):
        """
        Open the recommendations window for the current movie.
        Uses the class-level CSV_PATH so it works without changes
        to the existing constructor signature.
        """
        title = self.movie_data.get("Title", "")
        open_recommendations(
            parent=self.window,
            movie_title=title,
            csv_path=MovieDetailsWindow.CSV_PATH,
            on_movie_click=None,  # Can wire to open details if needed
        )

    def add_to_wishlist(self, movie_data):
        """Add movie details to the wishlist."""
        # Create a movie entry with relevant information
        movie_entry = {"Title": movie_data["Title"], "Poster": movie_data["Poster"]}

        # Check if the movie is already in the wishlist
        if movie_entry not in wishlist:
            wishlist.append(movie_entry)  # Add the movie to the wishlist
            print(f"{movie_data['Title']} added to wishlist.")
        else:
            print(f"{movie_data['Title']} is already in the wishlist.")

    def show_line_graph(self):
        """
        Trigger the line graph visualization by passing movie data.
        """
        try:
            title = self.movie_data.get("Title", "Unknown")
            year = int(self.movie_data.get("Year", 2020))  # Default to 2020 if Year is missing
            base_rating = float(self.movie_data.get("Rating", 5.0))  # Default to 5.0 if Rating is missing

            print(f"Preparing to plot graph for '{title}' ({year}) with base rating {base_rating}...")
            plot_movie_ratings(title, year, base_rating)
        except Exception as e:
            print(f"Error generating line graph: {e}")
