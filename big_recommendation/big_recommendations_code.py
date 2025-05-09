import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Ordnerpfade vorbereiten (relativ zum Skript selbst) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RATINGS_DIR = os.path.join(BASE_DIR, 'ratings')
MOVIES_PATH = os.path.join(BASE_DIR, 'movies.csv')

# --- Movies laden und bereinigen ---
df = pd.read_csv(MOVIES_PATH)
df['year'] = df['title'].str.extract(r'\((\d{4})\)')
df['title'] = df['title'].str.replace(r'\s*\(\d{4}\)', '', regex=True).str.strip()
df['year'] = df['year'].astype('Int64')
df = df.dropna(subset=['year'])

# --- Genres vektorisieren ---
vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'))
genre_matrix = vectorizer.fit_transform(df['genres'])

# --- Mapping: Titel zu Index ---
title_to_index = {t.lower(): i for i, t in enumerate(df['title'])}

# --- Ratings-Dateien einlesen und mittlere Bewertung berechnen ---
ratings_list = []
for i in range(33):
    path = os.path.join(RATINGS_DIR, f"ratings_{i}.csv")
    df_r = pd.read_csv(path, usecols=['movieId', 'rating'])
    ratings_list.append(df_r)

ratings_all = pd.concat(ratings_list, ignore_index=True)
mean_ratings = ratings_all.groupby('movieId')['rating'].mean().reset_index()
mean_ratings.rename(columns={'rating': 'mean_rating'}, inplace=True)

# --- Movies mit Ratings zusammenführen ---
df = pd.merge(df, mean_ratings, left_on='movieId', right_on='movieId', how='left')

# --- Nutzer-Input ---
print("Bitte gib 3 Filmtitel ein:")
user_inputs = [input(f"Film {i+1}: ").strip().lower() for i in range(3)]

try:
    min_rating = float(input("Minimale Bewertung (z. B. 2.0): ").strip())
    max_rating = float(input("Maximale Bewertung (z. B. 4.5): ").strip())
except ValueError:
    print("❌ Ungültiger Bewertungsbereich. Abbruch.")
    exit()

# --- Gültige Filme identifizieren ---
valid_indices = []
for title in user_inputs:
    if title in title_to_index:
        valid_indices.append(title_to_index[title])
    else:
        print(f"⚠️  Film nicht gefunden: {title}")

if not valid_indices:
    print("❌ Keine gültigen Filme eingegeben. Abbruch.")
    exit()

# --- Durchschnittlicher Genre-Vektor ---
user_vector = genre_matrix[valid_indices].mean(axis=0).A.flatten()

# --- Ähnlichkeiten berechnen ---
similarities = cosine_similarity(user_vector.reshape(1, -1), genre_matrix).flatten()

# --- Empfehlungen: Top-N, ausgeschlossen Input + Filter nach Ratingbereich ---
top_n = 5
recommendations = similarities.argsort()[::-1]
recommendations = [i for i in recommendations if i not in valid_indices]
recommendations = [
    i for i in recommendations
    if pd.notna(df.iloc[i]['mean_rating']) and min_rating <= df.iloc[i]['mean_rating'] <= max_rating
][:top_n]

print("\n🎬 Allgemeine Empfehlungen:")
print(df.iloc[recommendations][['title', 'genres', 'year', 'mean_rating']])

# --- Klassisch (vor 2010) / Modern (ab 2010) aufteilen ---
old_mask = df['year'] < 2010
new_mask = df['year'] >= 2010

df_old = df[old_mask].reset_index(drop=True)
df_new = df[new_mask].reset_index(drop=True)

genre_old = genre_matrix[old_mask.values]
genre_new = genre_matrix[new_mask.values]

# --- Ähnlichkeit für alt und neu ---
sim_old = cosine_similarity(user_vector.reshape(1, -1), genre_old).flatten()
sim_new = cosine_similarity(user_vector.reshape(1, -1), genre_new).flatten()

rec_old = [
    i for i in sim_old.argsort()[::-1]
    if pd.notna(df_old.iloc[i]['mean_rating']) and min_rating <= df_old.iloc[i]['mean_rating'] <= max_rating
][:top_n]

rec_new = [
    i for i in sim_new.argsort()[::-1]
    if pd.notna(df_new.iloc[i]['mean_rating']) and min_rating <= df_new.iloc[i]['mean_rating'] <= max_rating
][:top_n]

print("\n📼 Klassiker (vor 2010):")
print(df_old.iloc[rec_old][['title', 'genres', 'year', 'mean_rating']])

print("\n📱 Moderne Empfehlungen (ab 2010):")
print(df_new.iloc[rec_new][['title', 'genres', 'year', 'mean_rating']])
