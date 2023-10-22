import cv2
import numpy as np


def HexMaker(grid_size, tile_size, orientation):
    padding = tile_size*2  # Padding around the hexagonal grid
    match orientation:
        case 'flat':
            print("flat hexagon selected")

            canvas = drawHexGrid(tile_size, padding, grid_size[0], grid_size[1])
            
            # Rotate the canvas by 90 degrees to align with the flat-topped grid
            canvas = cv2.rotate(canvas, cv2.ROTATE_90_CLOCKWISE)
        case 'pointy':
            print("pointy hexagon selected")
            canvas = drawHexGrid(tile_size, padding, grid_size[1], grid_size[0])
        case _:
            print("Invalid hexagon Type")
            SystemExit

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

def drawHexGrid(sizeHex, padding, sizeGrid1, sizeGrid2):
    image_width = int((sizeGrid2 - 0.5) * sizeHex * np.sqrt(3)) + padding * 2
    image_height = int((sizeGrid1 - 1) * sizeHex * 1.5) + padding * 2
    # Create a canvas with the calculated dimensions
    canvas = np.zeros((int(image_height), int(image_width), 3), dtype=np.uint8)

    # Draw hexagonal grid with padding
    for row in range(sizeGrid1):
        for col in range(sizeGrid2):
            x = col * sizeHex * np.sqrt(3) + (row % 2) * (sizeHex * np.sqrt(3) / 2)
            y = row * sizeHex * 1.5
            x += padding
            y += padding
            draw_hexagon(canvas, (x, y), sizeHex)
    return canvas

