import re
import requests
from bs4 import BeautifulSoup

def extract_and_format_maps(input_string, output):
    maps = input_string.split('Replica map of')
    count = 0
    for map_section in maps:
        print(map_section)
        count += 1
        title_end = map_section.find('from')
        title = map_section[:title_end].strip()
        
        source_start = map_section.find('by') + 2
        source_end = map_section.find('current as of')
        source = map_section[source_start:source_end].strip()
        
        output.write(f"Title: {title}\nSource: {source}\n\n")
    return count



# Updated URL
vault_of_pandius_url = "http://www.pandius.com/maps.html"

# Define headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# Send a request to the website with headers
response = requests.get(vault_of_pandius_url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("response OK")
else:
    print(f"Error: Unable to fetch the page. Status Code: {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links with href containing common image file extensions
image_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg']

map_links = soup.find_all('a', href=lambda x: x and any(format in x.lower() for format in image_formats))
problematic_link = next((link for link in map_links if "Returned Blackmoor with superimposed colored territories modified by" in link.get_text()), None)

myString = str(problematic_link)
i = myString.find("by")
# Check if "by" is found
if i != -1:
    # Insert "</a>" after the first occurrence of "by"
    modified_string = myString[:i + 2] + "</a>" + myString[i + 2:]
else:
    print("The word 'by' was not found in the string.")

# Find the desired part
soup2 = BeautifulSoup(modified_string, 'html.parser')
desired_part = soup2.find_all('a', href=lambda x: x and any(format in x.lower() for format in image_formats))
# Print the desired part

map_links = [link for link in map_links if "Returned Blackmoor with superimposed colored territories modified by" not in link.get_text()] + desired_part

counter = 0
# Specify the file path to which you want to write the output
output_file_path = "ValutsOfPandius.txt"

# Open the file in write mode
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Extract and print map information to the file
    for link in map_links:
        counter += 1
        title = link.get_text(strip=True)
        # print(str(counter) + " -> " + str(link))

        author = link.find_next('a', href=lambda x: 'authors.html' in x).get_text(strip=True)

        # Use find instead of find_next and check if the returned value is not None
        update_date_tag = link.find('a', href=lambda x: 'current' in x)

        # Check if update_date_tag is not None before accessing its text
        update_date = update_date_tag.get_text(strip=True) if update_date_tag else "N/A"

        output_file.write(f"Map Title: {title}\nAuthor: {author}\nUpdate Date: {update_date}\n\n")
        print(f"Map Title: {title}\nAuthor: {author}\nUpdate Date: {update_date}\n\n")

print(f"Found {counter} maps! Output written to {output_file_path}")

