import os



# Maps Document ID to URL
#---------------------------------------------------------------------
def get_all_paths(path: str) -> list:
    dir_list = os.listdir(path)
    dir_list = sorted(dir_list)
    file_paths = [path + "/" + d for d in dir_list]
    return file_paths


def read_partial_document(path: str, index_dict: dict) -> dict:
    with open(path, "r") as f:
        for line in f.readlines():
            doc_id,url = line.strip().split(" : ")
            index_dict[doc_id] = url
    return index_dict


def get_URL_to_doc_id_map():
    path = "Preprocessing/thread_indexes/Documents"
    all_paths = get_all_paths(path)
    doc_id_to_url = dict()
    for f in all_paths:
        #print(f"Processing: {f}")
        read_partial_document(f, doc_id_to_url)
    return doc_id_to_url


def get_URL_from_doc_id(top_doc_ids,doc_id_to_url):
    urls = []
    for doc_id in top_doc_ids:
        urls.append(doc_id_to_url[str(doc_id)])
    return urls