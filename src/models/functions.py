from src.models.movie_recommender import MovieRecommender, Dset
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import glob
import pandas as pd
import time

def load_features(directory='Data/features'):
    '''
    Reads all CSV files in the specified directory and
    concatenates them into a single DataFrame.

    Args:
        directory (str): Path to the directory containing feature CSV files.

    Returns:
        pd.DataFrame: A DataFrame containing all combined features.
    '''
    # Get a list of all CSV files in the directory
    csv_files = glob.glob(f'{directory}/*.csv')

    # Read each CSV file and store in a list of DataFrames
    df_list = [pd.read_csv(file) for file in csv_files]

    # Concatenate all DataFrames into one
    x = pd.concat(df_list, ignore_index=True)

    return x

def load_labels(directory='Data/label'):
    '''
    Reads all CSV files in the specified directory and
    concatenates them into a single DataFrame (labels).

    Args:
        directory (str): Path to the directory containing label CSV files.

    Returns:
        pd.DataFrame: A DataFrame containing all combined labels.
    '''
    # Get a list of all CSV files in the directory
    csv_files = glob.glob(f'{directory}/*.csv')

    # Read each CSV file and store in a list of DataFrames
    df_list = [pd.read_csv(file) for file in csv_files]

    # Concatenate all DataFrames into one
    y = pd.concat(df_list, ignore_index=True)

    return y

def estimate_training_time(model, train_dataloader, criterion, optimizer, epochs=10, warmup_batches=1):
    '''
    Estimates the total training time by timing a small number of warm-up batches
    and extrapolating to all batches and epochs.

    Args:
        model (nn.Module): The PyTorch model to train.
        train_dataloader (DataLoader): DataLoader for the training set.
        criterion (nn.Module): Loss function (e.g. BCELoss).
        optimizer (torch.optim.Optimizer): Optimizer (e.g. Adam).
        epochs (int): Number of total epochs to train.
        warmup_batches (int): Number of initial batches to time.

    Returns:
        float: Estimated total training time in seconds.
    '''
    # Put the model in training mode
    model.train()

    # We'll time how long it takes to process 'warmup_batches' batches
    start_time = time.time()

    batches_processed = 0
    for i, (inputs, labels) in enumerate(train_dataloader):
        if i >= warmup_batches:
            break
        batch_start = time.time()

        # Forward pass
        prediction = model(inputs).squeeze(1)
        labels = labels.squeeze(1)
        batch_loss = criterion(prediction, labels)

        # Backward pass and update
        batch_loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        batch_end = time.time()
        batches_processed += (batch_end - batch_start)

    if warmup_batches == 0:
        warmup_batches = 1  # avoid division by zero

    average_batch_time = batches_processed / warmup_batches
    total_batches = len(train_dataloader)

    # Estimate total time = average time per batch * total batches * epochs
    estimated_time = average_batch_time * total_batches * epochs

    return estimated_time