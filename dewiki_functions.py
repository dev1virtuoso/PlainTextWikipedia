# https://www.reddit.com/r/wikipedia/comments/13it9xw/how_to_download_all_wikipedia_articles_in/

from threading import Thread
import json
import re
from html2text import html2text as htt
import wikitextparser as wtp
import unicodedata
import sys

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

def dewiki(text):
    text = wtp.parse(text).plain_text()
    text = htt(text)
    text = re.sub(r'{[^}]*}', '', text)
    text = text.replace('\\n',' ')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w+\s]', '', text)
    text = remove_accents(text)
    return text if isinstance(text, str) else text.decode('utf-8')


def analyze_chunk(text):
    try:
        if '<redirect title="' in text:
            return None
        if '(disambiguation)' in text:
            return None
        else:
            title = text.split('<title>')[1].split('</title>')[0]
            title = htt(title)
            if ':' in title:
                return None
        serial = text.split('<id>')[1].split('</id>')[0]
        content = text.split('</text')[0].split('<text')[1].split('>', maxsplit=1)[1]
        content = dewiki(content)
        return {'title': title.strip(), 'text': content.strip(), 'id': serial.strip()}
    except Exception as oops:
        print(oops)
        return None

def save_article(article, savedir, current_count, total_count):
    doc = analyze_chunk(article)
    if doc:
        sys.stdout.write(f"\rPROGRESS: {current_count}/{total_count} | SAVING: {doc['title'][:30]}...          ")
        sys.stdout.flush()
        
        filename = doc['id'] + '.json'
        with open(savedir + filename, 'w', encoding='utf-8') as outfile:
            json.dump(doc, outfile, sort_keys=True, indent=1, ensure_ascii=False)


def process_file_text(filename, savedir):
    article = ''
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            if '<page>' in line:
                article = ''
            elif '</page>' in line:
                Thread(target=save_article, args=(article, savedir)).start()
            else:
                article += line
