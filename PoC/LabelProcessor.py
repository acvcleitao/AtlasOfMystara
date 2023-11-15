import cv2
import numpy as np
from PIL import Image

import cv2
import numpy as np
from PIL import Image

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

    hexagon_data = []
    min_hexagon_size = 500  # Adjust this value based on the minimum size of your hexagons

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)  # Adjust the epsilon parameter

        if len(approx) == 6:
            x, y, w, h = cv2.boundingRect(approx)

            # Filter contours based on size
            if w * h > min_hexagon_size:
                hexagon_image = original_image[y:y+h, x:x+w]

                print(f"Hexagon detected at ({x}, {y}), width: {w}, height: {h}")

                hexagon_data.append(hexagon_image)

    # Display the image with contours for debugging
    cv2.drawContours(original_image, contours, -1, (0, 255, 0), 2)
    cv2.imshow('Contours', original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return hexagon_data


def find_and_save_black_parts(image_path, output_folder):
    original_image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Apply binary threshold to create a binary image
    _, binary_image = cv2.threshold(gray_image, 30, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Save images with padding for each contour with a blackish interior
    padding = 20  # Adjust this value based on the desired padding
    for i, contour in enumerate(contours):
        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # Adjust the area threshold based on your preference
        area_threshold = 500
        if area > area_threshold:
            x, y, w, h = cv2.boundingRect(contour)
            black_part_image = original_image[max(0, y - padding):min(y + h + padding, original_image.shape[0]),
                                               max(0, x - padding):min(x + w + padding, original_image.shape[1])]

            # Draw contours on the original image
            cv2.drawContours(original_image, [contour], -1, (0, 0, 255), 2)

            cv2.imwrite(f"{output_folder}/black_part_{i}.png", black_part_image)

    # Display the image with contours for debugging
    cv2.imshow('Contours on Black Parts', original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_hexagon_images(hexagon_data, output_folder):
    for i, hexagon_image in enumerate(hexagon_data):
        rect_image = Image.fromarray(cv2.cvtColor(hexagon_image, cv2.COLOR_BGR2RGB))
        rect_image.save(f"{output_folder}/hexagon_{i}.png")

if __name__ == "__main__":
    image_path = r"C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\data\DatasetSource\adamantyr-legend.png"
    output_folder = r'C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\PoC\ProcessedLabels'

    hexagon_data = extract_hexagons(image_path)
    save_hexagon_images(hexagon_data, output_folder)
    find_and_save_black_parts(image_path, output_folder)

