from nltk.stem import PorterStemmer



# Porter Stemmer Tokenizer
#---------------------------------------------------------------------
def tokenize(long_string) -> [str]:
    """
    Description:
    Helper function used to tokenize a string of text.

    Parameters:
    long_string - long text string from url content
    """
    ps = PorterStemmer()
    tokens = []
    alphanumeric = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    token = ""
    for char in long_string:
        #append token to token list and reset token if nonalphanumeric character is found
        if char not in alphanumeric:
            if token != "":
                if len(token) > 1:
                    tokens.append(ps.stem(token.lower()))
                token = ""
        #append character to token
        else: 
            token = token + char
    if token != "" and len(token) > 1:
        tokens.append(ps.stem(token.lower()))
    #return token list
    return tokens