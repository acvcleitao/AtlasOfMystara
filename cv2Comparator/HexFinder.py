import cv2
import numpy as np
import math
from collections import Counter

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

def calculate_hexagon_size(centers):
    distances = []
    for i, center1 in enumerate(centers):
        for center2 in centers[i+1:]:
            distance = np.linalg.norm(np.array(center1) - np.array(center2))
            distances.append(distance)
    counter = Counter(distances)
    most_common_distance = counter.most_common(1)[0][0]
    margin = most_common_distance / 4
    valid_distances = [d for d in distances if abs(d - most_common_distance) <= margin]
    hexagon_size = np.mean(valid_distances)
    return hexagon_size

def draw_blue_lines(image, centers):
    blue_image = image.copy()
    for center in centers:
        cv2.circle(blue_image, center, 5, (255, 0, 0), -1)
    return blue_image

def draw_orange_boxes(image, centers, hexagon_size):
    orange_image = image.copy()
    for center in centers:
        x, y = center
        # Calculate the corner points of the bounding box
        x1 = int(x - hexagon_size / 2)
        y1 = int(y - hexagon_size / 2)
        x2 = int(x + hexagon_size / 2)
        y2 = int(y + hexagon_size / 2)
        # Draw the orange box
        cv2.rectangle(orange_image, (x1, y1), (x2, y2), (0, 165, 255), 2)
    return orange_image

def draw_green_centers(image, centers, hexagon_size):
    green_image = image.copy()
    margin = int(hexagon_size / 4)

    for center in centers:
        x, y = center
        
        # Propagate horizontally
        new_x = x + 2 * hexagon_size
        if not any(np.linalg.norm(np.array((new_x, y)) - np.array(c)) < margin for c in centers):
            cv2.circle(green_image, (int(new_x), y), 5, (0, 255, 0), -1)
        
        # Propagate vertically
        new_y = y + hexagon_size
        if not any(np.linalg.norm(np.array((x, new_y)) - np.array(c)) < margin for c in centers):
            cv2.circle(green_image, (x, int(new_y)), 5, (0, 255, 0), -1)

    return green_image

def main(image_path):
    image = cv2.imread(image_path)
    hexagon_centers = detect_hexagons(image)

    # Calculate hexagon size automatically
    hexagon_size = calculate_hexagon_size(hexagon_centers)

    # Draw blue lines at all detected hexagon centers
    blue_image = draw_blue_lines(image, hexagon_centers)

    # Draw orange boxes around each hexagon center
    orange_image = draw_orange_boxes(blue_image, hexagon_centers, hexagon_size)

    # Draw green circles around missing hexagon centers
    green_image = draw_green_centers(orange_image, hexagon_centers, hexagon_size)

    cv2.imshow('Grid of Hexagons with Inscribed Hexagons', green_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    main(image_path)
