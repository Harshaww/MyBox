"""
recommendation_window.py
Displays content-based movie recommendations for a given title.
Called from MovieDetailsWindow with a single function: open_recommendations()
"""

import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

from recommender import get_recommendations


# ── Helpers ──────────────────────────────────────────────────────────────────

def _load_image(path: str, size: tuple) -> ImageTk.PhotoImage | None:
    """Load and resize a poster image, return None on failure."""
    try:
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


def _make_placeholder(size: tuple) -> ImageTk.PhotoImage:
    """Grey placeholder for missing posters."""
    img = Image.new("RGB", size, "#2b2b2b")
    return ImageTk.PhotoImage(img)


# ── Main window ───────────────────────────────────────────────────────────────

def open_recommendations(
    parent,
    movie_title: str,
    csv_path: str,
    on_movie_click=None,
):
    """
    Open a modal window showing the top-6 content-based recommendations
    for `movie_title`.

    Parameters
    ----------
    parent       : tkinter widget  — parent window
    movie_title  : str             — title of the movie to base recs on
    csv_path     : str             — path to final_movie_data.csv
    on_movie_click : callable | None
        Optional callback(title: str) invoked when the user clicks a
        recommended poster, so the caller can open MovieDetailsWindow.
    """

    # ── Window setup ─────────────────────────────────────────────────────────
    win = ttk.Toplevel(parent)
    win.title(f"Because you viewed: {movie_title}")
    win.geometry("1100x620")
    win.resizable(True, True)

    style = ttk.Style()
    style.configure("Rec.TFrame",  background="#111111")
    style.configure("Rec.TLabel",  background="#111111", foreground="white",
                    font=("Helvetica", 11))
    style.configure("RecH.TLabel", background="#111111", foreground="#FFD700",
                    font=("Helvetica", 13, "bold"))
    style.configure("RecSub.TLabel", background="#111111", foreground="#AAAAAA",
                    font=("Helvetica", 10))
    style.configure("Score.TLabel", background="#111111", foreground="#00CC66",
                    font=("Helvetica", 10, "bold"))

    root_frame = ttk.Frame(win, style="Rec.TFrame", padding=15)
    root_frame.pack(fill=BOTH, expand=YES)

    # ── Header ───────────────────────────────────────────────────────────────
    header = ttk.Frame(root_frame, style="Rec.TFrame")
    header.pack(fill=X, pady=(0, 15))

    ttk.Label(
        header,
        text="🎬  Recommended For You",
        style="RecH.TLabel",
        font=("Helvetica", 18, "bold"),
    ).pack(side=LEFT)

    ttk.Label(
        header,
        text=f"Based on: {movie_title}",
        style="RecSub.TLabel",
    ).pack(side=LEFT, padx=15)

    ttk.Label(
        header,
        text="Powered by TF-IDF content similarity",
        style="RecSub.TLabel",
    ).pack(side=RIGHT)

    # ── Fetch recommendations ─────────────────────────────────────────────────
    try:
        recs = get_recommendations(movie_title, csv_path, n=6)
    except ValueError as e:
        ttk.Label(
            root_frame,
            text=str(e),
            style="Rec.TLabel",
            foreground="red",
        ).pack(pady=40)
        return

    # ── Poster grid (1 row × 6 columns) ──────────────────────────────────────
    POSTER_W, POSTER_H = 150, 220
    CARD_PAD = 12

    grid_frame = ttk.Frame(root_frame, style="Rec.TFrame")
    grid_frame.pack(fill=BOTH, expand=YES)

    photo_refs = []  # Keep refs alive to prevent GC

    for col, (_, row) in enumerate(recs.iterrows()):
        card = ttk.Frame(grid_frame, style="Rec.TFrame", padding=CARD_PAD)
        card.grid(row=0, column=col, padx=8, pady=5, sticky="n")

        # ── Poster ───────────────────────────────────────────────────────────
        poster_path = str(row.get("Poster", ""))
        photo = _load_image(poster_path, (POSTER_W, POSTER_H))
        if photo is None:
            photo = _make_placeholder((POSTER_W, POSTER_H))
        photo_refs.append(photo)

        poster_lbl = ttk.Label(card, image=photo, style="Rec.TLabel",
                               cursor="hand2")
        poster_lbl.image = photo
        poster_lbl.pack()

        # Click → open movie details
        if on_movie_click:
            title_val = row["Title"]
            poster_lbl.bind(
                "<Button-1>",
                lambda _e, t=title_val: on_movie_click(t),
            )

        # ── Title (truncated) ─────────────────────────────────────────────────
        title_text = row["Title"]
        if len(title_text) > 22:
            title_text = title_text[:20] + "…"

        ttk.Label(
            card,
            text=title_text,
            style="Rec.TLabel",
            wraplength=POSTER_W,
            justify=CENTER,
            font=("Helvetica", 10, "bold"),
        ).pack(pady=(6, 0))

        # ── Year + Rating ─────────────────────────────────────────────────────
        ttk.Label(
            card,
            text=f"{int(row['Year'])}  ⭐ {row['Rating']}",
            style="RecSub.TLabel",
        ).pack()

        # ── Genre (first genre only to keep it short) ─────────────────────────
        first_genre = str(row["Genre"]).split(",")[0].strip()
        ttk.Label(
            card,
            text=first_genre,
            style="RecSub.TLabel",
        ).pack()

        # ── Similarity score ──────────────────────────────────────────────────
        score_pct = int(row["similarity_score"] * 100)
        ttk.Label(
            card,
            text=f"Match: {score_pct}%",
            style="Score.TLabel",
        ).pack(pady=(4, 0))

    # ── Footer ────────────────────────────────────────────────────────────────
    footer = ttk.Frame(root_frame, style="Rec.TFrame")
    footer.pack(fill=X, pady=(15, 0))

    ttk.Label(
        footer,
        text=(
            "Similarity is computed using TF-IDF vectorisation of genre, "
            "director, cast, and synopsis, ranked by cosine similarity."
        ),
        style="RecSub.TLabel",
        wraplength=900,
    ).pack(side=LEFT)

    ttk.Button(
        footer,
        text="Close",
        bootstyle="secondary-outline",
        command=win.destroy,
    ).pack(side=RIGHT)
