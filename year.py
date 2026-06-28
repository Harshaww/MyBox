import os
import pandas as pd

def fetch_top_movies_by_released_year(released_year, csv_path=r"C:\Users\harsh\OneDrive\Desktop\final_project\final_movie_data.csv"):
    """
    Fetch the top 5 movies for a specific Released_Year based on IMDb ratings.

    :param released_year: The released year to filter movies by.
    :param csv_path: Path to the CSV file containing movie data.
    :return: A DataFrame with the top 5 movies for the specified Released_Year.
    """
    if not os.path.exists(csv_path):
        print(f"Error: Could not find CSV file at {csv_path}")
        return None

    try:
        data = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

    # Ensure 'Year' column is numeric and 'Rating' is numeric
    data["Year"] = pd.to_numeric(data["Year"], errors="coerce")  # Convert 'Year' to numeric, invalid values become NaN
    data["Rating"] = pd.to_numeric(data["Rating"], errors="coerce")  # Ensure 'Rating' is numeric
    data["Gross"] = pd.to_numeric(data["Gross"], errors="coerce")  # Convert 'Gross' to numeric

    # Filter movies by the specified Year
    filtered_movies = data[data["Year"] == released_year]

    if filtered_movies.empty:
        print(f"No movies found for the released year: {released_year}")
        return None

    # Sort by IMDb rating (non-NaN) and select the top 5
    top_movies = filtered_movies.sort_values(by="Rating", ascending=False).head(5)
    return top_movies


def generate_output_file(released_year, top_movies, output_file="top_movies_by_released_year.txt", output_text_widget=None):
    """
    Generate a file containing the top 5 movies for the specified released year.

    :param released_year: The released year selected by the user.
    :param top_movies: DataFrame containing the top movies.
    :param output_file: Path to the output file.
    :param output_text_widget: Tkinter Text widget to display the output (optional).
    """
    output = ""

    if top_movies is None or top_movies.empty:
        output = f"No movies found for the released year: {released_year}\n"
        print(f"No movies found for the released year: {released_year}")
    else:
        output += "=" * 60 + "\n"
        output += f"{'🎬 Top 5 Movies of the Released Year:':^60}\n"
        output += f"{released_year:^60}\n"
        output += "=" * 60 + "\n"

        for idx, row in enumerate(top_movies.itertuples(), start=1):
            output += f"  ⭐ {idx}. {row.Title.upper():<40}\n"
            output += f"     {'Genre:':<10} {row.Genre}\n"
            output += f"     {'Rating:':<10} {row.Rating}\n"
            output += f"     {'Gross:':<10} {row.Gross if not pd.isna(row.Gross) else 'N/A'}\n"
            output += "-" * 60 + "\n"

        output += f"\n{'Enjoy the classics! 🍿':^60}\n"
        output += "=" * 60 + "\n"

    # Display the output in the Text widget (GUI)
    if output_text_widget is not None:
        output_text_widget.delete(1.0, "end")  # Clear the existing content
        output_text_widget.insert("end", output)  # Insert the new output

    # Save the output to the text file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(output)

    print(f"🎉 Output saved to '{output_file}'")
    print(f"Open the file to view the full details of the movies.")
