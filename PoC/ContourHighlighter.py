import cv2

def highlight_contours(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image.")
        return

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to get a binary image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original image
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)  # Green color for contours

    # Save the image with highlighted contours
    cv2.imwrite(output_path, image)
    print(f"Highlighted contours saved to {output_path}")

# Example usage
image_path = r"C:\Users\acvcl\Downloads\karameikos-6-1981-split\imageonline\21.png"
output_path = r'C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\PoC\output_image_with_contours.jpg'  # Path to save the output image
highlight_contours(image_path, output_path)
