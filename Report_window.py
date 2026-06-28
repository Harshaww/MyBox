import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Button, Entry
from genre import fetch_top_movies_by_genre, generate_output_file  # Import genre functions
from year import fetch_top_movies_by_released_year, generate_output_file  # Import year functions
import pandas as pd
from tkinter import scrolledtext  # Import ScrolledText widget
from movie_comparision import generate_comparison_report

# Fixed CSV file path for movie data
csv_path = r"C:\Users\harsh\OneDrive\Desktop\final_project\final_movie_data.csv"

# Load movie data
def load_data():
    try:
        data = pd.read_csv(csv_path)
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def open_report(dashboard_frame):
    """Function to open the report window with updated options."""
    report_window = tk.Toplevel(dashboard_frame)  # Use dashboard_frame as the parent
    report_window.title("Report Generation")
    report_window.geometry("500x400")  # Adjust size as necessary
    report_window.configure(bg="#000000")

    # Title label
    title_label = Label(
        report_window,
        text="Report Generation",
        font=("Helvetica", 18, "bold"),
        style="Custom.TLabel"
    )
    title_label.pack(pady=20)

    # Button frame for different report options
    button_frame = Frame(report_window, padding=10, style="Custom.TFrame")
    button_frame.pack(fill="x", pady=10)

    # Movie Comparison Button
    movie_comparison_button = Button(
        button_frame,
        text="Movie Comparison",
        style="Custom.TButton",
        command=open_movie_comparison_report
    )
    movie_comparison_button.pack(fill="x", pady=10)

    # Top 5 Movies by Genre Button
    top_genre_button = Button(
        button_frame,
        text="Top 5 Movies by Genre",
        style="Custom.TButton",
        command=open_top_movies_by_genre
    )
    top_genre_button.pack(fill="x", pady=10)

    # Top 5 Movies by Year Button
    top_year_button = Button(
        button_frame,
        text="Top 5 Movies by Year",
        style="Custom.TButton",
        command=open_top_movies_by_year
    )
    top_year_button.pack(fill="x", pady=10)

def open_movie_comparison_report():
    """Function to handle movie comparison report generation."""
    comparison_window = tk.Toplevel()
    comparison_window.title("Movie Comparison")
    comparison_window.geometry("400x400")
    comparison_window.configure(bg="#000000")

    # Label for movie 1 input
    movie1_label = Label(comparison_window, text="Enter first movie/series", style="Custom.TLabel")
    movie1_label.pack(pady=10)

    movie1_entry = Entry(comparison_window, width=40)
    movie1_entry.pack(pady=10)

    # Label for movie 2 input
    movie2_label = Label(comparison_window, text="Enter second movie/series", style="Custom.TLabel")
    movie2_label.pack(pady=10)

    movie2_entry = Entry(comparison_window, width=40)
    movie2_entry.pack(pady=10)

    # Function to trigger the comparison when "Compare" button is clicked
    def compare_movies():
        movie1 = movie1_entry.get()
        movie2 = movie2_entry.get()

        if movie1 and movie2:
            generate_comparison_report(movie1, movie2)
            comparison_window.destroy()
        else:
            print("Please enter both movie titles.")

    # Compare button
    compare_button = Button(comparison_window, text="Compare", style="Custom.TButton", command=compare_movies)
    compare_button.pack(pady=20)

def open_top_movies_by_genre():
    """Function to get genre input and generate top 5 movies by genre report."""
    genre_window = tk.Toplevel()
    genre_window.title("Top 5 Movies by Genre")
    genre_window.geometry("500x400")
    genre_window.configure(bg="#000000")

    # Label for genre input
    genre_label = Label(genre_window, text="Enter Genre:", style="Custom.TLabel")
    genre_label.pack(pady=10)

    genre_entry = Entry(genre_window, width=40)
    genre_entry.pack(pady=10)

    # Function to generate and display the report
    def generate_report():
        genre = genre_entry.get().strip()
        if genre:
            # Fetch top movies based on genre
            top_movies = fetch_top_movies_by_genre(genre, csv_path=csv_path)

            if top_movies.empty:
                print(f"No movies found for the genre: {genre}.")
                return

            # Create a new window to display the results
            result_window = tk.Toplevel(genre_window)  # New window for the results
            result_window.title(f"Top 5 Movies in {genre.capitalize()}")
            result_window.geometry("600x500")  # Adjusted window size
            result_window.configure(bg="#000000")

            # Create a larger ScrolledText widget to display the report
            output_text_widget = scrolledtext.ScrolledText(result_window, width=60, height=15, wrap=tk.WORD)
            output_text_widget.pack(padx=10, pady=10)

            # Generate the output file (or just print/display the result)
            generate_output_file(genre, top_movies, output_text_widget=output_text_widget)

            # Clear the genre entry field after report generation
            genre_entry.delete(0, tk.END)
        else:
            print("Please enter a valid genre.")

    # Generate button
    generate_button = Button(genre_window, text="Generate Report", style="Custom.TButton", command=generate_report)
    generate_button.pack(pady=20)

def open_top_movies_by_year():
    """Function to get year input and generate top 5 movies by year report."""
    year_window = tk.Toplevel()
    year_window.title("Top 5 Movies by Year")
    year_window.geometry("500x400")
    year_window.configure(bg="#000000")

    # Label for year input
    year_label = Label(year_window, text="Enter Year(1975-2020):", style="Custom.TLabel")
    year_label.pack(pady=10)

    year_entry = Entry(year_window, width=40)
    year_entry.pack(pady=10)

    # Function to generate and display the report
    def generate_report():
        year = year_entry.get().strip()
        if year.isdigit():
            year = int(year)
            # Fetch top movies by released year from year.py
            top_movies = fetch_top_movies_by_released_year(year, csv_path=csv_path)

            if top_movies is None or top_movies.empty:
                print(f"No movies found for the year {year}.")
                return

            # Create a new window to display the results
            result_window = tk.Toplevel(year_window)  # New window for the results
            result_window.title(f"Top 5 Movies in {year}")
            result_window.geometry("600x500")  # Adjusted window size
            result_window.configure(bg="#000000")

            # Create a larger ScrolledText widget to display the report
            output_text_widget = scrolledtext.ScrolledText(result_window, width=60, height=15, wrap=tk.WORD)
            output_text_widget.pack(padx=10, pady=10)

            # Generate the output file (or just print/display the result)
            generate_output_file(year, top_movies, output_text_widget=output_text_widget)

            # Clear the year entry field after report generation
            year_entry.delete(0, tk.END)
        else:
            print("Please enter a valid year.")

    # Generate button
    generate_button = Button(year_window, text="Generate Report", style="Custom.TButton", command=generate_report)
    generate_button.pack(pady=20)

