import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

# Fetch movie data from the CSV file
def fetch_movie_data(movie_title):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_directory, "final_movie_data.csv")

    if not os.path.exists(csv_path):
        print(f"Error: Could not find CSV file at {csv_path}")
        return None

    try:
        data = pd.read_csv(csv_path)
        data.columns = data.columns.str.strip()  # Ensure there are no leading/trailing spaces in column names
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

    if "Title" in data.columns:
        movie_data = data[data["Title"].str.lower() == movie_title.lower()]
    else:
        print("Error: Column 'Title' not found in the CSV.")
        return None

    if movie_data.empty:
        print(f"Error fetching data for '{movie_title}'")
        return None

    return movie_data.iloc[0].to_dict()

# Open poster from local file path
def get_poster(path):
    try:
        if os.path.exists(path):
            return Image.open(path)
        else:
            print(f"Error: Poster file not found at {path}")
            return None
    except Exception as e:
        print(f"Failed to open poster from {path}: {e}")
        return None

# Create a background with gradient and noise
def create_background(width, height):
    background = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(background)

    for y in range(height):
        r, g, b = 0, 0, int(40 + (y / height) * 100)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    for _ in range(1000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        noise_intensity = random.randint(0, 30)
        current_color = tuple([int(c + noise_intensity) for c in background.getpixel((x, y))])
        draw.point((x, y), fill=current_color)

    background = background.filter(ImageFilter.GaussianBlur(radius=1))
    return background

# Generate the comparison image
def generate_output_image(data):
    width = 1800
    padding = 60
    header_height = 150
    poster_height = 300  # Reduced poster height
    poster_width = 200   # Reduced poster width
    row_height = 100
    num_rows = len(data["Attributes"])
    height = padding * 3 + header_height + poster_height + row_height * num_rows

    background = create_background(width, height)
    draw = ImageDraw.Draw(background)

    # Use default bold font with increased sizes
    font_large = ImageFont.truetype("arialbd.ttf", 48)
    font_medium = ImageFont.truetype("arialbd.ttf", 36)
    font_small = ImageFont.truetype("arialbd.ttf", 28)

    header_color = "#1e3a63"
    text_color = "white"
    row_color = "#2e466d"
    row_color_alternate = "#1e2a4c"
    border_color = "#5c85d6"

    # Draw header with rounded corners
    draw.rounded_rectangle([(padding, padding), (width - padding, padding + header_height)], radius=20, fill=header_color)
    draw.text((padding + 40, padding + 50), "Movie Comparison Table", fill=text_color, font=font_large)

    # Column titles
    draw.text((padding + 20, padding + header_height + 40), "Attribute", fill=text_color, font=font_medium)
    draw.text((width // 3 + 70, padding + header_height + 40), data["Movie1"]["Title"], fill=text_color, font=font_medium)
    draw.text((2 * (width // 3) + 70, padding + header_height + 40), data["Movie2"]["Title"], fill=text_color, font=font_medium)

    # Load posters
    movie1_poster = get_poster(data["Movie1"]["Poster"])
    movie2_poster = get_poster(data["Movie2"]["Poster"])

    if not movie1_poster or not movie2_poster:
        print("Could not load one or both movie posters. Exiting.")
        return

    movie1_poster = movie1_poster.resize((poster_width, poster_height))
    movie2_poster = movie2_poster.resize((poster_width, poster_height))

    background.paste(movie1_poster, (width // 3 + 60, padding + header_height + 90))
    background.paste(movie2_poster, (2 * (width // 3) + 60, padding + header_height + 90))

    # Draw rows
    for idx, attribute in enumerate(data["Attributes"]):
        y_position = padding + header_height + poster_height + (idx * row_height)
        row_fill_color = row_color if idx % 2 == 0 else row_color_alternate

        draw.rectangle([(padding, y_position), (width - padding, y_position + row_height)], fill=row_fill_color, outline=border_color)
        draw.text((padding + 20, y_position + 40), str(attribute), fill=text_color, font=font_small)
        draw.text((width // 3 + 70, y_position + 40), str(data["Movie1"].get(attribute, "N/A")), fill=text_color, font=font_small)
        draw.text((2 * (width // 3) + 70, y_position + 40), str(data["Movie2"].get(attribute, "N/A")), fill=text_color, font=font_small)

    # Save and display the image
    output_filename = f"{data['Movie1']['Title']} vs {data['Movie2']['Title']}.png"
    background.save(output_filename)
    print(f"Comparison table saved as {output_filename}")
    background.show()  # Open the image to view it immediately

# Generate the comparison report
def generate_comparison_report(movie1_title, movie2_title):
    movie1_data = fetch_movie_data(movie1_title)
    movie2_data = fetch_movie_data(movie2_title)

    if movie1_data and movie2_data:
        data = {
            "Attributes": ["Title", "Year", "Rating", "Gross", "Budget"],
            "Movie1": movie1_data,
            "Movie2": movie2_data
        }
        generate_output_image(data)
    else:
        print("Could not fetch the required movie/series data.")
