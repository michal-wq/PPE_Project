import os
import glob
import time

import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

from src.models.movie_recommender import MovieRecommender, Dset
from src.models.functions import estimate_training_time

# ==== Konfiguration ====
EPOCHS = 10
BATCH_SIZE = 128
LR = 1e-3
WARMUP_BATCHES = 5

# ==== Hilfsfunktion Pfade ====
def get_data_paths():
    root = os.getcwd()  # Projekt‑Root
    feat_dir = os.path.join(root, 'Data', 'preprocessed', 'features')
    label_path = os.path.join(root, 'Data', 'preprocessed', 'label', 'label.csv')
    feat_files = sorted(glob.glob(os.path.join(feat_dir, 'features_part_*.csv')))
    return feat_files, label_path

# ==== Haupt ====
if __name__ == '__main__':
    # Phase 1: Pfade holen und Dateien einlesen
    print('[Phase 1] Lade vorverarbeitete Daten …')
    feat_files, label_path = get_data_paths()
    if not feat_files:
        raise RuntimeError(f'Keine Feature-Dateien in Data/preprocessed/features/')
    if not os.path.exists(label_path):
        raise RuntimeError(f'Label-Datei fehlt: {label_path}')

    df_feats = pd.concat([pd.read_csv(f) for f in feat_files], ignore_index=True)
    df_label = pd.read_csv(label_path)
    print(f'[Phase 1] Geladene Daten: {df_feats.shape[0]} Samples × {df_feats.shape[1]} Features')

    # Phase 2: Arrays vorbereiten
    print('[Phase 2] Baue NumPy‑Arrays …')
    # User‑IDs sauber casten
    df_feats['userId'] = pd.to_numeric(df_feats['userId'], errors='coerce') \
                             .fillna(0).astype(int)
    user_ids   = df_feats['userId'].values                    # (N,)
    item_feats = df_feats.drop(columns=['userId']).values     # (N, F)
    ratings    = df_label['rating'].values.reshape(-1,1)      # (N,1)
    print(f'[Phase 2] shapes: users={user_ids.shape}, items={item_feats.shape}, ratings={ratings.shape}')

    # Phase 3: Split in Train/Val/Test
    print('[Phase 3] Splitte in Train/Val/Test …')
    X_tr, X_tmp, u_tr, u_tmp, y_tr, y_tmp = train_test_split(
        item_feats, user_ids, ratings, test_size=0.3, random_state=42
    )
    X_val, X_te, u_val, u_te, y_val, y_te = train_test_split(
        X_tmp, u_tmp, y_tmp, test_size=0.5, random_state=42
    )
    print(f'[Phase 3] Samples: Train={len(X_tr)}, Val={len(X_val)}, Test={len(X_te)}')

    # Phase 4: DataLoader aufsetzen
    print('[Phase 4] Erstelle DataLoader …')
    train_loader = DataLoader(Dset(X_tr, u_tr, y_tr), batch_size=BATCH_SIZE, shuffle=True)
    val_loader   = DataLoader(Dset(X_val, u_val, y_val), batch_size=BATCH_SIZE)
    test_loader  = DataLoader(Dset(X_te,  u_te,  y_te),  batch_size=BATCH_SIZE)
    print(f'[Phase 4] Batch size: {BATCH_SIZE}')

    # Phase 5: Modell, Loss und Optimizer initialisieren
    print('[Phase 5] Initialisiere Modell …')
    input_dim = item_feats.shape[1]
    num_users = int(user_ids.max()) + 1
    model     = MovieRecommender(input_dim, num_users)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    print(f'[Phase 5] input_dim={input_dim}, num_users={num_users}, lr={LR}')

    # Phase 6: Trainingszeit schätzen
    print('[Phase 6] Schätze Trainingszeit …')
    eta = estimate_training_time(
        model=model,
        train_dataloader=train_loader,
        criterion=criterion,
        optimizer=optimizer,
        epochs=EPOCHS,
        warmup_batches=WARMUP_BATCHES
    )
    print(f'[Phase 6] Geschätzte Zeit für {EPOCHS} Epochen: {eta:.1f}s')

    # Phase 7: Training
    print('[Phase 7] Starte Training …')
    for ep in range(1, EPOCHS+1):
        # Training
        model.train()
        running_loss = 0.0
        for x_i, u_i, y_i in train_loader:
            pred = model(x_i, u_i)
            loss = criterion(pred, y_i)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            running_loss += loss.item() * x_i.size(0)
        train_mse = running_loss / len(train_loader.dataset)

        # Validierung
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for x_i, u_i, y_i in val_loader:
                val_loss += criterion(model(x_i, u_i), y_i).item() * x_i.size(0)
        val_mse = val_loss / len(val_loader.dataset)

        print(f'  Epoch {ep}/{EPOCHS} — Train MSE: {train_mse:.4f}, Val MSE: {val_mse:.4f}')

    # Phase 8: Test-Auswertung
    print('[Phase 8] Test-Auswertung …')
    model.eval()
    test_loss = 0.0
    with torch.no_grad():
        for x_i, u_i, y_i in test_loader:
            test_loss += criterion(model(x_i, u_i), y_i).item() * x_i.size(0)
    test_mse = test_loss / len(test_loader.dataset)
    print(f'[Phase 8] Test MSE: {test_mse:.4f}')

    # Phase 9: Modell speichern
    print('[Phase 9] Speichere Modell …')
    save_dir = os.path.join(os.getcwd(), 'trained_models')
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, 'movie_recommender.pth')
    torch.save(model.state_dict(), path)
    print(f'[Phase 9] Modell gespeichert nach {path}')
