"""
recommender.py
Content-based movie recommendation engine.

Algorithm:
1. Build a "content soup" for each movie by combining Genre, Director,
   Cast, and Synopsis into a single text string.
2. Vectorize all soups using TF-IDF (Term Frequency-Inverse Document
   Frequency), which down-weights common words and up-weights rare,
   meaningful ones.
3. Compute pairwise cosine similarity across all 1000 movies.
4. For a query movie, return the N most similar movies by cosine score,
   excluding itself.

Why TF-IDF + cosine similarity:
- Genre alone is too coarse (300+ Drama movies all look identical).
- Synopsis adds semantic meaning — movies with similar plots score higher.
- Director and Cast create implicit style clusters (e.g., Nolan films
  cluster together because "Christopher Nolan" appears in all their soups).
- Cosine similarity is direction-based, not magnitude-based, so a short
  synopsis doesn't penalize a movie against one with a long synopsis.
"""

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ── Internal state (module-level singletons, built once on first call) ──────
_df: pd.DataFrame | None = None
_cosine_sim = None
_title_index: pd.Series | None = None


def _build_content_soup(row: pd.Series) -> str:
    """
    Concatenate the fields that define a movie's content identity.
    Repeat Genre 3× so it carries more weight than free-text synopsis.
    Cast names have spaces removed so 'Tom Hanks' becomes 'TomHanks'
    and stays a single token — otherwise 'Tom' matches unrelated movies.
    """
    genre = str(row.get("Genre", "")).replace(",", " ")
    director = str(row.get("Director", "")).replace(" ", "")
    cast_raw = str(row.get("Cast", ""))
    cast = " ".join(name.strip().replace(" ", "") for name in cast_raw.split(","))
    synopsis = str(row.get("Synopsis", ""))

    # Genre repeated to increase its weight in TF-IDF
    return f"{genre} {genre} {genre} {director} {cast} {synopsis}"


def _load_and_fit(csv_path: str) -> None:
    """Load the CSV, build soups, fit TF-IDF, compute cosine similarity matrix."""
    global _df, _cosine_sim, _title_index

    df = pd.read_csv(csv_path)

    # Normalise title casing for consistent lookups
    df["Title"] = df["Title"].str.strip()

    # Fill missing fields so they don't break string ops
    for col in ["Genre", "Director", "Cast", "Synopsis"]:
        df[col] = df[col].fillna("")

    # Build content soup for every row
    df["_soup"] = df.apply(_build_content_soup, axis=1)

    # TF-IDF vectorisation
    # stop_words="english" removes "the", "a", "and", etc.
    # max_features caps vocabulary to keep memory manageable
    tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = tfidf.fit_transform(df["_soup"])

    # Full pairwise cosine similarity  (shape: n_movies × n_movies)
    _cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Map movie title → DataFrame row index for O(1) lookups
    _title_index = pd.Series(df.index, index=df["Title"]).drop_duplicates()

    _df = df


def get_recommendations(
    movie_title: str,
    csv_path: str,
    n: int = 6,
) -> pd.DataFrame:
    """
    Return the top-N most similar movies to `movie_title`.

    Parameters
    ----------
    movie_title : str
        Exact title as it appears in the CSV (case-sensitive after strip).
    csv_path : str
        Path to final_movie_data.csv.
    n : int
        Number of recommendations to return (default 6).

    Returns
    -------
    pd.DataFrame
        Subset of the original DataFrame with the top-N similar movies,
        sorted by similarity score descending. Includes a 'similarity_score'
        column (0–1 float).

    Raises
    ------
    ValueError
        If the title is not found in the dataset.
    """
    # Lazy load — only fits once per process lifetime
    if _df is None or not os.path.samefile(csv_path, csv_path):
        _load_and_fit(csv_path)

    # Re-fit if the CSV changed or first call
    if _df is None:
        _load_and_fit(csv_path)

    # Title lookup
    if movie_title not in _title_index:
        # Try case-insensitive fallback
        lower_map = {t.lower(): t for t in _title_index.index}
        match = lower_map.get(movie_title.lower())
        if match is None:
            raise ValueError(
                f"Movie '{movie_title}' not found in dataset. "
                "Check the title spelling."
            )
        movie_title = match

    idx = _title_index[movie_title]

    # Similarity scores for this movie against every other movie
    sim_scores = list(enumerate(_cosine_sim[idx]))

    # Sort by score descending, skip index 0 (the movie itself)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] != idx][:n]

    movie_indices = [s[0] for s in sim_scores]
    scores = [s[1] for s in sim_scores]

    result = _df.iloc[movie_indices].copy()
    result["similarity_score"] = [round(s, 4) for s in scores]

    return result[["Title", "Year", "Genre", "Rating", "Director", "Synopsis",
                   "Poster", "similarity_score"]]


def preload(csv_path: str) -> None:
    """
    Call this at app startup to fit the model eagerly so the first
    recommendation request is instant.
    """
    _load_and_fit(csv_path)
