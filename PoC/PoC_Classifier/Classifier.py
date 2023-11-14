from HexagonDetectionModule import HexagonDetectionModel
import cv2
import torch
from torchvision import transforms
from PIL import Image

def find_hexagon_size(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming the hexagon is the largest contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        hexagon_size = max(w, h)  # Assuming hexagons are roughly symmetric

        return hexagon_size
    else:
        raise ValueError("No contours found in the image")

def classify_hexagons(image_path, model):
    # Determine hexagon size
    hexagon_size = find_hexagon_size(image_path)

    # Load the image
    image = Image.open(image_path).convert('RGB')

    # Set up transformations
    transform = transforms.Compose([
        transforms.ToTensor(),
        # Add other necessary transformations (e.g., normalization) used during training
    ])

    # Define hexagon step (you may need to adjust this based on your grid)
    hexagon_step = hexagon_size  # Example step, adjust as needed

    # Initialize the list to store hexagon types
    hexagon_types = []

    # Iterate through the image in a grid pattern
    for y in range(0, image.size[1] - hexagon_size, hexagon_step):
        for x in range(0, image.size[0] - hexagon_size, hexagon_step):
            # Crop the hexagon region
            hexagon_region = image.crop((x, y, x + hexagon_size, y + hexagon_size))

            # Preprocess the hexagon region
            hexagon_input = transform(hexagon_region).unsqueeze(0)  # Add a batch dimension

            # Perform inference using the trained CNN
            with torch.no_grad():
                model_output = model(hexagon_input)

            # Extract the predicted hexagon type (modify based on your model's output structure)
            hexagon_type = torch.argmax(model_output, dim=1).item()

            # Save the hexagon type
            hexagon_types.append(hexagon_type)

    return hexagon_types

# Example usage
image_path = 'path_to_your_image.jpg'
trained_model = HexagonDetectionModel()
trained_model.load_state_dict(torch.load('path_to_your_trained_model.pth'))
trained_model.eval()

result = classify_hexagons(image_path, trained_model)
print(result)
