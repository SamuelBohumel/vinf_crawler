import requests
import os
import time 
import re
import logging
import shutil

logging.basicConfig(
    format='%(asctime)s - %(message)s', 
    filename="log.log",
    level=logging.INFO
    )


def get_links(save_directory, base_url):
    file_p = open(os.path.join(save_directory, "article_htmls.txt"), 'w', encoding='utf-8')

    response = requests.get(base_url).text
    
    results = re.findall(r'https:\/\/www\.space\.com\/archive\/[0-9]{4}\/[09]+', response)
    
    article_links = []
    for link in results:
        response = requests.get(link).text
        file_p.write(response)
        links = re.findall(r"<a\s+(?:[^>]*?\s+)?href=([\"'])(.*?)\1", response)
        for item in links:
            article_links.append(item[1])
    
    article_l = open(os.path.join(save_directory, "article_links.txt"), 'w', encoding='utf-8')
    article_links = list(set(article_links))
    for link in article_links:
        article_l.write(link)
        article_l.write("\n")
    article_l.close()
    file_p.close()


def get_all_articles(save_directory):
    
    links_p = open(os.path.join(save_directory, "article_links.txt"), 'r', encoding='utf-8')
    links = links_p.readlines()
    
    
    if not os.path.exists(os.path.join(save_directory, "articles")):
        os.makedirs(os.path.join(save_directory, "articles"))
    else:
        shutil.rmtree(os.path.join(save_directory, "articles"))
        os.makedirs(os.path.join(save_directory, "articles"))
    
    for link in links:
        link_name = link.strip("\n")
        logging.info(f"Downloading {link_name}")
        article_name = link_name.split('/')[-1]
        article_name = article_name.replace(".html", ".txt")
        
        try:
            file_p = open(os.path.join(save_directory, "articles", article_name), 'w', encoding='utf-8')
            response = requests.get(link_name)
            file_p.write(response.text)
            file_p.close()
        except Exception as e:
            logging.error(exc_info=True, msg="Error with file or something")
        



if __name__ == "__main__":

    start = time.time()
    base_url = "https://www.space.com/archive"  # Replace with the URL of the website you want to crawl
    save_directory = "results"  # Directory to save downloaded pages

    # Create the save directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    #get_links(save_directory, base_url)

    get_all_articles(save_directory)

    
    end = time.time()
    print(f"Duration: {(end-start)/60} minutes")

    
