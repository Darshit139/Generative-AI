import requests
from bs4 import BeautifulSoup

# URL of the web page to scrape
url = 'https://mudwtr.com/products/30-servings-tin'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Get the content of the response
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get the entire HTML content
    full_html = soup.prettify()

    # Save the HTML content to a text file
    with open('webstore_content.html', 'w', encoding='utf-8') as file:
        file.write(full_html)

    print("HTML content successfully extracted and saved to 'webstore_content.html'.")
else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")
