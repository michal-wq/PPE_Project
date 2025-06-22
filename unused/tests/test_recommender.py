from src.models.movie_recommender import MovieRecommender, Dset
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split

# Fake-Daten genau wie vorher
x_sample_data = [1,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,-0.01119,44807.0]
dim = len(x_sample_data)
x = np.random.randn(100, dim)
y = np.random.randint(0, 2, size=(100, 1))

# Model, Dataset & Dataloader
model = MovieRecommender(dim)
criterion = nn.MSELoss()            # Regression‐Loss
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
X_test, X_val, y_test, y_val   = train_test_split(X_test, y_test, test_size=0.5)

train_ds = Dset(X_train, y_train)
val_ds   = Dset(X_val,   y_val)
test_ds  = Dset(X_test,  y_test)

train_loader = DataLoader(train_ds, batch_size=5, shuffle=True)
val_loader   = DataLoader(val_ds,   batch_size=5, shuffle=False)
test_loader  = DataLoader(test_ds,  batch_size=5, shuffle=False)

# Training (wie vorher, nur eben mit MSELoss und ohne Accuracy)
for epoch in range(10):
    model.train()
    for Xb, yb in train_loader:
        pred = model(Xb)          # roher Output
        loss = criterion(pred, yb)
        loss.backward(); optimizer.step(); optimizer.zero_grad()

    # Optional: Validation pro Epoch
    model.eval()
    with torch.no_grad():
        mse_sum, se_sum, n = 0.0, 0.0, 0
        for Xb, yb in val_loader:
            pred = model(Xb)
            bs = Xb.size(0)
            mse_sum += criterion(pred, yb).item() * bs
            se_sum  += (pred - yb).pow(2).sum().item()
            n      += bs
        val_mse  = mse_sum / n
        val_rmse = (se_sum / n) ** 0.5
    print(f'Epoch {epoch+1}: Val MSE {val_mse:.4f}, RMSE {val_rmse:.4f}')

# Test‐Evaluation
model.eval()
with torch.no_grad():
    mse_sum, se_sum, n = 0.0, 0.0, 0
    for Xb, yb in test_loader:
        pred = model(Xb)
        bs = Xb.size(0)
        mse_sum += criterion(pred, yb).item() * bs
        se_sum  += (pred - yb).pow(2).sum().item()
        n      += bs
    test_mse  = mse_sum / n
    test_rmse = (se_sum / n) ** 0.5

print(f'Test MSE: {test_mse:.4f}, Test RMSE: {test_rmse:.4f}')
