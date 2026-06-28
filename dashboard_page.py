global scrollable_frame
import pandas as pd
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Entry, Button, Menubutton
from PIL import Image, ImageTk
import os
from movie_data import MovieDetailsWindow, ImageHandler
from search_movie import search_movies
from wishlist_window import open_wishlist_window
from Visualizer1 import Visualizer1
from Visualizer2 import Visualizer2
from Visualizer3 import Visualizer3
from Visualizer4 import Visualizer4
from search_movie import filter_by_year, filter_by_genre
from Report_window import open_report
from recommender import preload as _preload_recommender
from movie_data import MovieDetailsWindow as _MDW
from user_profile import show_user_profile

def display_dashboard(dashboard_frame, navigate_to_page):
    """
    Function to display the dashboard UI elements with fixed layout issues.
    """

    # Initialize style
    style = Style(theme="darkly")
    style.configure("Custom.TFrame", background="#000000")
    style.configure("Custom.TLabel", background="#000000", foreground="white")
    style.configure("Custom.TButton", background="#000000", foreground="white")
    style.configure("Custom.TMenubutton", background="#000000", foreground="white")
    style.configure("Highlighted.TLabel", background="white", foreground="black")

    # Load CSV Data
    csv_path = r"/mnt/c/Users/sai harsha/Downloads/mybox/final_movie_data.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")

    # Make the CSV path available to MovieDetailsWindow and pre-fit the recommender
    _MDW.CSV_PATH = csv_path
    _preload_recommender(csv_path)

    data = pd.read_csv(csv_path)
    top_movies = data.head(12)
    def clear_last_login_file():
    # """Clears the content of the last_login.txt file."""
        try:
            with open("last_login.csv", "w") as file:
                file.truncate(0)  # Clear the file content
        except Exception as e:
            print(f"Error clearing last_login.txt: {e}")


    def logout_and_clear_last_login():
        """Handles logout and clears the last login file."""
        clear_last_login_file()
        navigate_to_page(0)  # Navigate to the login page or the main page

    def show_main_dashboard():
        """Show the main dashboard content and hide search results"""
        # Clear search bar
        search_var.set("")

        # First clear all widgets in main content area
        for widget in main_frame.winfo_children():
            widget.destroy()

        # Recreate the main dashboard layout
        create_dashboard_layout()
        back_button.pack_forget()
        update_movie_display(top_movies, show_all=True)

    def open_report_window():
        """Function to open the report window"""
        import Report_window  # Assuming 'report_window.py' is the file where you want to handle the report window
        open_report(dashboard_frame)  # Call a function from the 'report_window.py' file that opens the report window

    # User dropdown menu
    def open_user_profile():
        """
        Open the user profile in a new window.
        """
        show_user_profile(dashboard_frame)  # Call the function from user_profile.py

    def show_year_range_menu():
        """Display year range options when 'Year' is selected."""
        year_range_menu = tk.Menu(dashboard_frame, tearoff=0, bg="#000000", fg="white")

        # Add year range options to the dropdown
        year_ranges = [
            "1950-1970", "1970-1980", "1980-1990", "1990-2000",
            "2000-2010", "2010-2020", "2020-2024"
        ]
        for year_range in year_ranges:
            year_range_menu.add_command(
                label=year_range,
                command=lambda year_range=year_range: on_year_range_selected(year_range)
            )

        # Show the year range menu
        year_range_menu.post(40, 350)  # Positioning at top left of dashboard

    def on_genre_selected(genre):
        """
        Handle genre selection, filter movies by the selected range,
        and display them in a grid with a maximum of 6 movies per row.
        """
        filtered_movies = filter_by_genre(genre)  # Use the filter_by_year function

        # Clear the scrollable frame (movie display)
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if not filtered_movies.empty:
            # No text, only the movie posters will be shown
            filtered_movies = filtered_movies.head(12)

            # Define max columns (6 movies per row)
            max_columns = 6

            # Calculate the number of rows required (round up if necessary)
            rows_required = (len(filtered_movies) + max_columns - 1) // max_columns  # Round up division

            for index, movie in filtered_movies.iterrows():
                row = index // max_columns  # Calculate row number based on index
                col = index % max_columns  # Calculate column within the row

                poster_path = movie.get("Poster", "default_poster.jpg")  # Use default if missing
                img = load_image(poster_path, (330, 425))  # Resize poster

                if img:
                    poster_label = Label(
                        scrollable_frame,
                        image=img,
                        style="Custom.TLabel",
                        cursor="hand2"
                    )
                    poster_label.image = img  # Prevent garbage collection
                    poster_label.grid(row=row, column=col, padx=35, pady=15)  # Adjust padding for better spacing
                    poster_label.bind(
                        "<Button-1>",
                        lambda e, title=movie["Title"]: open_movie_details(title)
                    )

            # Show back to dashboard button
            back_button.pack(side="top", pady=10)

        else:
            # Handle no movies found
            no_movies_label = Label(
                scrollable_frame,
                text="No movies found for this genre.",
                style="Error.TLabel"
            )
            no_movies_label.grid(row=0, column=0, pady=20, padx=20)

            # Show back to dashboard button
            back_button.pack(side="top", pady=10)

    def on_year_range_selected(year_range):
        """
        Handle year range selection, filter movies by the selected range,
        and display them in a grid with a maximum of 6 movies per row.
        """
        filtered_movies = filter_by_year(year_range)  # Use the filter_by_year function

        # Clear the scrollable frame (movie display)
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if not filtered_movies.empty:
            # No text, only the movie posters will be shown
            filtered_movies = filtered_movies.head(12)

            # Define max columns (6 movies per row)
            max_columns = 6

            # Calculate the number of rows required (round up if necessary)
            rows_required = (len(filtered_movies) + max_columns - 1) // max_columns  # Round up division

            for index, movie in filtered_movies.iterrows():
                row = index // max_columns  # Calculate row number based on index
                col = index % max_columns  # Calculate column within the row

                poster_path = movie.get("Poster", "default_poster.jpg")  # Use default if missing
                img = load_image(poster_path, (330, 425))  # Resize poster

                if img:
                    poster_label = Label(
                        scrollable_frame,
                        image=img,
                        style="Custom.TLabel",
                        cursor="hand2"
                    )
                    poster_label.image = img  # Prevent garbage collection
                    poster_label.grid(row=row, column=col, padx=35, pady=15)  # Adjust padding for better spacing
                    poster_label.bind(
                        "<Button-1>",
                        lambda e, title=movie["Title"]: open_movie_details(title)
                    )

            # Show back to dashboard button
            back_button.pack(side="top", pady=10)

        else:
            # Handle no movies found
            no_movies_label = Label(
                scrollable_frame,
                text="No movies found for this year range.",
                style="Error.TLabel"
            )
            no_movies_label.grid(row=0, column=0, pady=20, padx=20)

            # Show back to dashboard button
            back_button.pack(side="top", pady=10)

    def create_dashboard_layout():
        """Create the main dashboard layout structure"""
        global button_frame, TOP_12_frame, scrollable_frame

        # Buttons Section: Sort and Creative and Repoert Options
        button_frame = Frame(main_frame, padding=10, style="Custom.TFrame")
        button_frame.pack(fill="x", pady=10)

        # Sort Button with dropdown menu
        sort_menu = tk.Menu(dashboard_frame, tearoff=0, bg="#000000", fg="white")
        sort_menu.add_command(label="Year", command=show_year_range_menu)
        sort_menu.add_command(label="Comedy", command=lambda: on_genre_selected("Comedy"))
        sort_menu.add_command(label="Romance", command=lambda: on_genre_selected("Romance"))
        sort_menu.add_command(label="Horror", command=lambda: on_genre_selected("Horror"))
        sort_menu.add_command(label="Action", command=lambda: on_genre_selected("Action"))

        sort_button = Menubutton(
            button_frame,
            text="Sort",
            bootstyle="secondary",
            style="Custom.TMenubutton"
        )
        sort_button["menu"] = sort_menu
        sort_button.pack(side="left", padx=10)

        # Graph Button with dropdown menu
        graph_menu = tk.Menu(dashboard_frame, tearoff=0, bg="#000000", fg="white")
        graph_menu.add_command(label="Actor", command=open_actor_comparison_graph)
        graph_menu.add_command(label="Actress", command=open_actress_comparison_graph)
        graph_menu.add_command(label="Director", command=open_director_comparison_graph)
        graph_menu.add_command(label="Genre", command=open_genre_comparision_graph)

        graph_button = Menubutton(
            button_frame,
            text="Creative",
            bootstyle="secondary",
            style="Custom.TMenubutton"
        )
        graph_button["menu"] = graph_menu
        graph_button.pack(side="left", padx=10)
        # REPORT Button
        report_button = Button(
            button_frame,
            text="Report",
            bootstyle="secondary",
            command=open_report_window,  # Add this line to call the function that opens the report window
            style="Custom.TButton"
        )
        report_button.pack(side="left", padx=10)

        # TOP 12 Section
        TOP_12_frame = Frame(main_frame, padding=10, style="Custom.TFrame")
        TOP_12_frame.pack(fill="x", pady=20)

        yellow_line = Label(
            TOP_12_frame,
            text="|",
            font=("Helvetica", 36),
            foreground="yellow",
            style="Custom.TLabel"
        )
        yellow_line.pack(side="left", padx=10)

        TOP_12_label = Label(
            TOP_12_frame,
            text="TOP 12",
            font=("Helvetica", 28, "bold"),
            foreground="red",
            style="Custom.TLabel"
        )
        TOP_12_label.pack(side="left", padx=10)

        # Create a canvas with a scrollbar
        canvas_frame = Frame(main_frame, padding=30, style="Custom.TFrame")
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg="#000000", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, padding=10, style="Custom.TFrame")

        # Configure scrollable frame background
        scrollable_frame.configure(style="Custom.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_movie_display(results, show_all=False):
        """
        Update the movie display with search results or top movies.
        show_all: If True, shows all movies, if False, limits to 6 movies.
        """
        for widget in scrollable_frame.winfo_children():
            widget.destroy()  # Clear previous movie display

        if not show_all:
            # For search results: Show exactly 6 movies in one row
            results = results.head(6)
            for index, movie in results.iterrows():
                poster_path = movie.get("Poster", "default_poster.jpg")
                img = load_image(poster_path, (332, 425))
                if img:
                    poster_label = Label(
                        scrollable_frame,
                        image=img,
                        style="Custom.TLabel",
                        cursor="hand2"
                    )
                    poster_label.image = img
                    poster_label.grid(row=0, column=index, padx=35, pady=15)
                    poster_label.bind("<Button-1>", lambda e, title=movie["Title"]: open_movie_details(title))
        else:
            # For dashboard: Show 12 movies in 2 rows of 6
            for index, movie in results.iterrows():
                row = index // 6
                col = index % 6
                poster_path = movie.get("Poster", "default_poster.jpg")
                img = load_image(poster_path, (330, 425))
                if img:
                    poster_label = Label(
                        scrollable_frame,
                        image=img,
                        style="Custom.TLabel",
                        cursor="hand2"
                    )
                    poster_label.image = img
                    poster_label.grid(row=row, column=col, padx=35, pady=15)
                    poster_label.bind("<Button-1>", lambda e, title=movie["Title"]: open_movie_details(title))

    def search_movies_and_update():
        """Handle search and update UI accordingly"""
        search_term = search_var.get()
        if search_term:
            results = search_movies(search_term)
            if results is not None and not results.empty:
                # Clear main frame and create search results layout
                for widget in main_frame.winfo_children():
                    widget.destroy()

                # Create new frame for search results with proper styling
                canvas_frame = Frame(main_frame, padding=30, style="Custom.TFrame")
                canvas_frame.pack(fill="both", expand=True)

                # Create canvas with black background
                canvas = tk.Canvas(canvas_frame, bg="#000000", highlightthickness=0, bd=0)
                global scrollable_frame
                scrollable_frame = Frame(canvas, padding=10, style="Custom.TFrame")

                # Ensure all frames have black background
                scrollable_frame.configure(style="Custom.TFrame")
                canvas_frame.configure(style="Custom.TFrame")

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )

                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.pack(side="left", fill="both", expand=True)

                back_button.pack(side="left", padx=10)

                # Convert back to original case for display
                results['Title'] = results['Title'].str.title()
                update_movie_display(results, show_all=False)
            else:
                # Handle no results
                for widget in main_frame.winfo_children():
                    widget.destroy()

                no_results_label = Label(
                    main_frame,
                    text="No movies found",
                    style="Custom.TLabel"
                )
                no_results_label.pack(pady=20)
                back_button.pack(side="left", padx=10)

    def open_movie_details(title):
        """Function to return movie details"""
        movie_row = data[data["Title"] == title]
        if not movie_row.empty:
            movie_data = movie_row.iloc[0].to_dict()
            MovieDetailsWindow(dashboard_frame, movie_data)

    def load_image(path, size):
        """Function to load and display an image"""
        try:
            if not os.path.isabs(path):
                possible_paths = [
                    path,
                    os.path.join(os.path.dirname(csv_path), path),
                    os.path.join(os.path.dirname(__file__), path)
                ]
                for possible_path in possible_paths:
                    if os.path.exists(possible_path):
                        path = possible_path
                        break

            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def open_actor_comparison_graph():
        visualizer = Visualizer1()
        visualizer.plot_actor_comparison_animated({
            'actors': ['Robert Downey Jr.', 'Leonardo DiCaprio', 'Scarlett Johansson', 'Tom Hanks', 'Meryl Streep',
                       'Denzel Washington'],
            'average_ratings': [8.5, 8.7, 8.3, 8.6, 8.4, 8.2]
        })
    def open_actress_comparison_graph():
        visualizer = Visualizer2()
        visualizer.plot_actress_comparison_animated({
            'actresses': ['Meryl Streep', 'Scarlett Johansson', 'Jennifer Lawrence', 'Natalie Portman', 'Emma Stone', 'Cate Blanchett'],
            'average_ratings': [8.5, 8.7, 8.3, 8.6, 8.4, 8.2]
        })
    def open_director_comparison_graph():
        visualizer = Visualizer3()
        visualizer.plot_director_comparison_animated({
            'directors': ['Steven Spielberg', 'Christopher Nolan', 'Quentin Tarantino',
                              'Martin Scorsese', 'James Cameron', 'Greta Gerwig'],
            'average_ratings': [8.1, 8.6, 8.3, 8.2, 7.9, 7.8]
        })
    def open_genre_comparision_graph():
        visualizer = Visualizer4()
        visualizer.plot_genre_comparison_animated({
        'genres': ['Action', 'Drama', 'Comedy', 'Horror', 'Sci-Fi', 'Romance'],
    'average_ratings': [6.8, 7.9, 6.9, 5.7, 7.0, 6.5]
        })
    # Top Navigation Bar
    top_nav = Frame(dashboard_frame, padding=5, style="Custom.TFrame")
    top_nav.pack(fill="x", pady=10)

    # Logo on the left
    logo_path = r"E:/python/Project/Screenshot_20241116_102301_Samsung Notes.jpg"
    logo_img = load_image(logo_path, (200, 200))
    if logo_img:
        logo_label = Label(top_nav, image=logo_img, style="Custom.TLabel")
        logo_label.image = logo_img
        logo_label.pack(side="left", padx=10)

    # Add back button (initially hidden)
    back_button = Button(
        top_nav,
        text="Back to Dashboard",
        bootstyle="primary",
        command=show_main_dashboard
    )

    # Search bar in the center
    search_frame = Frame(top_nav, padding=5, style="Custom.TFrame")
    search_frame.pack(side="left", expand=True)

    search_var = tk.StringVar()
    search_bar = Entry(search_frame, width=50, bootstyle="info", textvariable=search_var)
    search_bar.pack(side="left", padx=10)
    search_bar.bind('<Return>', lambda event: search_movies_and_update())

    search_button = Button(
        search_frame,
        text="Search",
        bootstyle="primary",
        command=search_movies_and_update
    )
    search_button.pack(side="left")

    wishlist_button = Button(search_frame, text="Wishlist", bootstyle="primary",command=lambda: open_wishlist_window(dashboard_frame, open_movie_details))
    wishlist_button.pack(side="left", padx=10)



# Update the Logout menu command

    # User dropdown menu
    user_menu = tk.Menu(dashboard_frame, tearoff=0, bg="#000000", fg="white")
    user_menu.add_command(label="Profile", command=open_user_profile)
    user_menu.add_command(label="Logout", command=logout_and_clear_last_login)

    user_button = Menubutton(
        top_nav,
        text="USER",
        bootstyle="secondary",
        style="Custom.TMenubutton"
    )
    user_button["menu"] = user_menu
    user_button.pack(side="right", padx=10)

    # Main Content Frame
    main_frame = Frame(dashboard_frame, padding=10, style="Custom.TFrame")
    main_frame.pack(fill="both", expand=True)

    # Create initial dashboard layout
    create_dashboard_layout()

    # Initial display of top movies
    update_movie_display(top_movies, show_all=True)

    return dashboard_frame
