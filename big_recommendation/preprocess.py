import os
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer

# --- Pfade setzen ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RATINGS_DIR = os.path.join(BASE_DIR, 'ratings')
MOVIES_PATH = os.path.join(BASE_DIR, 'movies.csv')

# --- Filme laden ---
df = pd.read_csv(MOVIES_PATH)
df['year'] = df['title'].str.extract(r'\((\d{4})\)')
df['title'] = df['title'].str.replace(r'\s*\(\d{4}\)', '', regex=True).str.strip()
df['year'] = df['year'].astype('Int64')
df = df.dropna(subset=['year'])

# --- Genres vektorisieren ---
vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'))
genre_matrix = vectorizer.fit_transform(df['genres'])
genre_matrix_dense = genre_matrix.toarray()

# --- Ratings laden & mittlere Bewertung berechnen ---
ratings_list = []
for i in range(33):
    path = os.path.join(RATINGS_DIR, f"ratings_{i}.csv")
    df_r = pd.read_csv(path, usecols=['movieId', 'rating'])
    ratings_list.append(df_r)

ratings_all = pd.concat(ratings_list, ignore_index=True)
mean_ratings = ratings_all.groupby('movieId')['rating'].mean().reset_index()
mean_ratings.rename(columns={'rating': 'mean_rating'}, inplace=True)

# --- Zusammenführen ---
df = pd.merge(df, mean_ratings, on='movieId', how='left')

# --- Mapping: Titel → Index ---
title_to_index = {t.lower(): i for i, t in enumerate(df['title'])}

# --- Alles speichern ---
with open('cached_data.pkl', 'wb') as f:
    pickle.dump({
        'df': df,
        'genre_matrix_dense': genre_matrix_dense,
        'title_to_index': title_to_index
    }, f)

print("✅ Daten wurden erfolgreich verarbeitet und gespeichert.")
