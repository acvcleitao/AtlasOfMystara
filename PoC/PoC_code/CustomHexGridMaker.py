import cv2
import numpy as np

def createCustomHexGrid(grid_shape, tile_size, orientation):
    # Calculate the dimensions of the canvas based on the custom grid shape
    num_rows = len(grid_shape)
    num_cols = max(len(row) for row in grid_shape)
    padding = tile_size * 2  # Padding around the hexagonal grid
    image_width = int((num_cols - 0.5) * tile_size * np.sqrt(3)) + padding * 2
    image_height = int((num_rows - 1) * tile_size * 1.5) + padding * 2

    # Create a canvas with the calculated dimensions
    canvas = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    for row_idx, row in enumerate(grid_shape):
        for col_idx, exists in enumerate(row):
            if exists:
                x = col_idx * tile_size * np.sqrt(3) + (row_idx % 2) * (tile_size * np.sqrt(3) / 2)
                y = row_idx * tile_size * 1.5
                x += padding
                y += padding
                draw_hexagon(canvas, (x, y), tile_size)

    if orientation == 'flat':
        canvas = cv2.rotate(canvas, cv2.ROTATE_90_CLOCKWISE)

    return canvas

# Function to draw a regular hexagon
def draw_hexagon(image, center, size):
    angle = np.pi / 6
    vertices = []
    for i in range(6):
        x = center[0] + size * np.cos(angle + i * np.pi / 3)
        y = center[1] + size * np.sin(angle + i * np.pi / 3)
        vertices.append((int(x), int(y)))
    cv2.polylines(image, [np.array(vertices)], isClosed=True, color=(0, 255, 0), thickness=2)

def HexMaker(tile_size, orientation, grid_size=None, custom_grid_shape=None):
    if grid_size is not None:
        # Calculate grid size from the provided dimensions
        num_rows, num_cols = grid_size
        grid_shape = ((1,) * num_cols,) * num_rows
    elif custom_grid_shape is not None:
        grid_shape = custom_grid_shape
    else:
        raise ValueError("Must provide either grid_size or custom_grid_shape")

    canvas = createCustomHexGrid(grid_shape, tile_size, orientation)
    return canvas

# Example usage:
custom_grid_shape = ((1, 1, 1), (0, 1, 1), (0, 1, 1), (1, 1, 1))
canvas = HexMaker(tile_size=30, orientation='flat', custom_grid_shape=custom_grid_shape)
cv2.imwrite("custom_hex_grid.png", canvas)
