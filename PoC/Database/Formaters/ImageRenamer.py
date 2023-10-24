import os

def rename_images(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please provide a valid folder path.")
        return

    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')  # Add more extensions if needed
    image_count = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_count += 1
                image_extension = os.path.splitext(file)[1]
                new_name = f"Medium{image_count}{image_extension}"
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")
            if file.lower().endswith(".webp"):
                image_count += 1
                image_extension = ".png"
                new_name = f"Easy{image_count}{image_extension}"
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    rename_images(folder_path)
