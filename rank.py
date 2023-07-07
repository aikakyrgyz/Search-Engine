import math
import numpy as np
from collections import defaultdict



# tf-idf Sum Ranker
#---------------------------------------------------------------------
def ranker(word_to_postings,tokenized_query):

    sum_dictionary = defaultdict(int)
    doc_bias = defaultdict(int)

    for docs in word_to_postings.values(): 
        for doc in docs: #doc = [[doc_id, f, bias, tf-idf],]
            sum_dictionary[doc[0]] += doc[3]
            doc_bias[doc[0]] += doc[2]


    sorted_doc_ids = sorted(sum_dictionary.keys(), key=lambda x:-sum_dictionary[x]*(doc_bias[x]))
    #sorted_doc_ids = sorted(sorted(sum_dictionary.keys(), key=lambda x:(-sum_dictionary[x]/len(sum_dictionary))*doc_bias[x]))
    #sorted_doc_ids = sorted(sorted(sum_dictionary.keys(), key=lambda x:-sum_dictionary[x]*doc_bias[x]), key=lambda x:-doc_bias[x])
    print(f"Total Number of documents found: {len(sorted_doc_ids)}")

    top_docs_word_to_postings = {key:[doc for doc in value if doc[0] in sorted_doc_ids[:150]] for key, value in word_to_postings.items()}
    #return the cosine similarity of the top documents
    return cos_similarity(top_docs_word_to_postings,tokenized_query)


# Cosine Similarity
#---------------------------------------------------------------------
def cos_similarity(word_to_postings,tokenized_query):

    query_vector = []
    all_docs = []
    for v in word_to_postings.values():
        all_docs += v
    document_vectors = {tupple[0]:[] for tupple in all_docs}

    for word in word_to_postings:
        tf = tokenized_query.count(word)
        tf = 1 + math.log(tf)
        #1 is added because the query is considered a document 
        idf = math.log(55393/(len(word_to_postings[word])+1))
        tf_idf = tf*idf
        query_vector.append(tf_idf)
        
        docs_with_query_word = [tupple[0] for tupple in word_to_postings[word]]
        for doc in document_vectors:
            if doc in docs_with_query_word:
                i = docs_with_query_word.index(doc)
                tf_idf = word_to_postings[word][i][3]
                document_vectors[doc].append(tf_idf)
            else:
                document_vectors[doc].append(0)
    
    doc_to_cos_sim = {}
    for doc_id,vector in document_vectors.items():
        a = np.array(query_vector)
        b = np.array(vector)
        cos_sim =  np.dot(a/np.sqrt(sum(a**2)),b/np.sqrt(sum(b**2)))
        doc_to_cos_sim[doc_id] = cos_sim

    sorted_doc_ids = sorted(doc_to_cos_sim.keys(), key=lambda x:-doc_to_cos_sim[x])
    return sorted_doc_ids
