import torch
import torch.nn as nn

class HexTypeIdentificationBranch(nn.Module):
    def __init__(self, num_hex_types):
        """
        Hexagon type identification branch of the multi-task CNN.
        
        Parameters:
        - num_hex_types: Number of hexagon types in the dataset.
        """
        super(HexTypeIdentificationBranch, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1)

        # Max pooling layers
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Fully connected layers
        self.fc1 = nn.Linear(64, 128)
        self.fc2 = nn.Linear(128, num_hex_types)

        # Activation function
        self.relu = nn.ReLU()

    def forward(self, x):
        """
        Forward pass of the hexagon type identification branch.
        
        Parameters:
        - x: Input tensor (batch_size, channels, height, width).
        
        Returns:
        - Output tensor (batch_size, num_hex_types).
        """
        # Convolutional layers
        x = self.relu(self.conv1(x))
        x = self.pool(x)
        x = self.relu(self.conv2(x))
        x = self.pool(x)
        x = self.relu(self.conv3(x))
        x = self.pool(x)
        x = self.relu(self.conv4(x))
        x = self.pool(x)

        # Global average pooling
        x = torch.mean(x, dim=(2, 3))  # Average pooling across spatial dimensions

        # Fully connected layers
        x = self.relu(self.fc1(x))
        x = self.fc2(x)

        return x
