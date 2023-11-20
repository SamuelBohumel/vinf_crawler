import wikipediaapi
from bs4 import BeautifulSoup
import requests

def get_wikipedia_table_info(keyword):
    # Create a Wikipedia API object
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='Samuel B', 
                                       language='en', 
                                       extract_format=wikipediaapi.ExtractFormat.HTML)

    # Fetch the page for the given keyword
    page_py = wiki_wiki.page(keyword)

    if not page_py.exists():
        return None
    
    page_url = page_py.fullurl
    content = requests.get(page_url).text

    # Get the content of the Wikipedia page
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')

    # Find the first table in the page (you may need to adjust this based on your needs)
    table = soup.find('table')

    if not table:
        return {"error": "No table found on the page"}

    # Extract information from the table
    table_info = {}
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all(['td', 'th'])
        values = [col.get_text(strip=True) for col in columns]
        if values:
            # Assuming the first column is the key and the second column is the value
            table_info[values[0].lower()] = values[1].lower() if len(values) > 1 else ""

    return table_info

# Example usage
keyword_to_search = "future us"
result = get_wikipedia_table_info(keyword_to_search)

print(result)
