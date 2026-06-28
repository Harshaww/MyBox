import pandas as pd
from fuzzywuzzy import process  # type: ignore

# Define the path to your movie CSV file
csv_path = r"/mnt/c/Users/sai harsha/Downloads/mybox/final_movie_data.csv"


def search_movies(user_input):
    """
    Search for movies based on user input using fuzzy matching.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        return pd.DataFrame()  # Return empty DataFrame instead of None

    # Ensure case-insensitivity
    df['Title'] = df['Title'].str.lower()
    user_input = user_input.lower()

    # Apply fuzzy matching
    results = process.extract(user_input, df['Title'], limit=6)
    matched_titles = [match[0] for match in results]

    # Filter DataFrame to include only matched titles
    matched_movies = df[df['Title'].isin(matched_titles)]
    return matched_movies


def filter_by_year(year_range):
    """
    Filter movies based on the selected year range.
    """
    try:
        # Read the movie data
        df = pd.read_csv(csv_path)
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')  # Ensure 'Year' is numeric

        # Parse the year range
        start_year, end_year = map(int, year_range.split("-"))

        # Filter movies within the year range
        filtered_movies = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]
        return filtered_movies
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        return pd.DataFrame()  # Return empty DataFrame
    except Exception as e:
        print(f"Error filtering by year: {e}")
        return pd.DataFrame()  # Return empty DataFrame


def filter_by_genre(genre):
    """
    Filter movies based on the selected genre.
    """
    try:
        # Read the movie data
        df = pd.read_csv(csv_path)

        # Ensure 'Genre' column exists and is properly formatted
        if 'Genre' not in df.columns:
            print("Error: 'Genre' column missing in the CSV file.")
            return pd.DataFrame()  # Return empty DataFrame

        # Filter movies based on the genre
        filtered_movies = df[df['Genre'].str.contains(genre, case=False, na=False)]
        return filtered_movies
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        return pd.DataFrame()  # Return empty DataFrame
    except Exception as e:
        print(f"Error filtering by genre: {e}")
        return pd.DataFrame()  # Return empty DataFrame