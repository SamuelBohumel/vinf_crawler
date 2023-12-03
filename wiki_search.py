import wikipediaapi
from bs4 import BeautifulSoup
import requests
import os
import xmltodict

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
# keyword_to_search = "nightmare"
# result = get_wikipedia_table_info(keyword_to_search)

# print(result)

occurrences = []
def find_all_occurrences_in_nested_dict(dictionary, target_word, current_path=[]):
    """
    Recursively search for all occurrences of a target word in a nested dictionary
    and return a list of tuples containing the value and the path of keys.

    Returns A list of tuples (value, path) for all occurrences of the target word.
    """

    for key, value in dictionary.items():
        path = current_path + [key]
        if isinstance(value, dict):
            occurrences.extend(find_all_occurrences_in_nested_dict(value, target_word, path))
        elif isinstance(value, str) and target_word.lower() in value.lower():
            occurrences.append((value, path))
    return occurrences

def get_wiki_from_dump():
    with open(os.path.join("results", "data", "wiki_dump.xml"), 'r', encoding='utf-8') as file:
        my_xml = file.read()
        dictionary = xmltodict.parse(my_xml, encoding='utf-8', process_namespaces=False, namespace_separator=':') 
        print("Parsed")
        finds = find_all_occurrences_in_nested_dict(dictionary, "1955", [])
        print(finds)

get_wiki_from_dump()