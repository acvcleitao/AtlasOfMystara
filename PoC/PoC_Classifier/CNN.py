import torch
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader
from PoC.PoC_Classifier.HexDataset import HexagonDataset
from PoC.PoC_Classifier.HexagonDetectionModule import HexagonDetectionModel

## Example usage
# Specify the path to your hexagon dataset
dataset_path = '/path/to/your/hexagon/dataset'

# Define transformations
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])

# Create an instance of your custom dataset
hexagon_dataset = HexagonDataset(root_dir=dataset_path, transform=transform)

# Accessing a sample
image, hexagon_type = hexagon_dataset[0]

# Set batch size
batch_size = 32

# Create DataLoader
hexagon_dataloader = DataLoader(hexagon_dataset, batch_size=batch_size, shuffle=True)

# Assuming you have a HexagonDetectionModel defined
model = HexagonDetectionModel()

# Define loss function and optimizer
# TODO: Try with more loss functions and optimizers (CrossEntropyLoss BCEWithLogitsLoss SmoothL1Loss SGD Adam Adagrad RMSprop)
# TODO: Try with different learning rates and momentum
criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)


# Set up variables
batch_size = 32
num_epochs = 10

# Training loop
for epoch in range(num_epochs):
    model.train()  # Set the model to training mode

    for batch_images, batch_hexagon_types in hexagon_dataloader:
        # Zero the gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(batch_images)

        # Compute the loss
        loss = criterion(outputs, batch_hexagon_types)  # Assuming batch_hexagon_types are the ground truth labels

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

    # Print the loss after each epoch
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}')

# Adjust the training loop based on your specific hexagon detection model and requirements
# TODO: Validation Dataset?
