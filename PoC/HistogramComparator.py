import cv2
import matplotlib.pyplot as plt
import numpy as np

def calculate_and_plot_histogram(image_path1, image_path2):
    # Load the images with alpha channel (transparency)
    img1 = cv2.imread(image_path1, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(image_path2, cv2.IMREAD_UNCHANGED)

    # Split the channels (B, G, R, A)
    if img1.shape[2] == 4:  # Check if the image has an alpha channel
        b1, g1, r1, a1 = cv2.split(img1)
    else:
        b1, g1, r1 = cv2.split(img1)
        a1 = None  # No transparency

    if img2.shape[2] == 4:
        b2, g2, r2, a2 = cv2.split(img2)
    else:
        b2, g2, r2 = cv2.split(img2)
        a2 = None

    # Convert the channels to RGB format for consistency
    img1_rgb = cv2.merge((r1, g1, b1))
    img2_rgb = cv2.merge((r2, g2, b2))

    # Create a figure to plot the histograms
    plt.figure(figsize=(15, 10))

    # Colors for each channel (Red, Green, Blue)
    colors = ('r', 'g', 'b')

    # Plot the histogram for Image 1, excluding transparent pixels if transparency exists
    plt.subplot(3, 1, 1)
    plt.title("Image 1 Histogram" if a1 is not None else "Image 1 Histogram")
    for i, color in enumerate(colors):
        if a1 is not None:
            # Mask to exclude transparent pixels
            hist_img1 = cv2.calcHist([img1_rgb], [i], mask=(a1 > 0).astype(np.uint8), histSize=[256], ranges=[0, 256])
        else:
            hist_img1 = cv2.calcHist([img1_rgb], [i], None, [256], [0, 256])
        plt.plot(hist_img1, color=color)
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")

    # Plot the histogram for Image 2, excluding transparent pixels if transparency exists
    plt.subplot(3, 1, 2)
    plt.title("Image 2 Histogram" if a2 is not None else "Image 2 Histogram")
    for i, color in enumerate(colors):
        if a2 is not None:
            hist_img2 = cv2.calcHist([img2_rgb], [i], mask=(a2 > 0).astype(np.uint8), histSize=[256], ranges=[0, 256])
        else:
            hist_img2 = cv2.calcHist([img2_rgb], [i], None, [256], [0, 256])
        plt.plot(hist_img2, color=color)
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")

    # Plot the raw difference between the histograms
    plt.subplot(3, 1, 3)
    plt.title("Histogram Difference (Image 1 - Image 2)")
    for i, color in enumerate(colors):
        if a1 is not None:
            hist_img1 = cv2.calcHist([img1_rgb], [i], mask=(a1 > 0).astype(np.uint8), histSize=[256], ranges=[0, 256])
        else:
            hist_img1 = cv2.calcHist([img1_rgb], [i], None, [256], [0, 256])

        if a2 is not None:
            hist_img2 = cv2.calcHist([img2_rgb], [i], mask=(a2 > 0).astype(np.uint8), histSize=[256], ranges=[0, 256])
        else:
            hist_img2 = cv2.calcHist([img2_rgb], [i], None, [256], [0, 256])

        # Compute the difference between histograms
        hist_diff = hist_img1 - hist_img2
        plt.plot(hist_diff, color=color, label=f'{color.upper()} Difference')
    
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Difference (Image 1 - Image 2)")
    plt.legend()

    # Adjust layout for readability
    plt.tight_layout()

    # Show the histograms
    plt.show()

if __name__ == "__main__":
    # Replace these paths with the actual paths to your images
    image_path1 = r"PoC\HexagonHistogram1.png"
    image_path2 = r"PoC\HexagonHistogram2.png"

    # Calculate and plot histograms for both images
    calculate_and_plot_histogram(image_path1, image_path2)
