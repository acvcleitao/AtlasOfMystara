import cv2
import numpy as np
from collections import Counter
import os
from uuid import uuid4

def extract_hexagons(image_path):
    original_image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    # Define a color range for the hexagons based on the provided colors
    lower_color = np.array([0, 50, 50], dtype=np.uint8)  # Lower bound for any color
    upper_color = np.array([255, 255, 255], dtype=np.uint8)  # Upper bound for any color

    # Create a mask using the color range
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    hexagon_images = []
    hexagon_positions = []  # Stores the (x, y) positions of identified hexagons

    min_hexagon_size = 500  # Adjust this value based on the minimum size of your hexagons

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)  # Adjust the epsilon parameter

        if len(approx) == 6:
            x, y, w, h = cv2.boundingRect(approx)

            # Filter contours based on size
            if w * h > min_hexagon_size:
                hexagon_image = original_image[y:y+h, x:x+w]
                hexagon_images.append(hexagon_image)
                hexagon_positions.append((x, y))

    print(f"Phase 1: Found {len(hexagon_images)} hexagons.")

    # Display the original image without contours for phase 1
    cv2.imshow('Original Image - Phase 1', original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return hexagon_images, hexagon_positions, original_image

def fill_missing_hexagons(hexagon_images, hexagon_positions, original_image):
    # Assuming hexagons are arranged in a grid, find the positions of columns and rows
    column_positions = sorted(list(set(x for x, _ in hexagon_positions)))
    row_positions = sorted(list(set(y for _, y in hexagon_positions)))

    # Calculate the most common hexagon size
    hexagon_sizes = [image.shape[0] for image in hexagon_images]
    most_common_size = Counter(hexagon_sizes).most_common(1)[0][0]

    # Calculate the width of the columns using the size of the hexagon
    column_width = most_common_size

    num_columns = len(column_positions)
    num_rows = len(row_positions)
    padding = 3

    # Calculate the positions of lower and right sides of the columns and rows
    column_lower_sides = [y + padding + most_common_size for y in row_positions]
    column_right_sides = [x + padding + column_width for x in column_positions]

    # Generate a 2D array to represent the grid of hexagons
    grid = [[None] * num_columns for _ in range(num_rows)]

    # Fill in the grid with identified hexagons
    for hexagon_image, (x, y) in zip(hexagon_images, hexagon_positions):
        # Calculate the column index for the hexagon
        col_index = min(range(num_columns), key=lambda i: abs(column_positions[i] - x))

        # Calculate the row index for the hexagon
        row_index = min(range(num_rows), key=lambda i: abs(row_positions[i] - y))

        # Only fill the grid if the cell is empty
        if grid[row_index][col_index] is None:
            grid[row_index][col_index] = hexagon_image

    # Fill in missing hexagons
    for row_index in range(num_rows):
        for col_index in range(num_columns):
            if grid[row_index][col_index] is None:
                # Use some placeholder or blank image for missing hexagons
                grid[row_index][col_index] = np.zeros((most_common_size, most_common_size, 3), dtype=np.uint8)  # Placeholder image size

    print("Phase 2: Filled missing hexagons.")

    # Display the visualized image with row and column positions
    visualized_image = np.copy(original_image)

    # Initialize the dataset directory path
    dataset_dir = r"C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\CNN\Dataset"

    # Display each sector isolated
    for row_index in range(num_rows):
        for col_index in range(num_columns):
            # Only process the sector if it's not empty
            if not np.all(grid[row_index][col_index] == 0):
                sector_image = visualized_image[row_positions[row_index]:column_lower_sides[row_index], 
                                                column_positions[col_index]:column_right_sides[col_index]]
                cv2.imshow(f'Sector {row_index}-{col_index}', sector_image)
                cv2.imshow('Original Image - Phase 2', visualized_image)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
                hexagon_name = input(f"Enter a name for hexagon at row {row_index}, column {col_index} (type 'no' to skip): ").strip()
                if hexagon_name.lower() == "no":
                    continue  # Skip saving this hexagon
                subfolder_name = hexagon_name.lower()
                subfolder_path = os.path.join(dataset_dir, subfolder_name)
                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)
                hexagon_uid = uuid4().hex
                hexagon_filename = f"{hexagon_name}_{hexagon_uid}.png"
                hexagon_path = os.path.join(subfolder_path, hexagon_filename)
                cv2.imwrite(hexagon_path, sector_image)

    cv2.destroyAllWindows()  # Move this line outside the loop

    return grid


if __name__ == "__main__":
    image_path = input("Enter the path to the image: ").strip()
    hexagon_images, hexagon_positions, original_image = extract_hexagons(image_path)
    grid = fill_missing_hexagons(hexagon_images, hexagon_positions, original_image)
