import requests
from bs4 import BeautifulSoup
import os

# Function to download plain text from a webpage
def download_page_text(url, save_dir):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        # Extract the plain text (without HTML tags)
        text = ""
        for par in paragraphs:
            text += par.get_text()
            text += "\n"

        # Save the plain text to a file
        page_name = os.path.basename(url) + ".txt"
        with open(os.path.join(save_dir, page_name), 'w', encoding='utf-8') as file:
            file.write(url+"\n")
            file.write(text)
            file.close()

        print(f"Downloaded: {url}")

    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Function to crawl a website and follow links to subpages
def crawl_website(base_url, depth, save_dir):
    if depth == 0:
        return

    try:
        # Send an HTTP GET request to the base URL
        response = requests.get(base_url)
        response.raise_for_status()

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the links on the page
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')

            # Check if it's an absolute URL
            if href.startswith('http'):
                download_page_text(href, save_dir)
                crawl_website(href, depth - 1, save_dir)

            # Check if it's a relative URL
            elif href.startswith('/'):
                full_url = base_url + href
                download_page_text(full_url, save_dir)
                crawl_website(full_url, depth - 1, save_dir)

    except Exception as e:
        print(f"Error crawling {base_url}: {e}")

if __name__ == "__main__":
    base_url = "https://space.com"  # Replace with the URL of the website you want to crawl
    save_directory = "downloaded_pages"  # Directory to save downloaded pages
    max_depth = 3  # Maximum depth to crawl

    # Create the save directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Start crawling
    crawl_website(base_url, max_depth, save_directory)
