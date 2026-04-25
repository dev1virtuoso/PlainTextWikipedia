import os
from concurrent.futures import ProcessPoolExecutor
from dewiki_functions import *

wiki_xml_file = '/Users/carsonwu/Developer/Own/code/kg_chatbot/20260421/enwiki-latest-pages-articles.xml'
json_save_dir = '/Users/carsonwu/Developer/Own/code/kg_chatbot/20260421/json/'

os.makedirs(json_save_dir, exist_ok=True)

def process_file_multiprocessing(filename, savedir):
    article = ''
    with ProcessPoolExecutor() as executor:
        with open(filename, 'r', encoding='utf-8') as infile:
            for line in infile:
                if '<page>' in line:
                    article = ''
                elif '</page>' in line:
                    executor.submit(save_article, article, savedir)
                else:
                    article += line

if __name__ == '__main__':
    process_file_multiprocessing(wiki_xml_file, json_save_dir)
