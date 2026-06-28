# IMDB-Rating

A Python-based desktop movie analytics application built with tkinter and ttkbootstrap, featuring a content-based recommendation engine, interactive visualizations, and movie comparison tools across a dataset of 1,000 films.

## Setup

pip install scikit-learn ttkbootstrap pillow pandas matplotlib fuzzywuzzy python-levenshtein

python main_app.py

## Tech Stack

Python, tkinter, ttkbootstrap, pandas, scikit-learn, Matplotlib, FuzzyWuzzy

## Features

### Recommendation Engine
- Content-based recommendation system using TF-IDF vectorization and cosine similarity
- Computes similarity across genre, director, cast, and synopsis metadata for 1,000 films
- Returns top-6 similar movies ranked by match percentage
- Similarity matrix fitted once at startup for instant query response
- Accessible via the "Similar Movies" button on any movie detail page

### Authentication
- Login and registration pages
- Persistent user sessions across app restarts

### Main Dashboard
- Displays top 12 movies on load
- Click any poster to open full movie details including plot, director, cast, genre, synopsis, duration, rating, and release year

### Search and Filtering
- Fuzzy search using FuzzyWuzzy for typo-tolerant title matching
- Filter by release year range
- Filter by genre

### Wishlist
- Save movies across sessions
- Persists after logout

### Data Visualization
- Line graphs showing rating trends over time
- Animated bar graphs comparing average IMDb ratings by actor, actress, director, and genre

### Reports
- Side-by-side movie comparison across multiple metrics
- Top 5 movies by genre report
- Top 5 movies by year report

## Project Structure

main_app.py                 — Entry point
dashboard_page.py           — Main dashboard UI
movie_data.py               — Movie detail window
recommender.py              — TF-IDF recommendation engine
recommendation_window.py    — Recommendation UI
search_movie.py             — Fuzzy search and filters
login_page.py               — Login UI
registration_page.py        — Registration UI
wishlist_window.py          — Wishlist UI
Report_window.py            — Report generation
Visualizer1-4.py            — Animated bar graph visualizers
line_vis.py                 — Line graph visualizer
genre.py                    — Genre-based filtering
year.py                     — Year-based filtering
user_profile.py             — User profile UI
movie_comparision.py        — Movie comparison UI
final_movie_data.csv        — 1,000 movie dataset

## Author

Samavedam Sai Harsha
GitHub: https://github.com/Harshaww
