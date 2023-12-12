import requests
from bs4 import BeautifulSoup

def get_maps_index(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send a request to the website with headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links with the title containing 'Rollover'
        map_links = soup.find_all('a', title=lambda value: value and 'Rollover' in value)

        # Check if any map links are found
        if map_links:
            # Create a list to store map details
            maps_list = []

            # Extract information from each link
            for map_link in map_links:
                title = map_link.get('title')
                # Add more fields as needed

                # Append map details to the list
                maps_list.append({
                    'Title': title,
                    # Add more fields as needed
                })

            return maps_list

        else:
            print("Error: No map links found.")
            return None

    else:
        print(f"Error: Unable to fetch the page. Status Code: {response.status_code}")
        return None

# Example usage
vault_of_pandius_url = "http://pandius.com/"
maps_index = get_maps_index(vault_of_pandius_url)

# Print the list of maps
if maps_index:
    for index, map_info in enumerate(maps_index, start=1):
        print(f"Map {index}: {map_info}")
