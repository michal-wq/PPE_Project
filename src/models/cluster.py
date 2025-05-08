import os
import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from annoy import AnnoyIndex
from src.models.functions import load_features

# ————— CONFIG —————
FEATURE_PATH       = '../../Data/preprocessed_cluster/features'
CLUSTER_MODEL_FILE = '/Users/michal/Documents/PPE_Project/trained_models/dbscan_model.joblib'   # where the fitted DBSCAN will be saved
EPS                = 3
MIN_SAMPLES        = 2
N_TREES            = 50

# ————— LOAD DATA —————
df = load_features(FEATURE_PATH)
feature_cols = df.columns.difference(['movieId'])
X = df[feature_cols].to_numpy().astype('float32')

# ————— LOAD OR FIT & SAVE DBSCAN —————
if os.path.exists(CLUSTER_MODEL_FILE):
    print(f"Loading saved DBSCAN from {CLUSTER_MODEL_FILE}")
    clustering = joblib.load(CLUSTER_MODEL_FILE)
else:
    print("Fitting DBSCAN for the first time…")
    clustering = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES, metric='euclidean')
    clustering.fit(X)
    joblib.dump(clustering, CLUSTER_MODEL_FILE)
    print(f"Saved DBSCAN model to {CLUSTER_MODEL_FILE}")

labels = clustering.labels_



