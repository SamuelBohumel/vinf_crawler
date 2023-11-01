import requests
import os
import time 
import re
import logging
import shutil
import json
import sys

logging.basicConfig(
    format='%(asctime)s - %(message)s', 
    #filename="log.log",
    stream=sys.stdout,
    level=logging.INFO
    )



        
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

def parse_data():
    result_dir = os.path.join("results", "data")
    data_p = open(os.path.join(result_dir, "all_merged.txt"), "r", encoding="utf8")
    data = data_p.read()
    data = re.sub(r"<.*?>", "", data)
    
    #data = re.sub(r"</?[a-z]+>", "", data)
    dictionary = {}
    key = None
    data_p.seek(0)
    for line in data_p.readlines():
        if len(re.findall("----------", line)) == 2:
            title = line.replace("----------", "")
            key = title
            key = re.sub(r" |(\\n)|(.txt)","", key)
            dictionary[key] = ""
        elif key is not None:
            dictionary[key] += line

    
    with open(os.path.join("results", "data", "all_cleaned.json"), "w", encoding="utf8") as outfile: 
        json.dump(dictionary, outfile)
        outfile.close()

    # result = open(os.path.join("results", "data", "all_cleaned.txt"), "w", encoding="utf8")
    # result.write(data)
    




if __name__ == "__main__":

    start = time.time()
 
    # Create the save directory if it doesn't exist
    save_directory = os.path.join("results", "data")  # Directory to save downloaded pages
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)



    #process_files()

    #parse data
    parse_data()

    
    end = time.time()
    print(f"Duration: {(end-start)/60} minutes")

    
