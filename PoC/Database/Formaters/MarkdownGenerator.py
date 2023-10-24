import os

def generate_markdown_file(image_path):
    image_name = os.path.basename(image_path)
    image_format = image_name.split('.')[-1]

    md_content = f"---\ntitle: Image Information\n---\n\n"
    md_content += f"# Image Name: `{image_name}`\n\n"
    md_content += f"## Information\n\n"
    md_content += f"- **Image Format:** `{image_format}`\n\n"
    md_content += "## Difficulties\n\n"
    md_content += "Describe any difficulties related to this image here.\n\n"
    md_content += "## Considerations\n\n"
    md_content += "Mention any considerations or notes about this image.\n\n"
    md_content += "---\n"

    md_filename = os.path.splitext(image_path)[0] + ".md"
    
    with open(md_filename, 'w') as md_file:
        md_file.write(md_content)

def process_images(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please provide a valid folder path.")
        return

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Add more extensions if needed
                image_path = os.path.join(root, file)
                generate_markdown_file(image_path)

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")

    process_images(folder_path)
