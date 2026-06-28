import os
import pandas as pd
import tkinter as tk  # <-- Add this import to solve the "tk" not defined error
from tkinter import scrolledtext

# Function to fetch top movies by genre
def fetch_top_movies_by_genre(genre, csv_path=r"/mnt/c/Users/sai harsha/Downloads/mybox/final_movie_data.csv"):
    """
    Fetch the top 5 movies for a specific genre based on IMDb ratings.

    :param genre: The genre to filter movies by.
    :param csv_path: Path to the CSV file containing movie data.
    :return: A DataFrame with the top 5 movies for the specified genre.
    """
    if not os.path.exists(csv_path):
        print(f"Error: Could not find CSV file at {csv_path}")
        return None

    try:
        data = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

    # Clean genre data (fill NaN values)
    data["Genre"] = data["Genre"].fillna("")
    data["Rating"] = pd.to_numeric(data["Rating"], errors='coerce')  # Handle non-numeric ratings as NaN
    filtered_movies = data[data["Genre"].str.contains(genre, case=False, na=False)]
    top_movies = filtered_movies.sort_values(by="Rating", ascending=False).head(5)

    return top_movies


# Function to generate and display the report in the GUI, and save it to a file
def generate_output_file(genre, top_movies, output_file="top_movies_output.txt", output_text_widget=None):
    """
    Generate a file containing the top 5 movies for the specified genre and show it in the GUI.

    :param genre: The genre selected by the user.
    :param top_movies: DataFrame containing the top movies.
    :param output_file: Path to the output file.
    :param output_text_widget: Tkinter Text widget to display the output (optional).
    """
    output = ""

    if top_movies is None or top_movies.empty:
        output = f"No movies found for the genre: {genre}\n"
        print(f"No movies found for the genre: {genre}")
    else:
        output += "=" * 60 + "\n"
        output += f"{'🎬 Top 5 Movies in the Genre:':^60}\n"
        output += f"{genre.upper():^60}\n"
        output += "=" * 60 + "\n"

        for idx, row in enumerate(top_movies.itertuples(), start=1):
            output += f"  ⭐ {idx}. {row.Title.upper():<40}\n"
            output += f"     {'Year:':<10} {row.Year}\n"
            output += f"     {'Rating:':<10} {row.Rating}\n"
            output += f"     {'Gross:':<10} {row.Gross if not pd.isna(row.Gross) else 'N/A'}\n"
            output += "-" * 60 + "\n"

        output += f"\n{'Enjoy the classics! 🍿':^60}\n"
        output += "=" * 60 + "\n"

    # Display the output in the Text widget (GUI)
    if output_text_widget is not None:
        output_text_widget.delete(1.0, tk.END)  # Clear the existing content
        output_text_widget.insert(tk.END, output)  # Insert the new output

    # Save the output to the text file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(output)

    print(f"🎉 Output saved to '{output_file}'")
    print(f"Open the file to view the full details of the movies.")
