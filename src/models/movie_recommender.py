import torch
import torch.nn as nn
import torch.nn.functional as F

class MovieRecommender(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        """
        Args:
            input_dim (int): Size of the input feature vector.
            hidden_dim (int): Number of neurons in the first hidden layer.
        """
        # In Python, the super() function is used to refer to the parent class or superclass.
        # It allows you to call methods defined in the superclass from the subclass, enabling
        # you to extend and customize the functionality inherited from the parent class.
        # https://www.geeksforgeeks.org/python-super/
        super(MovieRecommender, self).__init__()
        # First layer
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        # Second layer
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        # Output layer
        self.fc3 = nn.Linear(hidden_dim // 2, 1)

    def forward(self, x):
        # Apply first layer and activation
        x = F.relu(self.fc1(x))
        # Apply second layer and activation
        x = F.relu(self.fc2(x))
        # Output layer
        rating = self.fc3(x)
        return rating
