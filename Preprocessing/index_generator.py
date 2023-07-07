#from multiprocessing import Process, Lock
#import threading
import sys
import os
from partial_indexer import *
from file_operations import *


# Generate All Partial Indexes
#====================================================================================================
def full_index_generator(path):
    #define number of processes
    dumps = 10

    #create a list of all directories
    dir_list = os.listdir(path)

    #allpaths = [ (doc_id,path) ]
    allpaths = get_all_paths(path)
    
    #set to store simhashes
    simhashes = set()

    #file to map document id to url 
    thread_doc_file = open(f"thread_indexes/Documents/documents.txt", 'a')
    filemap = alphabet_indexes()

    #run processs to create indexes
    startindex = 0
    increment = len(allpaths)//dumps
    endindex = len(allpaths)//dumps
    for process_number in range(dumps):
        process_urls = allpaths[startindex:endindex]
        create_partial_index(process_urls,process_number,thread_doc_file,filemap,simhashes)
        startindex = endindex
        endindex = endindex + increment    

    #run process to handle remaining files
    startindex = len(allpaths)-(len(allpaths)%dumps)
    process_urls = allpaths[startindex:]
    create_partial_index(process_urls,dumps,thread_doc_file,filemap,simhashes)

    thread_doc_file.close()



# Run
#====================================================================================================
#set the developer folder as path
path = os.getcwd() + "/developer/DEV"
full_index_generator(path)