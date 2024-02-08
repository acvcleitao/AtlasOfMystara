import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision.transforms import ToTensor
from CNN.CNN import MultiTaskCNN
from hex_map_dataset import HexMapDataset

# Step 1: Prepare the Dataset
dataset = HexMapDataset(root_dir='Dataset', transform=ToTensor())  # Provide the root directory
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=64)

# Step 2: Define Loss Functions
criterion_hex_type = nn.CrossEntropyLoss()
criterion_hex_map = nn.BCELoss()

# Step 3: Define Multi-task Model
# Define and instantiate the multi-task model here

# Step 4: Define Optimizer
multi_task_model = MultiTaskCNN()  # Instantiate your multi-task model
optimizer = optim.Adam(multi_task_model.parameters(), lr=0.001)  # Move optimizer initialization here

# Step 5: Training Loop
num_epochs = 10
for epoch in range(num_epochs):
    multi_task_model.train()
    for batch_idx, (images, hex_type_labels, hex_map_labels) in enumerate(train_loader):
        optimizer.zero_grad()
        hex_type_output, hex_map_output = multi_task_model(images)
        
        # Calculate loss for hexagon type identification
        loss_hex_type = criterion_hex_type(hex_type_output, hex_type_labels)
        
        # Calculate loss for hexmap detection
        loss_hex_map = criterion_hex_map(hex_map_output, hex_map_labels.float())
        
        # Total loss
        total_loss = loss_hex_type + loss_hex_map
        
        # Backpropagation
        total_loss.backward()
        optimizer.step()
        
        if batch_idx % 100 == 0:
            print(f"Epoch {epoch + 1}/{num_epochs}, Batch {batch_idx}/{len(train_loader)}, "
                  f"Hex Type Loss: {loss_hex_type.item():.4f}, Hex Map Loss: {loss_hex_map.item():.4f}")

# Step 5: Validation Loop
multi_task_model.eval()
total_hex_type_correct = 0
total_hex_map_correct = 0
total_samples = 0
with torch.no_grad():
    for images, hex_type_labels, hex_map_labels in val_loader:
        hex_type_output, hex_map_output = multi_task_model(images)
        
        # Calculate hexagon type prediction accuracy
        _, hex_type_predicted = torch.max(hex_type_output, 1)
        total_hex_type_correct += (hex_type_predicted == hex_type_labels).sum().item()
        
        # Calculate hexmap detection accuracy
        hex_map_predicted = torch.round(hex_map_output)
        total_hex_map_correct += (hex_map_predicted == hex_map_labels).sum().item()
        
        total_samples += hex_type_labels.size(0)

# Calculate accuracy
hex_type_accuracy = total_hex_type_correct / total_samples
hex_map_accuracy = total_hex_map_correct / total_samples

print(f"Validation Accuracy - Hexagon Type Identification: {100 * hex_type_accuracy:.2f}%")
print(f"Validation Accuracy - Hexmap Detection: {100 * hex_map_accuracy:.2f}%")

# Step 6: Save Model
torch.save(multi_task_model.state_dict(), 'multi_task_model.pth')
