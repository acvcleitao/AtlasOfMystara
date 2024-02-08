import torch
import torch.nn as nn

class HexMapDetectionBranch(nn.Module):
    def __init__(self):
        """
        Hexmap detection branch of the multi-task CNN.
        """
        super(HexMapDetectionBranch, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)

        # Max pooling layers
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Fully connected layers
        self.fc1 = nn.Linear(32 * 16 * 16, 128)
        self.fc2 = nn.Linear(128, 1)  # Binary classification (hexmap or non-hexmap)

        # Activation function
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """
        Forward pass of the hexmap detection branch.
        
        Parameters:
        - x: Input tensor (batch_size, channels, height, width).
        
        Returns:
        - Output tensor (batch_size, 1).
        """
        # Convolutional layers
        x = self.relu(self.conv1(x))
        x = self.pool(x)
        x = self.relu(self.conv2(x))
        x = self.pool(x)

        # Flatten
        x = x.view(-1, 32 * 16 * 16)

        # Fully connected layers
        x = self.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))  # Sigmoid for binary classification

        return x
