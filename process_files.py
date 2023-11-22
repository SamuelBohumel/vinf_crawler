import requests
import os
import time 
import re
import logging
import shutil
import json
import sys
from rake_nltk import Rake
import nltk
import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import Pillow
import wikipediaapi
from bs4 import BeautifulSoup
from time import sleep
# nltk.download('stopwords')
# nltk.download('punkt')

# logging.basicConfig(
#     format='%(asctime)s - %(message)s', 
#     #filename="log.log",
#     stream=sys.stdout,
#     level=logging.INFO
#     )

def check_words_in_sentence(words, sentence):
    correct = 0
    for word in words:
        if word in sentence:
            correct += 1
    if correct == len(words):
        return True
    return False




def find_best_match(search_term, dictionary):
    words = search_term.split(" ")
    if " " not in search_term:
        #try to find definiton:
        for key, value in dictionary.items():
            if search_term in key:
                article = value['text']
                sententes = article.split('.')
                for sent in sententes:
                    if f"{search_term} is " in sent:
                        return sent, article
    else:
        for key, value in dictionary.items():
            if search_term in key:
                article = value['text']
                sententes = article.split('.')
                for sent in sententes:
                    if check_words_in_sentence(words, sent):
                        return sent, article
        return "",""


def search_keywords(dictionary, search_var, result_text, result_article):
    search_term = search_var.get()
    result_text.delete(1.0, tk.END)  # Clear previous results

    result, article = find_best_match(search_term, dictionary)
    result_text.insert(tk.END, result)
    result_article.delete(1.0, tk.END)
    result_article.insert(tk.END, article)



def create_GUI(dictionary):
    offset = 0
    app = tk.Tk()
    app.title('Keyword Search App')

    # Set default window size
    app.geometry('800x600')

    # Load and resize your logo
    logo_image = Image.open('logo.png')  # Replace 'logo.png' with your image file
    quantif = 0.5
    logo_image = logo_image.resize((round(logo_image.width*quantif), 
                                    round(logo_image.height*quantif)), 
                                    Image.ANTIALIAS)  # Adjust the size as needed
    logo = ImageTk.PhotoImage(logo_image)

    # Create a label for the logo and use grid for centering
    logo_label = ttk.Label(app, image=logo)
    logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Create a frame to center the search elements
    frame = ttk.Frame(app)
    frame.grid(row=1, column=0, columnspan=2)

    logo_label = ttk.Label(app, image=logo, anchor='center')
    logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    search_label = ttk.Label(app, text='Enter search keyword:')
    search_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky='w')

    search_var = tk.StringVar()
    search_var.trace('w', lambda name, index, mode, sv=search_var: search_keywords(dictionary, search_var, result_text, result_article))
    search_entry = ttk.Entry(app, textvariable=search_var)
    search_entry.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

    search_button = ttk.Button(app, text='Next match', command=lambda: search_keywords(dictionary, search_var, result_text, result_article))
    search_button.grid(row=2, column=1, padx=(0, 10), pady=5, sticky='ew')

    result_text = tk.Text(app, wrap=tk.WORD, height=10, width=40)
    result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    source_article = ttk.Label(app, text='Source article', anchor='center')
    source_article.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
    result_article = tk.Text(app, wrap=tk.WORD, height=10, width=40)
    result_article.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    # Column and row weights to make widgets expand correctly
    app.columnconfigure(0, weight=1)
    app.rowconfigure(3, weight=1)

    app.mainloop()

 
def process_files():
    article_dir = os.path.join("results", "articles")
    file_list = os.listdir(article_dir)
    result_dir = os.path.join("results", "data")
    result_file_p = open(os.path.join(result_dir, "all_merged.txt"), "w", encoding="utf8")

    for filename in file_list:
        path = os.path.join(article_dir, filename)
        file_p = open(path, "r", encoding="utf8")
        try:
            data = file_p.read()
        except UnicodeDecodeError as error:
            logging.error(exc_info=True)
            continue
        file_p.close()
        found = re.findall(r'<p>.*?</p>', data, re.DOTALL)
        article_name = filename.strip(".txt")
        result_file_p.write(f'---------- {filename} ----------\n')

        for f in found:
            result_file_p.write(re.sub(r'<p>|</p>','', f))
            result_file_p.write('\n')
        
        logging.info(f"parsing file {filename}")
    result_file_p.close()

def get_wikipedia_table_info(keyword):
    # Create a Wikipedia API object
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='Samuel B', 
                                       language='en', 
                                       extract_format=wikipediaapi.ExtractFormat.HTML)

    # Fetch the page for the given keyword
    page_py = wiki_wiki.page(keyword)

    if not page_py.exists():
        return {"error": "Page not found"}
    
    page_url = page_py.fullurl
    content = requests.get(page_url).text

    # Get the content of the Wikipedia page
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')

    # Find the first table in the page (you may need to adjust this based on your needs)
    table = soup.find('table')

    if not table:
        return None

    # Extract information from the table
    table_info = {}
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all(['td', 'th'])
        values = [col.get_text(strip=True) for col in columns]
        if values:
            # Assuming the first column is the key and the second column is the value
            table_info[values[0]] = values[1].lower() if len(values) > 1 else ""

    return table_info

def parse_data():
    result_dir = os.path.join("results", "data")
    data_p = open(os.path.join(result_dir, "all_merged.txt"), "r", encoding="utf8")
    data = data_p.read()
    data = re.sub(r"<.*?>", "", data)

    all_key_words = []
    
    #data = re.sub(r"</?[a-z]+>", "", data)
    dictionary = {}
    key = None
    data_p.seek(0)
    for line in data_p.readlines():
        if len(re.findall("----------", line)) == 2:
            title = line.replace("----------", "")
            key = title
            key = re.sub(r" |(\\n)|(.txt)","", key)
            key = key.replace('\n', '')
            dictionary[key] = {
                "text": "",
                "keywords" :[]
            }
        elif key is not None:
            cleaned = re.sub(r"<.*?>", "", line)
            cleaned = re.sub('"', "'", cleaned)
            dictionary[key]['text'] += cleaned

    counter = 0
    dictionary['info'] = {}
    for key, value in dictionary.items():
        try:
            print(f"processing {counter}/{len(dictionary.items())}")
            counter += 1
            rake_nltk_var = Rake()
            rake_nltk_var.extract_keywords_from_text(value['text'])
            phrases = rake_nltk_var.get_ranked_phrases()
            keyword_extracted = []
            phrases = list(set(phrases))
            for word in phrases:
                match = re.search(word, value['text'], re.IGNORECASE)
                if match:
                    keyword_extracted.append(match.group())
            print(keyword_extracted)
            for keyword in list(set(keyword_extracted)):
                if re.search(r'[A-Z]+', keyword):
                    result = get_wikipedia_table_info(keyword)
                    if result is not None:
                        dictionary["info"][keyword] = result
                    sleep(0.01)
                else:
                    dictionary["info"][keyword] = "no data"
            all_key_words.extend(keyword_extracted)
        except:
            pass
    
    with open(os.path.join("results", "data", "all_cleaned.json"), "w", encoding="utf8") as outfile: 
        json.dump(dictionary, outfile)
        outfile.close()

    # result = open(os.path.join("results", "data", "all_cleaned.txt"), "w", encoding="utf8")
    # result.write(data)
    keyword_df = pd.DataFrame(all_key_words, columns=['keyword'])
    keyword_df = keyword_df.groupby('keyword').size().reset_index(name='count')
    keyword_df.sort_values(by='count', ascending=False, inplace=True)
    keyword_df.to_csv("keywords.csv", index=False)
    

if __name__ == "__main__":

    start = time.time()
 
    # Create the save directory if it doesn't exist
    save_directory = os.path.join("results", "data")  # Directory to save downloaded pages
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    #process_files()

    parse_data()

    file_p =  open(os.path.join("results", "data", "all_cleaned.json"), "r", encoding="utf8")
    dictionary = json.load(file_p)

    create_GUI(dictionary)
    
    end = time.time()
    print(f"Duration: {(end-start)/60} minutes")

    
