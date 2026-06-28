# IMDb-Clone

## Commands to Start the Application:
- **Run main_app.py**
  - From the terminal: Run `main_app.py`.
  - Activate the virtual environment: `.\venv\Scripts\activate`.


## Operating Systems Supported

- Windows

## Libraries To Install

- ttkbootstrap  
- pandas  
- matplotlib  
- numpy  
- fuzzywuzzy  
- python-Levenshtein  
- tkinter  
- random  
- datetime  

## APIs Used

- **OMDb API** – Used for retrieving detailed movie information such as plot, cast, director, genre, runtime, and release year.  
- **TMDb API** – Used for retrieving and analyzing movie ratings and related metadata.

## Features Implemented

### Authentication
- Login page
- New user registration
- Persistent user sessions

### Main Dashboard
- Displays top 12 movies
- Interactive movie selection
- Clicking on a movie displays:
- Plot
- Director
- Cast
- Genre
- Synopsis
- Duration
- IMDb rating
- Release year

### Search and Sorting
- Search bar with fuzzy matching
- Sorting options:
- By release year
- By genre

### Wishlist
- Save movies of interest
- Wishlist persists across sessions
- Data retained even after logout

### Data Visualization
- **Line Graphs**
- Displays rating trends over:
 - 1st day
 - 1st month
 - 3 months
 - 6 months
 - 1 year
- **Creative Mode (Bar Graphs)**
- Average IMDb ratings by:
 - Actor
 - Actress
 - Director
 - Genre

### Reports & Analysis
- Compare two movies across multiple metrics
- Generate:
- Top 5 movies by genre
- Top 5 movies by user-specified year

## Architecture Overview

- Modular design separating UI, API integration, data processing, and visualization logic
- Secure and organized user data management
- Smooth navigation between application pages
- Efficient backend automation

## Documentation

Detailed documentation of all modules and classes is available within the codebase.

## Author

**Samavedam Sai Harsha**

