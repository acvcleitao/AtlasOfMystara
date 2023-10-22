import cv2
import numpy as np
your_min_area_threshold = 400

def HexTranslator(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detection to find edges in the image
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    hexagon_count = 0
    hexagon_size = 0
    hexagon_orientation = "flat"

    # Define the expected number of sides and minimum/maximum area of hexagons
    expected_sides = 6
    min_area = 500  # Adjust this threshold based on your specific image
    max_area = 50000  # Adjust this threshold based on your specific image
    pointyTopCounter = 0
    flatTopCounter = 0

    # Loop through all the contours
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the polygon has 6 sides and is within the area range
        if len(approx) == expected_sides and min_area < cv2.contourArea(approx) < max_area:
            hexagon_count += 1
            hexagon_size = cv2.contourArea(approx)

            # Determine orientation by checking the y-coordinate of the top point
            top_point = tuple(approx[approx[:, :, 1].argmin()][0])
            if top_point[1] < image.shape[1] / 2:
                pointyTopCounter += 1
            else:
                flatTopCounter += 1

    print("TOP: ", pointyTopCounter)
    print("FLAT: ", flatTopCounter)

    if (pointyTopCounter > flatTopCounter):
        hexagon_orientation = 'pointy'

    radius = np.sqrt(hexagon_size / (3 * np.sqrt(3)))

    print(f"Number of hexagons: {hexagon_count}")
    print(f"Size of hexagons: {hexagon_size}")
    print(f"Radius of hexagons: {radius}")
    print(f"Orientation: {hexagon_orientation}")

    cv2.imshow("Image", image)


def HexCounter(contours):
    # Count the hexagons among the contours
    hexagon_count = 0
    for contour in contours:
        if is_hexagon(contour):
            hexagon_count += 1

    print(f"Number of hexagons: {hexagon_count}")
    return

# Function to check if a contour is a hexagon
def is_hexagon(contour):
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    return len(approx) == 6 and cv2.contourArea(contour) > your_min_area_threshold