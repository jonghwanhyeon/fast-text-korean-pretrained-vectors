import logging
import re
import json
import unicodedata

from multiprocessing import Pool
from tqdm import tqdm
from namuwiki.extractor import extract_text

namu_wiki_dump_filename = 'namuwiki_20170327.json'
output_filename = 'namuwiki_20170327_dataset'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parent_document_pattern = re.compile(r'^상위 *문서[ \t]*\:.+')
special_character_pattern = re.compile(r'[\`\~\!\@\#\$\%\^\&\*\(\)\_\|\+\-\=\?\;\:\'\"\,\.\<\>\{\}\[\]\\\/]')
whitespace_pattern = re.compile(r'\s+')

def work(document):
    text = extract_text(document['text'])

    text = parent_document_pattern.sub('', text).strip()
    text = special_character_pattern.sub(' ', text)

    text = whitespace_pattern.sub(' ', text)
    text = text.strip()

    return {
        'title': document['title'],
        'text': text
    }

logger.info('Reading file...')
with open(namu_wiki_dump_filename, 'r', encoding='utf-8') as input_file:
    namu_wiki = json.load(input_file)

documents = []
with Pool() as pool:
    logger.info('Processing...')
    with tqdm(total=len(namu_wiki)) as progress_bar:
        for document in pool.imap(work, namu_wiki):
            documents.append(document)

            progress_bar.update()

logger.info('Writing file...')
with open(output_filename, 'w', encoding='utf-8') as output_file:
    for document in tqdm(documents):
        decomposed_text = unicodedata.normalize('NFD', document['text'])
        print(decomposed_text, end=' ', file=output_file)
