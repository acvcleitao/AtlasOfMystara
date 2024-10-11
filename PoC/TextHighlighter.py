import cv2
import pytesseract
import re

# Set up the path to the Tesseract executable (if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
safe_words = ("i, of, to, in, it, is, be, as, at, so, we, he, by, or, on, do, if, me, my, up, an, go, no, us, am, 0,1,2,3,4,5,6,7,8,9,10,.")

def get_osd_orientation(image_path):
    # Load the image
    img = cv2.imread(image_path)
    
    # Detect the orientation of the image using OSD
    osd_data = pytesseract.image_to_osd(img)
    
    # Parse the OSD data to extract the rotation angle
    rotation_angle = int(re.search(r'(?<=Rotate: )\d+', osd_data).group(0))
    return rotation_angle

def rotate_image(image, angle):
    # Get the image dimensions
    (h, w) = image.shape[:2]
    
    # Calculate the center of the image
    center = (w // 2, h // 2)
    
    # Perform the rotation
    matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h))
    
    return rotated

def highlight_text_in_image(image_path, output_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    
    # Detect the orientation using OSD
    rotation_angle = get_osd_orientation(image_path)
    
    # If rotation is needed, rotate the image
    if rotation_angle != 0:
        img = rotate_image(img, rotation_angle)

    # Convert the image to RGB (pytesseract requires RGB format)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Use Tesseract to get the bounding boxes for each detected word
    data = pytesseract.image_to_data(rgb_img, output_type=pytesseract.Output.DICT)

    # Get image dimensions (needed to map coordinates correctly)
    h, w, _ = img.shape

    # Define a pattern to remove all non-alphabetic characters from the text
    clean_word_pattern = re.compile(r'[^A-Za-z0-9]')
    
    # Loop over each word and draw a rectangle around it
    for i in range(len(data['text'])):
        word = data['text'][i].strip()

        # Remove symbols and non-alphabetic characters from the word
        cleaned_word = clean_word_pattern.sub('', word)

        # Filter out empty words and words with less than 3 letters after cleaning
        if cleaned_word and (len(cleaned_word) >= 3 or cleaned_word.lower() in safe_words):
            x, y, w_box, h_box = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            
            # Draw the bounding box around the cleaned word
            cv2.rectangle(img, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)

    # Save the image with bounding boxes to a file
    cv2.imwrite(output_path, img)
    
    # Show the image with bounding boxes (optional)
    cv2.imshow("Text Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def print_detected_text(image_path):
    # Load the image
    img = cv2.imread(image_path)
    
    # Detect the orientation using OSD
    rotation_angle = get_osd_orientation(image_path)
    
    # Rotate the image if necessary
    if rotation_angle != 0:
        img = rotate_image(img, rotation_angle)
    
    # Use Tesseract to extract the detected text
    text = pytesseract.image_to_string(img)

    # Define a pattern to remove all non-alphabetic characters from the text
    clean_word_pattern = re.compile(r'[^A-Za-z0-9]')

    # Print each line of filtered text
    for line in text.splitlines():
        words = line.split()

        # Clean each word by removing symbols, and only print words with at least 3 letters
        filtered_words = [clean_word_pattern.sub('', word) for word in words if (len(clean_word_pattern.sub('', word)) >= 3 or word in safe_words)]
        
        if filtered_words:
            print(" ".join(filtered_words))

if __name__ == "__main__":
    image_path = r'C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\PoC\mystaros-karameikos-8-thorf.png'  # Replace with the path to your image
    output_path = r'C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\PoC\highlighted_text.png'  # Replace with the desired output path

    # Highlight text bounding boxes in the image and save it
    highlight_text_in_image(image_path, output_path)

    # Print the detected text one by one with filtering applied
    print_detected_text(image_path)
