import cv2
import numpy as np
import random

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

    # Create canvases for pointy-top and flat-top hexagons with random colors
    pointy_top_image = np.zeros_like(image)
    flat_top_image = np.zeros_like(image)

    # Loop through all the contours
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        M = cv2.moments(contour)

        # Check if the polygon has 6 sides and is within the area range
        if len(approx) == expected_sides and min_area < cv2.contourArea(approx) < max_area:
            hexagon_count += 1
            hexagon_size = cv2.contourArea(approx)

            # Determine orientation by checking the y-coordinate of the top point
            top_point = tuple(approx[approx[:, :, 1].argmin()][0])
            reference_point = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']) - int(np.sqrt(hexagon_size / (3 * np.sqrt(3)))))

            if top_point[1] > reference_point[1]:
                pointyTopCounter += 1
                # Draw the pointy-top hexagon in a random color
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                cv2.drawContours(pointy_top_image, [contour], -1, color, thickness=cv2.FILLED)
                # Mark the top point with a black dot on the pointy top canvas
                if M['m00'] != 0:
                    center_x = int(M['m10'] / M['m00'])
                    center_y = int(M['m01'] / M['m00'])
                    center = (center_x, center_y)
                    cv2.circle(pointy_top_image, center, 5, (0, 0, 255), -1)  # Draw a red dot at the center
                    cv2.circle(pointy_top_image, top_point, 5, (0, 255, 0), -1)
                    cv2.circle(pointy_top_image, reference_point, 5, (255, 255, 255), -1)

            else:
                flatTopCounter += 1
                # Draw the flat-top hexagon in a random color
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                cv2.drawContours(flat_top_image, [contour], -1, color, thickness=cv2.FILLED)
                # Mark the top point with a black dot on the flat top canvas
                cv2.circle(flat_top_image, top_point, 5, (0, 255, 0), -1)
                if M['m00'] != 0:
                    center_x = int(M['m10'] / M['m00'])
                    center_y = int(M['m01'] / M['m00'])
                    center = (center_x, center_y)
                    cv2.circle(flat_top_image, center, 5, (0, 0, 255), -1)  # Draw a red dot at the center
                    cv2.circle(flat_top_image, reference_point, 5, (255, 255, 255), -1)

    print("TOP: ", pointyTopCounter)
    print("FLAT: ", flatTopCounter)

    if pointyTopCounter > flatTopCounter:
        hexagon_orientation = 'pointy'

    radius = np.sqrt(hexagon_size / (3 * np.sqrt(3)))

    print(f"Number of hexagons: {hexagon_count}")
    print(f"Size of hexagons: {hexagon_size}")
    print(f"Radius of hexagons: {radius}")
    print(f"Orientation: {hexagon_orientation}")

    # Display the canvases with different colors for different hexagons
    cv2.imshow("Pointy Top Hexagons", pointy_top_image)
    cv2.imshow("Flat Top Hexagons", flat_top_image)
    cv2.imshow("Original Image", image)
    ####
    return (hexagon_count, radius, hexagon_orientation)
    ####

