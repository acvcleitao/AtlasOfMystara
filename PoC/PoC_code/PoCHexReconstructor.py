import cv2
import numpy as np

def HexReconstructor(image):
    # Detect grid lines using Hough Line Transform
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=100, maxLineGap=10)

    # Calculate intersection points
    intersection_points = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            intersection_points.append((x1, y1))
            intersection_points.append((x2, y2))

    # Calculate hexagon vertices based on the intersection points
    hexagon_size = 100  # Adjust this based on your hexagon size
    hexagons = []
    for x, y in intersection_points:
        for i in range(6):
            angle = i * np.pi/3
            x_i = int(x + hexagon_size * np.cos(angle))
            y_i = int(y + hexagon_size * np.sin(angle))
            hexagons.append((x_i, y_i))

    # Ensure hexagon is in the correct format
    hexagons = [hexagons]  # Wrap the hexagons in a list
    hexagons = np.array(hexagons, dtype=np.int32)  # Convert to int32 data type
    hexagons = hexagons.reshape((-1, 1, 2))  # Reshape to (n, 1, 2)

    # Draw the reconstructed hexagons
    cv2.polylines(image, hexagons, isClosed=True, color=(0, 255, 0), thickness=2)

    # Save or display the image
    cv2.imwrite('output_image.jpg', image)
    cv2.imshow('Reconstructed Hexagons', image)
    gridFromBorders(image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def gridFromBorders(image):

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection (e.g., Canny)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Find contours to detect the outer border
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the contour with the largest area as the outer border
    largest_contour = max(contours, key=cv2.contourArea)

    # Calculate the parameters of the outer border
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Calculate the side length of a regular hexagon
    side_length = min(w, h) / (2 * np.sqrt(3))  # Assuming regular hexagons

    # Calculate the number of rows and columns of hexagons
    hexagon_width = side_length * np.sqrt(3)
    hexagon_height = 2 * side_length
    num_columns = int(w / hexagon_width)
    num_rows = int(h / hexagon_height)

    # Generate hexagons in a grid pattern
    hexagons = []
    for row in range(num_rows):
        for col in range(num_columns):
            x_i = x + col * hexagon_width
            y_i = y + row * hexagon_height
            if col % 2 == 1:
                y_i += hexagon_height / 2
            hexagon = []
            for i in range(6):
                angle = i * np.pi / 3
                x_coord = int(x_i + side_length * np.cos(angle))
                y_coord = int(y_i + side_length * np.sin(angle))
                hexagon.append((x_coord, y_coord))
            hexagons.append(hexagon)

    # Draw the hexagons
    for hexagon in hexagons:
        cv2.polylines(image, [np.array(hexagon, np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)

    # Save or display the image with drawn hexagons
    cv2.imwrite('output_image.jpg', image)
    cv2.imshow('Image with Hexagons', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
