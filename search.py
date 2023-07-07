from collections import defaultdict
from typing import TextIO, List, Tuple, Any



def search_word(open_file: TextIO, word: str, index_of_index: dict) -> list:
    """ Given an open file of the full index, the word to be searched for, and the index of indexes
        dictionary, return the postings list of that word"""
    #print(f"Searching for word: {word} ... ")
    if word not in index_of_index:
        return []
    start, buffer = index_of_index[word]
    open_file.seek(start)
    line = open_file.read(buffer)
    word, postings_list = line.split(" : ")
    return [[int(number.strip()) if i<2 else float(number.strip()) for number, i in zip(per_doc.strip().split(","), range(4))] for per_doc in postings_list.strip()[2:-2].split("], [")]


def search_words(open_file: TextIO, words: list, index_of_index: dict) -> dict:
    words_postings = {}
    for word in words:
        words_postings[word] = search_word(open_file, word, index_of_index)
    return words_postings


