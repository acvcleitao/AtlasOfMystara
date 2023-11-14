import torch.nn as nn

class HexagonDetectionModel(nn.Module):
    def __init__(self, num_classes):
        super(HexagonDetectionModel, self).__init__()

        # Convolutional Layers
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Fully Connected Layers
        self.fc1 = nn.Linear(64 * 64 * 64, 128)  # Adjust input size based on your architecture
        self.relu3 = nn.ReLU()

        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        # Convolutional Layer 1
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)

        # Convolutional Layer 2
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)

        # Flatten for Fully Connected Layers
        x = x.view(x.size(0), -1)

        # Fully Connected Layer 1
        x = self.fc1(x)
        x = self.relu3(x)

        # Fully Connected Layer 2 (Output Layer)
        x = self.fc2(x)

        return x
