import os
import sys
from collections import defaultdict

from bs4 import BeautifulSoup
from urllib.parse import urldefrag
import lxml
import json

#from multiprocessing import Process, Lock
#import threading

from tokenizer import *
from simhash import *
from file_operations import *



# Partial Indexer (given to each process)
# ---------------------------------------------------------------------
def create_partial_index(paths, threadnumber, thread_doc_file, filemap, simhashes):

    stopwords = {'and', 'at', 'by', 'from', 'for', 'in', 'is', 'next', 'of', 'on', 'to', 'the', 'thi', 'up', 'with'}

    #Note: HTML defines six levels of headings. A heading element implies all the font changes, paragraph 
    #breaks before and after, and any white space necessary to render the heading. The heading elements 
    #are H1, H2, H3, H4, H5, and H6 with H1 being the highest (or most important) level and H6 the least.
    important_tags = {
        "title": 5,  #title of the webpage
        "strong": 0.20, #"strong importance"
        "b": 0.20,      #bold 
        "i": 0.10,      #italics
        "em": 0.10,     #emphasis
        "h1": 1,        #header level 1 (most important)
        "h2": 0.90,     #header level 2
        "h3": 0.80,     #header level 3
        "h4": 0.70,     #header level 4
        "h5": 0.60,     #header level 5
        "h6": 0.50}     #header level 6 (least important)
    #Note: increment by 1 for multiplication

    inverted_index = dict()

    for doc_id, filepath in paths:

        with open(filepath) as openfile:
            data = json.load(openfile)

        #print(f"Thread : {threadnumber} doc_id : {doc_id} filepath : {filepath}")

        url = data["url"]
        # defrag url
        # Note: if the url did have a fragment and is identical to another url
        # it would be caught by the content similarity check
        url = urldefrag(url).url
        content = data["content"]
        encoding = data["encoding"]
        soup = BeautifulSoup(content, "html.parser") 

        # Index Regular Text
        # -----------------------------------------------------------------------------------------
        tokens = tokenize(soup.get_text())
        
        #skip empty pages
        if len(tokens) == 0:
            continue

        #duplicate and near duplicate check
        number_bits = 64
        similarity_threshold = 0.9375
        current_content_hash = simhash(tokens,number_bits)
        similar_to_another_url = isSimilar(simhashes,current_content_hash,number_bits,similarity_threshold)
        simhashes.add(current_content_hash)

        if similar_to_another_url:
            continue

        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = [[doc_id, 1, 0]]
            else:
                found = False
                for i in range(len(inverted_index[token])):
                    d_id, f, b = inverted_index[token][i]
                    if d_id == doc_id:
                        found = True
                        inverted_index[token][i][1] += 1
                        break
                if not found:
                    inverted_index[token].append([doc_id, 1, 0])


        # Index Important Text
        # -----------------------------------------------------------------------------------------
        for tag in important_tags:
            for i in soup.find_all(tag):
                tag_tokens = tokenize(i.text)
                for token in tag_tokens:

                    if token not in stopwords:
                        if token not in inverted_index:
                            inverted_index[token] = [[doc_id, 1, important_tags[tag]]]
                        else:
                            found = False
                            for i in range(len(inverted_index[token])):
                                d_id, f, b = inverted_index[token][i]
                                if d_id == doc_id:
                                    found = True
                                    inverted_index[token][i][1] += 1
                                    inverted_index[token][i][2] += important_tags[tag]
                                    break
                            if not found:
                                inverted_index[token].append([doc_id, 1, important_tags[tag]])
    
        # map the document ID to the url
        string = f"{doc_id} : {url}" 
        thread_doc_file.write(f'{string}\n')
    
    # write words to index
    filemap = alphabet_indexes()
    for k in inverted_index:
        letter = k[0].upper()
        string = f"{k} : {inverted_index[k]}"
        filemap[letter].write(f'{string}\n')
    for letter,open_file in filemap.items():
        open_file.close()

    print(f"Thread {threadnumber} Complete")