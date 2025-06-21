import os
from typing import List
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import state


# bobber recommendations
def get_recommendations(
    user_inputs: List[str],
    min_rating: float,
    max_rating: float,
):
    user_inputs = [title.lower().strip() for title in user_inputs]
    print(user_inputs)
    for i in user_inputs:
        print(i)
    # --- Ordnerpfade vorbereiten (relativ zum Skript) ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RATINGS_DIR = os.path.join(BASE_DIR, "ratings")
    MOVIES_PATH = os.path.join(BASE_DIR, "movies.csv")

    # --- Filme laden und bereinigen ---
    df = pd.read_csv(MOVIES_PATH)
    df["year"] = df["title"].str.extract(r"\((\d{4})\)")
    df["title"] = df["title"].str.replace(r"\s*\(\d{4}\)", "", regex=True).str.strip()
    df["year"] = df["year"].astype("Int64")
    df = df.dropna(subset=["year"])

    # --- Genres vektorisieren ---
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split("|"))
    genre_matrix = vectorizer.fit_transform(df["genres"])
    genre_matrix_dense = genre_matrix.toarray()

    # --- Mapping: Titel zu Index ---
    title_to_index = {t.lower(): i for i, t in enumerate(df["title"])}

    # --- Ratings einlesen & mittlere Bewertung berechnen ---
    ratings_list = []
    for i in range(33):
        path = os.path.join(RATINGS_DIR, f"ratings_{i}.csv")
        df_r = pd.read_csv(path, usecols=["movieId", "rating"])
        ratings_list.append(df_r)

    ratings_all = pd.concat(ratings_list, ignore_index=True)
    mean_ratings = ratings_all.groupby("movieId")["rating"].mean().reset_index()
    mean_ratings.rename(columns={"rating": "mean_rating"}, inplace=True)

    # --- Ratings mit Filmen verbinden ---
    df = pd.merge(df, mean_ratings, on="movieId", how="left")

    # --- Gültige Filme überprüfen ---
    valid_indices = []
    for title in user_inputs:
        if title in title_to_index:
            valid_indices.append(title_to_index[title])
        else:
            print(f"⚠️  Film nicht gefunden: {title}")

    if not valid_indices:
        print("❌ Keine gültigen Filme eingegeben. Abbruch.")
        exit()

    # --- Benutzervektor berechnen ---
    user_vector = np.asarray(genre_matrix_dense[valid_indices].mean(axis=0))

    # --- Hauptempfehlung (Top-N mit Ratingfilter, Ein gaben ausschließen) ---
    similarities = cosine_similarity(
        user_vector.reshape(1, -1), genre_matrix_dense
    ).flatten()
    mask_main = ~np.isin(np.arange(len(df)), valid_indices) & df["mean_rating"].between(
        min_rating, max_rating
    )
    top_main = np.argsort(similarities[mask_main])[::-1][:5]
    recommendations_main = df[mask_main].iloc[top_main]

    print("\n🎬 Allgemeine Empfehlungen:")
    print(recommendations_main[["title", "genres", "year", "mean_rating"]])

    for _, row in recommendations_main.iterrows():
        year_str: str = str(row["year"]) if pd.notna(row["year"]) else "0"
        try:
            release_year: int = int(year_str) if year_str.isdigit() else 0
        except ValueError:
            release_year = 0

        film = state.Film(
            movie_id=str(row["movieId"]),
            imdb_id="nix",
            title=str(row["title"]),
            release_year=release_year,
            genres=str(row["genres"]),
        )
        state.recommended_films_all_time.append(film)

    # --- Alte und neue Filme trennen ---
    df_old = df[df["year"] < 2010].reset_index(drop=True)
    df_new = df[df["year"] >= 2010].reset_index(drop=True)

    genre_old = genre_matrix_dense[df["year"] < 2010]
    genre_new = genre_matrix_dense[df["year"] >= 2010]

    # --- Klassische Empfehlungen ---
    sim_old = cosine_similarity(user_vector.reshape(1, -1), genre_old).flatten()
    mask_old = df_old["mean_rating"].between(min_rating, max_rating)
    top_old = np.argsort(sim_old[mask_old])[::-1][:5]
    recommendations_old = df_old[mask_old].iloc[top_old]

    print("\n📼 Klassiker (vor 2010):")
    print(recommendations_old[["title", "genres", "year", "mean_rating"]])
    for _, row in recommendations_old.iterrows():
        year_str: str = str(row["year"]) if pd.notna(row["year"]) else "0"
        try:
            release_year: int = int(year_str) if year_str.isdigit() else 0
        except ValueError:
            release_year = 0

        film = state.Film(
            movie_id=str(row["movieId"]),
            imdb_id="nix",
            title=str(row["title"]),
            release_year=release_year,
            genres=str(row["genres"]),
        )
        state.recommended_films_classics.append(film)

    # --- Moderne Empfehlungen ---
    sim_new = cosine_similarity(user_vector.reshape(1, -1), genre_new).flatten()
    mask_new = df_new["mean_rating"].between(min_rating, max_rating)
    top_new = np.argsort(sim_new[mask_new])[::-1][:5]
    recommendations_new = df_new[mask_new].iloc[top_new]

    print("\n📱 Moderne Empfehlungen (ab 2010):")
    print(recommendations_new[["title", "genres", "year", "mean_rating"]])
    for _, row in recommendations_new.iterrows():
        year_str: str = str(row["year"]) if pd.notna(row["year"]) else "0"
        try:
            release_year: int = int(year_str) if year_str.isdigit() else 0
        except ValueError:
            release_year = 0

        film = state.Film(
            movie_id=str(row["movieId"]),
            imdb_id="nix",
            title=str(row["title"]),
            release_year=release_year,
            genres=str(row["genres"]),
        )
        state.recommended_films_new_timers.append(film)
