from src.models.movie_recommender import MovieRecommender, Dset
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchsummary import summary
import os
from sklearn.model_selection import train_test_split
from torch.optim import Adam
import glob
import pandas as pd
import time
from src.models.functions import load_features, load_labels, estimate_training_time


if __name__ == '__main__':
    x = load_features('../Data/preprocessed/features')
    print('Combined features DataFrame:\n', x.head())

    x_array = x.to_numpy()
    print('\nShape of x_array:', x_array.shape)

    # Anzahl der dimensions
    dim = x_array.shape[1]

    # Features array
    x = x_array

    y_df = load_labels('../Data/preprocessed/label')
    print('Combined labels DataFrame:\n', y_df.head())
    y = y_df.to_numpy()
    print('\nShape of y_array:', y.shape)

    Model = MovieRecommender(dim)

    # Daten spliten
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.5)

    # Dset Objekte instanzieren
    training_data = Dset(X_train, y_train)
    val_data = Dset(X_val, y_val)
    test_data = Dset(X_test, y_test)

    # Data loaders instanzieren
    train_dataloader = DataLoader(training_data, batch_size=5, shuffle=True)
    validation_dataloader = DataLoader(val_data, batch_size=5, shuffle=True)
    test_dataloader = DataLoader(test_data, batch_size=5, shuffle=True)

    # Zusammenfassung des Models
    summary(Model, (x.shape[1],))

    criterion = nn.MSELoss()
    optimizer = Adam(Model.parameters(), lr=1e-3)

    '''
    Estimate training time before running all epochs
    '''
    estimated_time_seconds = estimate_training_time(
        model=Model,
        train_dataloader=train_dataloader,
        criterion=criterion,
        optimizer=optimizer,
        epochs=10,          # total epochs we plan to run
        warmup_batches=1    # number of batches to time
    )
    print(f'Estimated training time for 10 epochs: {estimated_time_seconds:.2f} seconds')

    '''
    Training
    '''
    total_loss_train_plot = []
    total_loss_validation_plot = []
    total_acc_train_plot = []
    total_acc_validation_plot = []

    epochs = 10

    for epoch in range(epochs):
        Model.train()

        total_loss_train = 0.0
        total_se_train = 0.0  # Sum of squared errors for RMSE
        total_samples_train = 0

        for inputs, labels in train_dataloader:
            # Forward
            prediction = Model(inputs)

            # Compute loss
            batch_loss = criterion(prediction, labels)

            # Backprop
            batch_loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            # Accumulate total loss (MSE) and sum of squared errors for RMSE
            bs = inputs.size(0)  # batch size
            total_loss_train += batch_loss.item() * bs
            total_se_train += (prediction - labels).pow(2).sum().item()
            total_samples_train += bs

        # Average MSE across the entire training set
        epoch_mse = total_loss_train / total_samples_train
        # RMSE is sqrt of average MSE
        epoch_rmse = (total_se_train / total_samples_train) ** 0.5

        # Validation loop (similar approach)
        Model.eval()
        val_loss = 0.0
        val_se = 0.0
        val_samples = 0

        with torch.no_grad():
            for inputs, labels in validation_dataloader:
                prediction = Model(inputs)
                batch_loss = criterion(prediction, labels)
                bs = inputs.size(0)
                val_loss += batch_loss.item() * bs
                val_se += (prediction - labels).pow(2).sum().item()
                val_samples += bs

        val_mse = val_loss / val_samples
        val_rmse = (val_se / val_samples) ** 0.5

        print(f'Epoch [{epoch + 1}/{epochs}] '
              f'Train MSE: {epoch_mse:.4f} | Train RMSE: {epoch_rmse:.4f} | '
              f'Val MSE: {val_mse:.4f} | Val RMSE: {val_rmse:.4f}')

    '''
    Save the trained model
    '''
    # Create a directory for saving the model (if it doesn't exist)
    save_dir = '../trained_models'
    os.makedirs(save_dir, exist_ok=True)

    # Define a path for the model
    model_save_path = os.path.join(save_dir, 'movie_recommender.pth')

    # Save only the model's state_dict
    torch.save(Model.state_dict(), model_save_path)
    print(f'Model has been saved to {model_save_path}')
