import math 



# tf-idf Calculator
#---------------------------------------------------------------------
def tfidf(word,posting_list):
    #posting_list = [[doc_id, [postitions], bias],]

    #compute idf
    idf = math.log(55393/(len(posting_list)+1)) #count the query as a doc by adding 1

    #compute tf-idf for each document
    for i in range(len(posting_list)):
        doc_id = posting_list[i][0]
        tf = posting_list[i][1]
        tf = 1 + math.log(tf)
        tf_idf = tf*idf
        bias = posting_list[i][2]

        posting_list[i].append(round(tf_idf,4)) #[[doc_id, [postitions], bias, tf-idf],]

