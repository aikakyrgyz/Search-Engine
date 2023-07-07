_______________________________________________________________________________________________
Team Information:

Akyra Lee, akyral, akyral@uci.edu, 96121718
Cecheng Cao, cechengc, cechengc@uci.edu, 87871777
Aigerim Kubanychbek Kyzy, akubanyc, akubanyc@uci.edu, 70321299

_______________________________________________________________________________________________
Required Dependancies:

1) nltk
    Installation:
        pip install --user -U nltk
        python -m nltk.downloader popular

2) Flask
    Installation:
        pip install Flask

_______________________________________________________________________________________________
Instructions:


1) Generate Partial Indexes

index_generator.py will generate partial indexes used to create the full index including every 
file in the developer/DEV folder. We assumed that our script is kept the in same folder as 
developer/DEV and call our function using the given current directory with the relative path 
"developer/DEV" appended.

The directories thread_indexes/Documents and thread_indexes/Partial_Indexes must not be altered. 


Steps:
    1. Place "developer/DEV" in the "Preprocessing" directory
            NOTE: developer/DEV must have this exact path
    1. Navigate to the Preprocessing directory
    2. run python3 index_generator.py in terminal 
    3. Wait for script to finish


2) Merge Partial Indexes

merger_and_index_of_index_generator.py will merge all partial indexes previously generated
into the file full_index.txt and generate the index of the index in the file index_of_index.txt

Steps:
    1. Navigate to the Preprocessing directory
    2. run python3 merger_and_index_of_index_generator.py in terminal 
    3. Wait for script to finish


3) Run Web Server and Start Search Engine 

Our search engine has a web interface that must be generated and hosted through localhost.
server.py

Steps:
    1. run python3 server.py in terminal 
    2. open http://127.0.0.1:5000 in browser
    3. Enter queries though web interface search bar
