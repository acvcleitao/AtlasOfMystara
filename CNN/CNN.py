import torch
import torch.nn as nn

from hexagon_identification_branch import HexTypeIdentificationBranch
from hexmap_detection_branch import HexMapDetectionBranch

class MultiTaskCNN(nn.Module):
    def __init__(self, num_hex_types):
        """
        Multi-task CNN model for hexmap detection and hexagon type identification.
        
        Parameters:
        - num_hex_types: Number of hexagon types in the dataset.
        """
        super(MultiTaskCNN, self).__init__()
        
        # Hexagon type identification branch
        self.hex_type_branch = HexTypeIdentificationBranch(num_hex_types)
        
        # Hexmap detection branch
        self.hex_map_branch = HexMapDetectionBranch()
        
    def forward(self, x):
        """
        Forward pass of the multi-task CNN model.
        
        Parameters:
        - x: Input tensor (batch_size, channels, height, width).
        
        Returns:
        - Output tensor for hexagon type identification (batch_size, num_hex_types).
        - Output tensor for hexmap detection (batch_size, 1).
        """
        # Forward pass through hexagon type identification branch
        hex_type_output = self.hex_type_branch(x)
        
        # Forward pass through hexmap detection branch
        hex_map_output = self.hex_map_branch(x)
        
        return hex_type_output, hex_map_output

# Instantiate the MultiTaskCNN model
num_hex_types = 30
multi_task_model = MultiTaskCNN(num_hex_types)

# Print the model architecture
print(multi_task_model)
