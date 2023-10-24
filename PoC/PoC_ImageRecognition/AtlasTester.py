# combined_script.py
import os
import subprocess
import argparse
from PIL import Image  # You may need to install the Pillow library


def list_image_files(folder_path):
    image_files = []
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif')  # Add more extensions if needed

    # dirs is not used as we are assuming no subfolders
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(valid_extensions):
                image_files.append(os.path.join(root, file))
    return image_files

def get_valid_folder_path():
    while True:
        folder_path = input("Enter the folder path: ")
        if os.path.isdir(folder_path):
            return folder_path
        else:
            print("Invalid folder path. Please provide a valid folder path.")


def main():
    parser = argparse.ArgumentParser(description='Image Processing for Multiple Images')
    parser.add_argument('folder_path', nargs='?', help='Path to the folder containing images')

    args = parser.parse_args()
    folder_path = args.folder_path

    if folder_path is None:
        folder_path = get_valid_folder_path()

    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please provide a valid folder path.")
    else:
        image_files = list_image_files(folder_path)
        if not image_files:
            print("No image files found in the specified folder.")
        else:
            for image_file in image_files:
                subprocess.run(['python', PROGRAMTORUN, image_file])

if __name__ == "__main__":
    AtlasTester = r"C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\PoC\PoC_code\AtlasOfMystaraMain.py"
    BitmapToHex = r"C:\Users\acvcl\Documents\GitHub\AtlasOfMystara\PoC\PoC_code\PoCBitmapToHex.py"
    PROGRAMTORUN = r"PoC\PoC_code\PoCBitmapToHex.py"
    main()
