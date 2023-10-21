import requests
import os
import time 
import re
import logging
import shutil
import sys

logging.basicConfig(
    format='%(asctime)s - %(message)s', 
    #filename="log.log",
    stream=sys.stdout,
    level=logging.INFO
    )



        
def process_files(article_dir, file_list):
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
        result_file_p.write(f'---------- {filename} ----------\n')

        for f in found:
            result_file_p.write(re.sub(r'<p>|</p>','', f))
            result_file_p.write('\n')
        
        logging.info(f"parsing file {filename}")
    result_file_p.close()

if __name__ == "__main__":

    start = time.time()
 
    # Create the save directory if it doesn't exist
    save_directory = os.path.join("results", "data")  # Directory to save downloaded pages
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    article_dir = os.path.join("results", "articles")
    file_list = os.listdir(article_dir)

    process_files(article_dir, file_list)
    
    end = time.time()
    print(f"Duration: {(end-start)/60} minutes")

    
