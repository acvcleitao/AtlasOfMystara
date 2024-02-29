import cv2
import numpy as np

def find_grid(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    lines = []
    hexagons = []

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by their x and y coordinates to find the top-left one
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))

    # Loop over contours
    for contour in contours:
        # Get the bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)

        # Approximate grid lines
        lines.append([(x, y), (x + w, y)])  # Top horizontal line
        lines.append([(x, y + h), (x + w, y + h)])  # Bottom horizontal line
        lines.append([(x, y), (x, y + h)])  # Left vertical line
        lines.append([(x + w, y), (x + w, y + h)])  # Right vertical line

        # Store the top-left corner of the first identified square
        hexagons.append((x, y))

    return lines, hexagons

def find_most_common_spacing(lines):
    horizontal_distances = [line[1][1] - line[0][1] for line in lines if line[0][1] != line[1][1]]
    vertical_distances = [line[1][0] - line[0][0] for line in lines if line[0][0] != line[1][0]]

    most_common_horizontal_spacing = max(set(horizontal_distances), key=horizontal_distances.count)
    most_common_vertical_spacing = max(set(vertical_distances), key=vertical_distances.count)

    return most_common_horizontal_spacing, most_common_vertical_spacing

def draw_grid(image, lines):
    grid_image = image.copy()
    for line in lines:
        cv2.line(grid_image, line[0], line[1], (0, 255, 0), 2)
    return grid_image

def generate_perfect_grid(image, hexagons, lines, horizontal_spacing, vertical_spacing):
    grid_image = image.copy()
    rows = image.shape[0] // vertical_spacing
    cols = image.shape[1] // horizontal_spacing

    current_x, current_y = hexagons[0]

    for i in range(rows):
        for j in range(cols):
            # Check if the starting point of the current square is close enough to any perfect hexagon
            color = (0, 255, 0)
            for hexagon in hexagons:
                if abs(current_x - hexagon[0]) < 2 and abs(current_y - hexagon[1]) < 2:
                    current_x, current_y = hexagon
                    color = (0, 0, 255)
                    break

            cv2.rectangle(grid_image, (current_x, current_y), (current_x + horizontal_spacing, current_y + vertical_spacing), color, 2)
            current_x += horizontal_spacing

        current_x = hexagons[0][0]
        current_y += vertical_spacing

    return grid_image

def mark_start_point(image, start_point):
    marked_image = image.copy()
    cv2.circle(marked_image, start_point, 5, (0, 0, 255), -1)  # Draw a red dot at the start point
    return marked_image

def main(image_path):
    image = cv2.imread(image_path)
    lines, hexagons = find_grid(image)
    horizontal_spacing, vertical_spacing = find_most_common_spacing(lines)
    approx_grid_image = draw_grid(image, lines)
    perfect_grid_image = generate_perfect_grid(image, hexagons, lines, horizontal_spacing, vertical_spacing)

    # Mark the start point on both images
    marked_approx_grid_image = mark_start_point(approx_grid_image, hexagons[0])
    marked_perfect_grid_image = mark_start_point(perfect_grid_image, hexagons[0])

    concatenated_image = np.concatenate((marked_approx_grid_image, marked_perfect_grid_image), axis=1)

    cv2.imshow('Approximated Grid vs Perfect Grid', concatenated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    main(image_path)
