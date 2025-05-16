import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# --- Vorverarbeitete Daten laden ---
with open('cached_data.pkl', 'rb') as f:
    data = pickle.load(f)

df = data['df']
genre_matrix_dense = data['genre_matrix_dense']
title_to_index = data['title_to_index']

# --- Nutzereingabe ---
print("Bitte gib 3 Filmtitel ein:")
user_inputs = [input(f"Film {i+1}: ").strip().lower() for i in range(3)]

try:
    min_rating = float(input("Minimale Bewertung (z. B. 2.0): ").strip())
    max_rating = float(input("Maximale Bewertung (z. B. 4.5): ").strip())
except ValueError:
    print("❌ Ungültiger Bewertungsbereich. Abbruch.")
    exit()

# --- Gültige Filme prüfen ---
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

# --- Hauptempfehlungen ---
similarities = cosine_similarity(user_vector.reshape(1, -1), genre_matrix_dense).flatten()
mask_main = (
    ~np.isin(np.arange(len(df)), valid_indices) &
    df['mean_rating'].between(min_rating, max_rating)
)
top_main = np.argsort(similarities[mask_main])[::-1][:5]
recommendations_main = df[mask_main].iloc[top_main]

print("\n🎬 Allgemeine Empfehlungen:")
print(recommendations_main[['title', 'genres', 'year', 'mean_rating']])

# --- Alte & neue Filme aufteilen ---
df_old = df[df['year'] < 2010].reset_index(drop=True)
df_new = df[df['year'] >= 2010].reset_index(drop=True)

genre_old = genre_matrix_dense[df['year'] < 2010]
genre_new = genre_matrix_dense[df['year'] >= 2010]

# --- Klassiker ---
sim_old = cosine_similarity(user_vector.reshape(1, -1), genre_old).flatten()
mask_old = df_old['mean_rating'].between(min_rating, max_rating)
top_old = np.argsort(sim_old[mask_old])[::-1][:5]
recommendations_old = df_old[mask_old].iloc[top_old]

print("\n📼 Klassiker (vor 2010):")
print(recommendations_old[['title', 'genres', 'year', 'mean_rating']])

# --- Moderne Empfehlungen ---
sim_new = cosine_similarity(user_vector.reshape(1, -1), genre_new).flatten()
mask_new = df_new['mean_rating'].between(min_rating, max_rating)
top_new = np.argsort(sim_new[mask_new])[::-1][:5]
recommendations_new = df_new[mask_new].iloc[top_new]

print("\n📱 Moderne Empfehlungen (ab 2010):")
print(recommendations_new[['title', 'genres', 'year', 'mean_rating']])
