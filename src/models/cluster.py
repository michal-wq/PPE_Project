import os
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster     import DBSCAN
from scipy.sparse        import coo_matrix, vstack, save_npz, load_npz
from src.models.functions import load_features

FEATURE_PATH  = '../../Data/preprocessed_cluster/features'
GRAPH_DIR     = '../../Data/graph_chunks'      # folder to hold per‐chunk .npz files
LABELS_FILE   = 'dbscan_labels.npy'
EPS           = 3.0
MIN_SAMPLES   = 2
CHUNK_SIZE    = 200_000            # tune down until you stop OOM
N_JOBS        = -1

os.makedirs(GRAPH_DIR, exist_ok=True)

# 1) load your feature matrix
df = load_features(FEATURE_PATH)
feature_cols = df.columns.difference(['movieId'])
X = df[feature_cols].to_numpy(dtype=np.float32)
N = X.shape[0]

# 2) build or load the radius‐neighbor graph
#    we’ll produce chunk files: graph_chunks/chunk_0.npz, chunk_1.npz, …
chunk_files = sorted(os.listdir(GRAPH_DIR))
if not chunk_files:
    print("➤ Building neighbor‐graph in chunks…")
    nn = NearestNeighbors(
        radius=EPS,
        metric='euclidean',
        n_jobs=N_JOBS
    ).fit(X)

    for chunk_idx, start in enumerate(range(0, N, CHUNK_SIZE)):
        end = min(N, start + CHUNK_SIZE)
        X_chunk = X[start:end]

        nbr_idxs, nbr_dists = nn.radius_neighbors(
            X_chunk,
            radius=EPS,
            return_distance=True
        )

        # turn this chunk into a COO block of shape (chunk_len, N)
        rows = []
        cols = []
        data = []
        for local_i, (inds, dists) in enumerate(zip(nbr_idxs, nbr_dists)):
            global_i = start + local_i
            rows.extend([local_i] * len(inds))
            cols.extend(inds.tolist())
            data.extend(dists.tolist())

        coo = coo_matrix((data, (rows, cols)),
                         shape=(end - start, N),
                         dtype=np.float32)

        fn = os.path.join(GRAPH_DIR, f"chunk_{chunk_idx}.npz")
        save_npz(fn, coo.tocsr())
        print(f"  • wrote {fn}  ({end-start}×{N}, nnz={coo.nnz})")

    chunk_files = sorted(os.listdir(GRAPH_DIR))

# 3) load all the chunked CSR blocks and stack them
print("➤ Loading & stitching graph…")
blocks = []
for fn in chunk_files:
    path = os.path.join(GRAPH_DIR, fn)
    blocks.append(load_npz(path))
    print(f"  • loaded {fn}")

# This vstack gives you a full (N×N) CSR matrix of distances ≤ EPS
A = vstack(blocks, format='csr')
print("➤ done – full graph shape:", A.shape, "nnz:", A.nnz)

# 4) cluster with DBSCAN on the precomputed sparse graph
if os.path.exists(LABELS_FILE):
    labels = np.load(LABELS_FILE)
    print("➤ loaded saved labels")
else:
    print("➤ running DBSCAN(metric='precomputed')…")
    db = DBSCAN(
        eps=EPS,
        min_samples=MIN_SAMPLES,
        metric='precomputed',
        n_jobs=N_JOBS
    )
    labels = db.fit_predict(A)
    np.save(LABELS_FILE, labels)
    print("➤ labels saved to", LABELS_FILE)

# `labels` is now your (N,) array of cluster IDs
