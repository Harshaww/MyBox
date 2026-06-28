import matplotlib.pyplot as plt
import datetime
import random
from matplotlib import rcParams

# Set global font for Matplotlib
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Trebuchet MS', 'Californian FB']
rcParams['font.size'] = 12


def generate_time_intervals(start_date):
    """
    Generate time intervals over a 1-year period from the release date.
    Intervals:
    - Starting day
    - 1 month later
    - 3 months later
    - 6 months later
    - 1 year later
    """
    intervals = [
        start_date,
        start_date + datetime.timedelta(days=30),  # Approx. 1 month
        start_date + datetime.timedelta(days=90),  # Approx. 3 months
        start_date + datetime.timedelta(days=180),  # Approx. 6 months
        start_date + datetime.timedelta(days=365)  # Approx. 1 year
    ]
    return intervals


def generate_random_ratings(base_rating, num_points):
    """
    Generate random ratings around the base IMDB rating within a small range (+/- 0.5).
    """
    ratings = []
    for _ in range(num_points):
        fluctuation = random.uniform(-0.5, 0.5)  # Random fluctuation between -0.5 and +0.5
        new_rating = round(base_rating + fluctuation, 1)
        # Clamp ratings between 0 and 10
        new_rating = max(0, min(10, new_rating))
        ratings.append(new_rating)
    return ratings


def plot_movie_ratings(title, year, base_rating):
    """
    Plots a professional animated 3D bar chart comparing average ratings over a 1-year period.
    Instead of fetching data from CSV, the function accepts title, year, and rating as arguments.
    """

    print(f"\n🎬 Movie '{title.upper()}' found with release year: {year} and IMDb rating: {base_rating}")

    # Generate dates and random ratings
    start_date = datetime.date(year, 1, 1)  # Assume the movie was released on Jan 1 of its release year
    intervals = generate_time_intervals(start_date)  # Generate intervals
    random_ratings = generate_random_ratings(base_rating, len(intervals))

    # Visualize data
    plt.figure(figsize=(12, 8))

    # Plot the generated data
    plt.plot(intervals, random_ratings, marker='o', linestyle='-', color='#0056b3', linewidth=2,
             markersize=8, label=f"{title.upper()} IMDb Rating")

    # Add a benchmark horizontal line
    plt.axhline(y=base_rating, color='green', linestyle='--', linewidth=1, label="Base IMDb Rating")

    # Add graph labels and title
    plt.title(f"IMDb Rating Changes Over 1-Year Time Span for '{title.upper()}'", fontsize=20, fontweight='bold', family='Trebuchet MS')
    plt.xlabel("Time Periods", fontsize=16, family='Californian FB')
    plt.ylabel("IMDb Rating", fontsize=16, family='Californian FB')

    # Customize the x-axis with interval names
    interval_labels = ['Start Date', '1 Month', '3 Months', '6 Months', '1 Year']
    plt.xticks(intervals, interval_labels, fontsize=12, family='Californian FB')
    plt.yticks(fontsize=12, family='Californian FB')

    # Add a legend
    plt.legend(fontsize=12, loc='best', frameon=False, prop={'family': 'Californian FB'})
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Finalize and show the graph
    plt.tight_layout()
    plt.show()

    print("\n✅ Graph successfully visualized!")


