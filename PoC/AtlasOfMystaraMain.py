import cv2
import numpy as np

class HexTile:
    def __init__(self, tile_size, orientation, position):
        self.tile_size = tile_size
        self.orientation = orientation
        self.position = position

    def draw(self, image):
        # Calculate the position for this hexagon based on its position attribute
        x = self.position[1] * self.tile_size * np.sqrt(3) + (self.position[0] % 2) * (self.tile_size * np.sqrt(3) / 2)
        y = self.position[0] * self.tile_size * 1.5
        # Draw the hexagon
        draw_hexagon(image, (x, y), self.tile_size)

def draw_hexagon(image, center, size):
    angle = np.pi / 6
    vertices = []
    for i in range(6):
        x = center[0] + size * np.cos(angle + i * np.pi / 3)
        y = center[1] + size * np.sin(angle + i * np.pi / 3)
        vertices.append((int(x), int(y)))
    cv2.polylines(image, [np.array(vertices)], isClosed=True, color=(0, 255, 0), thickness=2)


def HexMaker(grid_size, tile_size, orientation):
    """
    grid_size -> tuple of size 2: (width, height)
    tile_size -> size of  the hexagon
    orientation -> 'pointy' or 'flat'
    This function draws a grid of hexagons
    """
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

def drawHexGrid(sizeHex, padding, sizeGrid1, sizeGrid2):
    """Auxiliary function to HexMaker"""
    image_width = int((sizeGrid2 - 0.5) * sizeHex * np.sqrt(3)) + padding * 2
    image_height = int((sizeGrid1 - 1) * sizeHex * 1.5) + padding * 2
    # Create a canvas with the calculated dimensions
    canvas = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    # Draw hexagonal grid with padding
    for row in range(sizeGrid1):
        for col in range(sizeGrid2):
            x = col * sizeHex * np.sqrt(3) + (row % 2) * (sizeHex * np.sqrt(3) / 2)
            y = row * sizeHex * 1.5
            x += padding
            y += padding
            draw_hexagon(canvas, (x, y), sizeHex)
    return canvas

def createCustomHexGrid(grid_shape, tile_size, orientation):
    """
    Creates a custom shaped HexGrid
    grid_shape -> a tuple of tuples that is essentially the whole grid
    tile_size -> size of the hexagons
    orientation -> 'pointy' or 'flat'

    TODO: flat orientation not working correctly
    """
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


def HexFinder(image):
    """
    Finds Hexagons in an image
    image -> image file
    returns a contour of the hexagons found
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    contours, _= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    c = 0
    for i in contours:
            area = cv2.contourArea(i)
            if area > 1000:
                    if area > max_area:
                        max_area = area
                        best_cnt = i
                        image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
            c+=1
    mask = np.zeros((gray.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)

    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]

    blur = cv2.GaussianBlur(out, (5,5), 0)

    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    cv2.imshow("thresh1", thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    averageArea = 0
    counter = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000/2 and area < 2000:
            counter += 1
            averageArea += area

    averageArea = averageArea/counter

    c = 0
    HexFound = np.zeros_like(image)
    for i in contours:
        area = cv2.contourArea(i)
        if area > 700:
            cv2.drawContours(HexFound, contours, c, (0, 255, 0), 3)
        c+=1

    return HexFound



""" Testing
import cv2
import numpy as np
import PoCHexFinder
import PoCHexMaker
import PoCHexTranslator
import Test

image = cv2.imread("your_image3.jpg")

hexFound = PoCHexFinder.HexFinder(image)

cv2.imshow("Final Image", hexFound)
cv2.imshow("Hexagonal Grid", hexFound)
cv2.waitKey(0)
cv2.destroyAllWindows()

result = Test.HexTranslator(hexFound)
# Grid parameters
grid_size = (7, 3)  # Number of hexagons in each direction (width, height)
tile_size = 19     # Size of each hexagon
orientation = 'pointy'  # 'pointy' or 'flat'

finalCanvas = PoCHexMaker.HexMaker(grid_size, result[1], result[2])

cv2.imshow("Hexagonal Grid", finalCanvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""