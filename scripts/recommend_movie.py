import torch
import numpy as np
import pandas as pd
from src.models.movie_recommender import MovieRecommender
from src.models.functions import load_features

if __name__ == '__main__':
    # --- 0) IDs der 3 Filme, die Du schon gesehen hast ---
    watched_movie_ids = [1, 208947, 24]

    # --- 1) Alle Feature‑CSVs laden und Duplikate nach movieId entfernen ---
    df = load_features('../Data/preprocessed/features')
    df = df.drop_duplicates(subset='movieId', keep='first').reset_index(drop=True)
    print('Unique movies insgesamt:', len(df))

    # --- 2) Liste aller Spalten, inklusive movieId, um input_dim=23 zu erhalten ---
    all_cols = df.columns.tolist()

    # --- 3) Die drei gesehenen Filme extrahieren ---
    df_watched = df[df['movieId'].isin(watched_movie_ids)]
    print('Gefundene gesehen Filme (sollten 3 sein):', len(df_watched))

    # --- 4) Kandidaten = alle außer den drei gesehenen ---
    df_cand = df[~df['movieId'].isin(watched_movie_ids)].reset_index(drop=True)
    print('Kandidaten nach Entfernen der 3 gesehenen:', len(df_cand))

    # --- 5) Bestimme echte Feature‑Spalten (alles außer movieId) ---
    feature_only_cols = [c for c in all_cols if c != 'movieId']

    # --- 6) Finde die gemeinsamen Feature‑Spalten der drei gesehenen Filme ---
    mask_common = (df_watched[feature_only_cols] != 0).any(axis=0)
    common_features = mask_common[mask_common].index.tolist()
    print('Gemeinsame Feature‑Spalten der 3 gesehenen Filme:', common_features)

    # --- 7) Filtere Kandidaten auf diejenigen, die in mindestens einer gemeinsamen Feature‑Spalte !=0 sind ---
    df_cand = df_cand[(df_cand[common_features] != 0).any(axis=1)].reset_index(drop=True)
    print('Kandidaten nach Feature‑Filter:', len(df_cand))

    # --- 8) Baue Input‑Array und ID‑Array, diesmal mit allen 23 Spalten (inkl. movieId) ---
    X = df_cand[all_cols].to_numpy(dtype=np.float32)
    movie_ids = df_cand['movieId'].to_numpy()

    # --- 9) Modell initialisieren und Gewichte laden ---
    input_dim = X.shape[1]  # jetzt 23
    model = MovieRecommender(input_dim)
    state = torch.load('../trained_models/movie_recommender.pth', map_location='cpu')
    model.load_state_dict(state)
    model.eval()

    # --- 10) Vorhersage für alle Kandidaten ---
    with torch.no_grad():
        scores = model(torch.from_numpy(X)).squeeze(1).numpy()

    # --- 11) Besten Kandidaten finden ---
    best_idx = np.argmax(scores)
    best_movie_id = movie_ids[best_idx]
    best_score = scores[best_idx]

    # --- 12) Titel aus raw/movies.csv holen ---
    movies = pd.read_csv('../Data/raw/movies.csv')
    title = movies.loc[movies['movieId'] == best_movie_id, 'title'].iloc[0]

    # --- 13) Ausgabe ---
    print('Gesehene movieIds:', watched_movie_ids)
    print(f'Recommended movieId: {best_movie_id}  →  "{title}"  (predicted rating: {best_score:.4f})')
