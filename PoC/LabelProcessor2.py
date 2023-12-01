import cv2
import numpy as np
from PIL import Image
import pytesseract
import os
import re

# Set the path to the Tesseract executable (change this path according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_nearest_right_hexagon(contours, current_index, current_x, current_y, current_w, current_h):
    nearest_distance = float('inf')
    nearest_index = None

    for i, contour in enumerate(contours):
        if i != current_index:
            x, y, w, h = cv2.boundingRect(contour)

            # Check if the current contour is to the right of the current hexagon
            if x > current_x + current_w:
                distance = x - (current_x + current_w)

                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_index = i

    return nearest_index, nearest_distance

def clean_text_for_filename(text):
    # Replace invalid characters in the text for filename
    cleaned_text = text.replace(' ', '_').replace('\n', '_').replace('\r', '')
    cleaned_text = re.sub(r'[^a-zA-Z_]', '', cleaned_text)  # Remove non-alphabetic characters
    return cleaned_text

def ensure_directory(directory):
    # Ensure that the specified directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_hexagons_with_text(image_path, output_folder):
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
    unknown_counter = 0

    for i, contour in enumerate(contours):
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)  # Adjust the epsilon parameter

        if len(approx) == 6:
            x, y, w, h = cv2.boundingRect(approx)

            # Filter contours based on size
            if w * h > min_hexagon_size:
                hexagon_image = original_image[y:y+h, x:x+w]

                # Find the nearest hexagon to the right
                nearest_index, nearest_distance = find_nearest_right_hexagon(contours, i, x, y, w, h)

                # Determine the width for text detection
                text_area_width = int(nearest_distance) if nearest_index is not None else original_image.shape[1] - (x + w)

                # Find text to the right of the hexagon
                text_area = original_image[y:y+h, x+w:x+w+text_area_width]
                text = pytesseract.image_to_string(Image.fromarray(cv2.cvtColor(text_area, cv2.COLOR_BGR2RGB)))

                # Draw a rectangle around the hexagon
                cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Draw a rectangle around the text area
                cv2.rectangle(original_image, (x+w, y), (x+w+text_area_width, y+h), (0, 255, 0), 2)

                if not text:
                    # If no text is found, save hexagon as unknown with a number
                    unknown_counter += 1
                    text = f"unknown_{unknown_counter}"

                print(f"Hexagon {i + 1} detected at ({x}, {y}), width: {w}, height: {h}, Text: {text}")

                hexagon_data.append((hexagon_image, text))

    # Display the image with rectangles for debugging
    cv2.imshow('Rectangles', original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return hexagon_data

def save_hexagon_images_with_text(hexagon_data, output_folder):
    ensure_directory(output_folder)  # Ensure that the output folder exists

    for i, (hexagon_image, text) in enumerate(hexagon_data):
        rect_image = Image.fromarray(cv2.cvtColor(hexagon_image, cv2.COLOR_BGR2RGB))

        # Clean the text for use in the filename
        cleaned_text = clean_text_for_filename(text)

        # Save the hexagon image with the cleaned text as the filename
        filename = f"{cleaned_text}_hexagon.png"
        filepath = os.path.join(output_folder, filename)
        rect_image.save(filepath)
        print(f"Saved: {filename}")

# TODO: Make it recieve arguments
# args -> input file and output folder
# Maybe tesseract input?
if __name__ == "__main__":
    image_path = r"C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\data\DatasetSource\adamantyr-legend.png"
    output_folder = r'C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\PoC\ProcessedLabels'

    hexagon_data = extract_hexagons_with_text(image_path, output_folder)
    save_hexagon_images_with_text(hexagon_data, output_folder)
