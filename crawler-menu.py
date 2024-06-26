import requests
from bs4 import BeautifulSoup
import re

# Define the URL
url = 'https://hearohio.com'

# Define headers to avoid 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Define the word to search for
search_word = 'mary'  # Replace 'mary' with the word you are looking for

# Function to count occurrences of the word in a given URL
def count_word_in_url(url, word):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            return len(re.findall(r'\b{}\b'.format(re.escape(word)), content, re.IGNORECASE))
        else:
            return 0
    except requests.RequestException:
        return 0

# Send a GET request with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the top menu (adjust the selector based on the actual HTML structure)
    top_menu = soup.find('nav')  # Adjust as necessary

    if top_menu:
        # Find all the links within the top menu
        links = top_menu.find_all('a')

        # Extract the href attributes and count word occurrences
        link_data = []
        for link in links:
            href = link.get('href')
            if href and href.startswith('http'):
                count = count_word_in_url(href, search_word)
                link_data.append((href, count))

        # Generate the HTML output
        html_content = '<html><head><title>Link Word Count</title></head><body>'
        html_content += '<h1>Link Word Count</h1>'
        html_content += '<ul>'
        for href, count in link_data:
            html_content += f'<li><a href="{href}">{href}</a>: {count} occurrences of "{search_word}"</li>'
        html_content += '</ul>'
        html_content += '</body></html>'

        # Write the HTML content to a file
        with open('link_word_count.html', 'w') as file:
            file.write(html_content)

        print("HTML file 'link_word_count.html' has been created successfully.")
    else:
        print("Top menu not found.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
