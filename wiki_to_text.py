from dewiki_functions import *

wiki_xml_file = '/Users/carsonwu/Developer/Own/code/kg_chatbot/20260421/enwiki-latest-pages-articles.xml'
json_save_dir = '/Users/carsonwu/Developer/Own/code/kg_chatbot/20260421/json/'

if __name__ == '__main__':
    process_file_text(wiki_xml_file, json_save_dir)
