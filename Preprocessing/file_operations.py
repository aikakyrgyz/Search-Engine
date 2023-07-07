import os 



# Generates Alphanumeric txt Files 
#---------------------------------------------------------------------
def alphabet_indexes():
    alphanumeric = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    open_file_map = dict()
    for letter in alphanumeric:
        open_file_map[letter] = open(f"thread_indexes/Partial_Indexes/{letter}.txt","a")
    return open_file_map


# Append To Files
#---------------------------------------------------------------------
def write_file(content,filename):
    if not os.path.isfile(filename):
        create = open(filename, "w")
        create.close()
    with open(filename, 'a') as write_line_to_file:
        write_line_to_file.write(f'{content}\n')


# File Path Generator 
#---------------------------------------------------------------------
def get_all_paths(path):
    doc_id = 0
    dir_list = os.listdir(path)
    allpaths = []
    #list all the inner directories
    for DIR in dir_list:
        files = os.listdir(path + "/" + DIR) 
        #get all files
        for f in files:
            filepath = path + "/" + DIR + "/" + f 
            allpaths.append( (doc_id, filepath) )
            doc_id += 1
    return allpaths