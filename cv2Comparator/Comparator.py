import os
import cv2

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    return image

import numpy as np

def calculate_color_similarity(image1, image2):
    # Resize images to a fixed size
    resized_image1 = cv2.resize(image1, (100, 100))  # Adjust the size as needed
    resized_image2 = cv2.resize(image2, (100, 100))  # Adjust the size as needed

    # Convert images to LAB color space
    image1_lab = cv2.cvtColor(resized_image1, cv2.COLOR_BGR2LAB)
    image2_lab = cv2.cvtColor(resized_image2, cv2.COLOR_BGR2LAB)

    # Compute the absolute difference between the LAB images
    diff = np.abs(image1_lab.astype(np.float32) - image2_lab.astype(np.float32))

    # Compute the average pixel-wise absolute difference
    avg_diff = np.mean(diff)

    # Scale the average difference to get a similarity score
    max_diff = 100  # Adjust this based on the expected range of differences
    similarity = 1 - (avg_diff / max_diff)

    return max(0, similarity)  # Ensure similarity is non-negative


def calculate_contour_similarity(image1, image2):
    # Resize images to a fixed size
    resized_image1 = cv2.resize(image1, (100, 100))  # Adjust the size as needed
    resized_image2 = cv2.resize(image2, (100, 100))  # Adjust the size as needed

    # Convert resized images to grayscale
    image1_gray = cv2.cvtColor(resized_image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(resized_image2, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference between the grayscale images
    difference = cv2.absdiff(image1_gray, image2_gray)

    # Calculate percentage of pixels that are different
    num_different_pixels = cv2.countNonZero(difference)
    total_pixels = difference.size
    similarity = 1 - (num_different_pixels / total_pixels)
    return similarity

def compare_with_database(database_folder, given_image):
    # Preprocess given image
    given_hexagon = preprocess_image(given_image)

    # Initialize lists to store similarities for all images
    color_similarities = []
    contour_similarities = []

    # Iterate through subfolders in the database folder
    for subdir, _, files in os.walk(database_folder):
        for file in files:
            # Preprocess database image
            db_image_path = os.path.join(subdir, file)
            db_hexagon = preprocess_image(db_image_path)

            # Calculate color and contour similarity
            color_similarity = calculate_color_similarity(given_hexagon, db_hexagon)
            contour_similarity = calculate_contour_similarity(given_hexagon, db_hexagon)

            # Append similarities to the lists
            color_similarities.append((db_image_path, color_similarity))
            contour_similarities.append((db_image_path, contour_similarity))

    # Sort the lists based on similarity
    color_similarities.sort(key=lambda x: x[1], reverse=True)
    contour_similarities.sort(key=lambda x: x[1], reverse=True)

    # Get the top 5 matches for each parameter
    top_color_matches = color_similarities[:5]
    top_contour_matches = contour_similarities[:5]

    return top_color_matches, top_contour_matches

def calculate_weighted_average(matches):
    total_similarity = 0
    total_weight = 0
    for match, similarity in matches:
        # Assigning weights to similarities (adjust as needed)
        weight = 1.0  # Equal weight for now
        total_similarity += similarity * weight
        total_weight += weight
    return total_similarity / total_weight if total_weight != 0 else 0

def find_best_guess(top_color_matches, top_contour_matches):
    # Extract folder names from the paths of the top matches
    color_folder_names = [os.path.basename(os.path.dirname(match[0])) for match in top_color_matches]
    contour_folder_names = [os.path.basename(os.path.dirname(match[0])) for match in top_contour_matches]

    # Get the folder names with the highest similarity for both color and contour
    best_color_guess = max(set(color_folder_names), key=color_folder_names.count)
    best_contour_guess = max(set(contour_folder_names), key=contour_folder_names.count)

    # Determine the best guess based on the folder with the highest similarity in both color and contour
    if best_color_guess == best_contour_guess:
        return f"Best guess: {best_color_guess}"
    else:
        # If there's a discrepancy, return both the best matches for both parameters
        return f"Best color match: {best_color_guess}, Best contour match: {best_contour_guess}"


if __name__ == "__main__":
    database_folder = "C:/Users/acvcl/Documents/GitHub/AtlasOfMystara/CNN/Dataset"
    given_image = r"C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\CNN\Dataset\border\border_c7ba9edc62a840f0beccc0bd6b0e498c.png"
    top_color_matches, top_contour_matches = compare_with_database(database_folder, given_image)

    print("Top 5 color matches:")
    for match in top_color_matches:
        print("{} color similarity: {:.2f}%".format(match[0], match[1] * 100))

    print("\nTop 5 contour matches:")
    for match in top_contour_matches:
        print("{} contour similarity: {:.2f}%".format(match[0], match[1] * 100))

    # Find the best guess
    best_guess = find_best_guess(top_color_matches, top_contour_matches)
    print("\n" + best_guess)