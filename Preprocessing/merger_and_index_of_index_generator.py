import os
from collections import defaultdict
from file_operations import *
from tfidf import *



# Merges All Partial Indexes
#---------------------------------------------------------------------
def get_all_paths(path: str) -> list:
    dir_list = os.listdir(path)
    file_paths = [path + "/" + d for d in dir_list]
    return file_paths


def merge(path,index_of_index):
    print(f"Merging {path}")
    partial_index_dict = defaultdict(list)
    with open(path, 'r') as index:
        for line in index.readlines():
            line = line.strip()
            [word,posting_list] = line.split(" : ")
            partial_index_dict[word] += [[int(number.strip()) if i<2 else float(number.strip()) for number, i in zip(per_doc.strip().split(","), range(3))] for per_doc in posting_list[2:-2].split("], [")]
    
    with open("../full_index.txt", "a") as f:
        for k in partial_index_dict.keys():
            partial_index_dict[k] = sorted(sorted(partial_index_dict[k], key=lambda x:-x[2]), key=lambda k:-k[1])

        for k,v in partial_index_dict.items():
            #append the tfidf to all postings in v
            tfidf(k,v)

            string = f"{k} : {v}"

            start_position = f.tell()
            end_position = len(string) + 1

            index_of_index[k] = [start_position,end_position]

            f.write(f'{string}\n')


def main():
    index_of_index = dict()
    path = "thread_indexes/Partial_Indexes"
    all_paths = get_all_paths(path)
    for path in all_paths:
        merge(path,index_of_index)

    with open("../index_of_index.txt", "a") as f:
        for k,v in index_of_index.items():
            f.write(f'{k} : {v}\n')



if __name__ == "__main__":
    main()

    