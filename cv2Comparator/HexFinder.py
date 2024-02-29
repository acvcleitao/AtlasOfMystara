import cv2
import numpy as np
import math

def detect_hexagons(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    hexagon_centers = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
        if len(approx) == 6:
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            hexagon_centers.append((cX, cY))

    return hexagon_centers

def draw_hexagon_centers(image, centers):
    center_image = image.copy()
    for center in centers:
        cv2.circle(center_image, center, 5, (0, 0, 255), -1)
    return center_image

def draw_approximate_lines(image, centers):
    # Sort centers by x-coordinate for vertical lines
    centers.sort(key=lambda center: center[0])

    # Draw vertical lines on the original image
    for center in centers:
        x, y = center
        cv2.line(image, (x, 0), (x, image.shape[0] - 1), (255, 0, 0), 2)

    # Sort centers by y-coordinate for horizontal lines
    centers.sort(key=lambda center: center[1])

    # Draw horizontal lines on the original image
    for center in centers:
        x, y = center
        cv2.line(image, (0, y), (image.shape[1] - 1, y), (255, 0, 0), 2)

    return image


def find_common_distance(centers):
    distances = []
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            dist = math.sqrt((centers[i][0] - centers[j][0]) ** 2 + (centers[i][1] - centers[j][1]) ** 2)
            distances.append(dist)
    return max(set(distances), key=distances.count)

def draw_remaining_lines(image, hex_centers, common_distance, hexagon_size):
    orange_image = image.copy()

    # Sort hexagon centers by x-coordinate for vertical lines
    hex_centers.sort(key=lambda center: center[0])

    # Start with the leftmost x-coordinate for vertical lines
    leftmost_x = hex_centers[0][0]

    # Start drawing vertical orange lines
    while leftmost_x < image.shape[1]:
        # Check if there's a blue line at the same position or within the tolerance
        blue_line_found = False
        for line in orange_image:
            if len(line) == 4:  # Ensure it's a line with four coordinates
                x1, y1, x2, y2 = line
                if x1 == x2 and abs(x1 - leftmost_x) <= hexagon_size / 2:
                    blue_line_found = True
                    break

        if not blue_line_found:
            # Draw the orange line
            cv2.line(orange_image, (leftmost_x, 0), (leftmost_x, image.shape[0] - 1), (0, 165, 255), 2)
        
        # Move to the next position
        leftmost_x += int(common_distance * math.sqrt(3) / 2)

    # Sort hexagon centers by y-coordinate for horizontal lines
    hex_centers.sort(key=lambda center: center[1])

    # Start with the topmost y-coordinate for horizontal lines
    topmost_y = hex_centers[0][1]

    # Start drawing horizontal orange lines
    while topmost_y < image.shape[0]:
        # Check if there's a blue line at the same position or within the tolerance
        blue_line_found = False
        for line in orange_image:
            if len(line) == 4:  # Ensure it's a line with four coordinates
                x1, y1, x2, y2 = line
                if y1 == y2 and abs(y1 - topmost_y) <= hexagon_size / 2:
                    blue_line_found = True
                    break

        if not blue_line_found:
            # Draw the orange line
            cv2.line(orange_image, (0, topmost_y), (image.shape[1] - 1, topmost_y), (0, 165, 255), 2)
        
        # Move to the next position
        topmost_y += int(common_distance)

    return orange_image


def main(image_path):
    image = cv2.imread(image_path)
    hexagon_centers = detect_hexagons(image)

    # Draw red dots at the centers of hexagons
    center_image = draw_hexagon_centers(image, hexagon_centers)

    # Draw approximate vertical and horizontal lines
    line_image = draw_approximate_lines(center_image, hexagon_centers)

    # Find the most common distance between two hexagon centers
    common_distance = find_common_distance(hexagon_centers)

    # Assuming the size of a hexagon's side is known
    hexagon_size = 10  # Replace this with the actual size

    # Draw remaining orange lines
    orange_image = draw_remaining_lines(line_image, hexagon_centers, common_distance, hexagon_size)

    cv2.imshow('Grid of Squares with Extended Lines', orange_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    main(image_path)
