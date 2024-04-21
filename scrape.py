import requests
from bs4 import BeautifulSoup

# URL of the website you want to scrape
url = 'https://sweet-tuna-safe.ngrok-free.app'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the entire text content of the webpage
    text_content = soup.get_text()

    # Print the text content
    print(text_content.strip())  # .strip() removes leading/trailing whitespace
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
