import requests
from bs4 import BeautifulSoup

def fetch_google_doc(url):
    """Fetches the content from the Google Doc URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_data(data):
    """Parses the HTML data into a list of (char, x, y) tuples."""
    soup = BeautifulSoup(data, 'html.parser')
    parsed_data = []
    
    # Assuming data is in a table format
    table = soup.find('table')
    if not table:
        raise ValueError("No table found in the document")

    rows = table.find_all('tr')
    
    # Skip the header row if it exists
    for row in rows:
        cells = row.find_all('td')
        if len(cells) != 3:
            continue  # Skip rows that do not have exactly 3 cells
        
        try:
            # Extract character Unicode, x-coordinate, and y-coordinate
            x = int(cells[0].get_text().strip())
            print(x)
            char = cells[1].get_text().strip() # Unicode in hexadecimal format
            print(char)
            y = int(cells[2].get_text().strip())
            print(y)
            parsed_data.append((x, char, y))
        except ValueError:
            # Handle any conversion errors
            continue

    return parsed_data

def create_grid(parsed_data):
    """Creates a grid from the parsed data."""
    # Determine the size of the grid
    max_x = max(data[0] for data in parsed_data) if parsed_data else 0
    max_y = max(data[2] for data in parsed_data) if parsed_data else 0
    print(max_x, max_y)
    
    # Initialize the grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # Place characters in the grid
    for x, char, y in parsed_data:
        grid[y][x] = char
    
    return grid

def print_grid(grid):
    """print the grid"""
    for row in range(len(grid)-1,-1,-1):
        print(''.join(grid[row]))

def main(url):
    """Main function to fetch, parse, and print the grid."""
    data = fetch_google_doc(url)
    parsed_data = parse_data(data)
    print(parsed_data)
    grid = create_grid(parsed_data)
    print(grid)
    print_grid(grid)

# url
url = 'https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub'
main(url)
