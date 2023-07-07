from search import *
from Preprocessing.tokenizer import tokenize
from rank import *
import time
from threading import Thread
from ID_to_url_map_generator import *


# Map Generation Helper Functions 
#=====================================================================================================

# Index of Index
#---------------------------------------------------------------------
def get_index_of_index(filename):
    print("Loading index of index ...")
    index_of_index_dict = dict()
    with open(filename, "r") as index:
        for line in index.readlines():
            line = line.strip()
            [word,byte_tuple] = line.split(" : ")
            #print(line)
            index_of_index_dict[word] = [int(b.strip()) for b in byte_tuple[1:-1].split(",")]
    return index_of_index_dict


# Full Disk Index
#---------------------------------------------------------------------
def get_disk_index(filename):
    disk_index_file = open(filename,"r")
    return disk_index_file


# Flask Web UI
#=====================================================================================================

from flask import Flask,render_template,request
app = Flask(__name__)

index_of_index = {}
index = {}
URL_to_doc_id_map = {}


@app.route("/")
@app.route("/home")
def home():
    return render_template("googlekrone.html")

@app.route("/search",methods = ['POST', 'GET'])
def result():
    output = request.form.to_dict()
    query = output["searchbar"]

    total_start = time.time()

    tokenized_query = tokenize(query)
    stopwords = {'and', 'at', 'by', 'from', 'for', 'in', 'is', 'next', 'of', 'on', 'to', 'the', 'thi', 'up', 'with'}
    words = set(tokenized_query)
    remove_stopwords = set(tokenized_query) - stopwords

    if len(remove_stopwords)/len(words) >= 1/2:
        words = remove_stopwords

    start = time.time()
    word_to_postings = search_words(index, words, index_of_index)
    end = time.time()
    print(f"ELAPSED RETRIVAL TIME : {(end - start)*1000} ms")

    start = time.time()
    ranked_doc_ids = ranker(word_to_postings,tokenized_query)
    end = time.time()
    print(f"ELAPSED RANK TIME : {(end - start)*1000} ms")

    total_end = time.time()
    print(f"TOTAL TIME : {(total_end - total_start)*1000} ms")


    if 15 >= len(ranked_doc_ids):
        urls = get_URL_from_doc_id(ranked_doc_ids[:15],URL_to_doc_id_map)
    else:
        urls = get_URL_from_doc_id(ranked_doc_ids,URL_to_doc_id_map)

    return render_template(
        "googlekrone.html",
        query=query,
        search_results1= (urls[0] if len(urls) > 0 else None),
        search_results2= (urls[1] if len(urls) > 1 else None),
        search_results3= (urls[2] if len(urls) > 2 else None),
        search_results4= (urls[3] if len(urls) > 3 else None),
        search_results5= (urls[4] if len(urls) > 4 else None),

        search_results6= (urls[5] if len(urls) > 5 else None),
        search_results7= (urls[6] if len(urls) > 6 else None),
        search_results8= (urls[7] if len(urls) > 7 else None),
        search_results9= (urls[8] if len(urls) > 8 else None),
        search_results10= (urls[9] if len(urls) > 9 else None),

        search_results11= (urls[10] if len(urls) > 10 else None),
        search_results12= (urls[11] if len(urls) > 11 else None),
        search_results13= (urls[12] if len(urls) > 12 else None),
        search_results14= (urls[13] if len(urls) > 13 else None),
        search_results15= (urls[14] if len(urls) > 14 else None),
        )


if __name__ == "__main__":
    index_of_index = get_index_of_index("index_of_index.txt")
    index = get_disk_index("full_index.txt")
    URL_to_doc_id_map = get_URL_to_doc_id_map()

    app.run(debug=True,port=5000)
    #app.run(host="0.0.0.0",port=5000)

    index.close()