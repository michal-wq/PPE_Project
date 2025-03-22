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


'''
Hier wird Modell getestet, mit selbsterstellten Daten, die genau gleich Aufgebaut sind
'''

x_sample_data = [ 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.01119, 44807.0]
dim = np.size(x_sample_data)

# Fake Array
x = np.zeros((100, dim))
y = np.ones((100, 1))

Model = MovieRecommender(dim)

# Daten spliten
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size = 0.5)

# Dset Objekte instanzieren
training_data = Dset(X_train, y_train)
val_data = Dset(X_val, y_val)
test_data = Dset(X_test, y_test)

# Data loaders instanzieren
train_dataloader = DataLoader(training_data, batch_size = 5, shuffle = True)
validation_dataloader = DataLoader(val_data, batch_size = 5, shuffle = True)
test_dataloader = DataLoader(test_data, batch_size = 5, shuffle = True)

# Zusammenfassung des Models
summary(Model, (x.shape[1],))


criterion = nn.BCELoss()
optimizer = Adam(Model.parameters(), lr = 1e-3)

'''
Training
'''

total_loss_train_plot = []
total_loss_validation_plot = []
total_acc_train_plot = []
total_acc_validation_plot = []

epochs = 10

for epoch in range(epochs):
    total_acc_train = 0
    total_loss_train = 0
    total_acc_val = 0
    total_loss_val = 0
    # Bis hier ist gut
    for data in train_dataloader:
        inputs, labels = data

        prediction = Model(inputs).squeeze(1)

        labels = labels.squeeze(1)

        batch_loss = criterion(prediction, labels)

        total_loss_train += batch_loss.item()

        acc = ((prediction).round() == labels).sum().item()

        total_acc_train += acc

        batch_loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    with torch.no_grad():
        for data in validation_dataloader:
            inputs, labels = data
            prediction = Model(inputs).squeeze(1)
            labels = labels.squeeze(1)  # Auch Labels anpassen
            batch_loss = criterion(prediction, labels)
            total_loss_val += batch_loss.item()
            acc = ((prediction).round() == labels).sum().item()
            total_acc_val += acc

    total_loss_train_plot.append(round(total_loss_train/1000, 4))
    total_loss_validation_plot.append(round(total_loss_val/1000, 4))

    total_acc_train_plot.append(round(total_acc_train/training_data.__len__() * 100, 4))
    total_acc_validation_plot.append(round(total_acc_val/val_data.__len__() * 100, 4))

    print(f'''Epoch no. {epoch + 1} Train Loss: {round(total_loss_train/1000, 4)} Train Accuracy {round(total_acc_train/training_data.__len__() * 100, 4)},
            Validtation Loss: {round(total_loss_val/1000, 4)} Validation Accuracy: {round(total_acc_val/val_data.__len__() * 100, 4)}''')

    print('='*25)
