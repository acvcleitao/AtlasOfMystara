import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision.transforms import ToTensor, Resize, Compose
from CNN import MultiTaskCNN
from hex_type_dataset import HexTypeDataset
from hex_map_dataset import HexMapDataset  # Import the HexMapDataset class

# Define transforms
transform = Compose([
    Resize((64, 64)),
    ToTensor(),
])

# Step 1: Prepare the Datasets
hex_type_dataset = HexTypeDataset(root_dir=r'C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\CNN\Dataset', transform=transform)
hex_map_dataset = HexMapDataset(root_dir=r'C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\CNN\MapDataset', transform=transform)

# Step 2: Create Data Loaders
train_size = int(0.8 * len(hex_type_dataset))
val_size = len(hex_type_dataset) - train_size
train_hex_type_dataset, val_hex_type_dataset = random_split(hex_type_dataset, [train_size, val_size])

train_loader_hex_type = DataLoader(train_hex_type_dataset, batch_size=64, shuffle=True)
val_loader_hex_type = DataLoader(val_hex_type_dataset, batch_size=64)

train_size = int(0.8 * len(hex_map_dataset))
val_size = len(hex_map_dataset) - train_size
train_hex_map_dataset, val_hex_map_dataset = random_split(hex_map_dataset, [train_size, val_size])

train_loader_hex_map = DataLoader(train_hex_map_dataset, batch_size=64, shuffle=True)
val_loader_hex_map = DataLoader(val_hex_map_dataset, batch_size=64)

# Step 3: Define Loss Functions
criterion_hex_type = nn.CrossEntropyLoss()
criterion_hex_map = nn.BCELoss()

# Step 4: Define Multi-task Model
num_hex_types = 58  # Assuming there are 58 hexagon types
multi_task_model = MultiTaskCNN(num_hex_types)

# Step 5: Define Optimizer
optimizer = optim.Adam(multi_task_model.parameters(), lr=0.001)

# Step 6: Training Loop for Hexagon Type Identification
num_epochs = 10
for epoch in range(num_epochs):
    multi_task_model.train()
    total_hex_type_correct_epoch = 0  # Initialize total correct predictions for the current epoch
    total_samples_hex_type = 0  # Initialize total samples for hex type
    for batch_idx, (images_hex_type, hex_type_labels, _) in enumerate(train_loader_hex_type):
        optimizer.zero_grad()
        hex_type_output, hex_map_output = multi_task_model(images_hex_type)
        
        loss_hex_type = criterion_hex_type(hex_type_output, hex_type_labels)
        loss_hex_type.backward()
        optimizer.step()
        
        if batch_idx % 100 == 0:
            print(f"Epoch {epoch + 1}/{num_epochs}, Batch {batch_idx}/{len(train_loader_hex_type)}, "
                  f"Hex Type Loss: {loss_hex_type.item():.4f}")

        # Accumulate the total number of predictions made
        total_samples_hex_type += images_hex_type.size(0)

        # Calculate the number of correct predictions for the current epoch
        _, predicted_hex_type = torch.max(hex_type_output, 1)
        total_hex_type_correct_epoch += (predicted_hex_type == hex_type_labels).sum().item()
    """
        # Print predictions and labels for transparency
        for i in range(len(hex_type_labels)):
            print(f"Tried to predict hexagon type of label {hex_type_labels[i]} and guessed {predicted_hex_type[i]}")
    """
    # Calculate accuracy for hexagon type identification after each epoch
    hex_type_accuracy_epoch = total_hex_type_correct_epoch / total_samples_hex_type * 100  # Convert to percentage
    print(f"Total Hex Type Predictions: {total_samples_hex_type}")  # Print total number of predictions
    print(f"Total Hex Type Correct Predictions (Epoch {epoch + 1}): {total_hex_type_correct_epoch}")  # Print total number of correct predictions for the current epoch
    print(f"Avg Hex Type Loss: {loss_hex_type.item():.4f}, Avg Hex Type Accuracy (Epoch {epoch + 1}): {hex_type_accuracy_epoch:.4f}%")

# Step 7: Training Loop for Hexmap Detection
for epoch in range(num_epochs):
    multi_task_model.train()
    total_hex_map_correct_epoch = 0  # Initialize total correct predictions for the current epoch
    total_samples_hex_map = 0  # Initialize total samples for hex map
    for batch_idx, (images_hex_map, hex_map_labels, _) in enumerate(train_loader_hex_map):
        optimizer.zero_grad()
        hex_type_output, hex_map_output = multi_task_model(images_hex_map)
        
        # Convert hex_map_labels to float and reshape to match output shape
        hex_map_labels = hex_map_labels.float().unsqueeze(1)
        
        loss_hex_map = criterion_hex_map(hex_map_output, hex_map_labels)
        loss_hex_map.backward()
        optimizer.step()
        
        if batch_idx % 100 == 0:
            print(f"Epoch {epoch + 1}/{num_epochs}, Batch {batch_idx}/{len(train_loader_hex_map)}, "
                  f"Hex Map Loss: {loss_hex_map.item():.4f}")

        # Accumulate the total number of predictions made
        total_samples_hex_map += images_hex_map.size(0)

        # Calculate the number of correct predictions for the current epoch
        predicted_hex_map = torch.round(hex_map_output)
        total_hex_map_correct_epoch += (predicted_hex_map == hex_map_labels).sum().item()

        """# Print predictions and labels for transparency
        for i in range(len(hex_map_labels)):
            print(f"Tried to predict hexagon map of label {hex_map_labels[i]} and guessed {predicted_hex_map[i]}")
        """
    # Calculate accuracy for hexmap detection after each epoch
    hex_map_accuracy_epoch = total_hex_map_correct_epoch / total_samples_hex_map * 100  # Convert to percentage
    print(f"Total Hex Map Predictions: {total_samples_hex_map}")  # Print total number of predictions
    print(f"Total Hex Map Correct Predictions (Epoch {epoch + 1}): {total_hex_map_correct_epoch}")  # Print total number of correct predictions for the current epoch
    print(f"Avg Hex Map Loss: {loss_hex_map.item():.4f}, Avg Hex Map Accuracy (Epoch {epoch + 1}): {hex_map_accuracy_epoch:.4f}%")
