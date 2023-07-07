import numpy as np
from hashlib import sha256
import os
from file_operations import write_file



# Custom Simhash
#---------------------------------------------------------------------
def simhash(tokens,number_bits):
    """
    Description:
    Function used to calcuate the simhash of a url based on the url's tokens.
    Uses sha256 hashing.

    Parameters:
    tokens - tokens collected from the text contained in the url's page
    number_bits - the number of bits desired for the hash
    """
    #map tokens to frequencies
    frequencies = dict()
    for token in tokens:
        if token not in frequencies:
            frequencies[token] = 1
        else:
            frequencies[token] += 1

    #hash each token
    hashes = dict()
    for token in frequencies:
        checksum = sha256(token.encode("utf-8")).hexdigest()
        hashes[token] = int(checksum,16)%(2**(number_bits-1))

    #create vector
    vector = np.zeros((1,number_bits))
    for h in hashes:
        f = frequencies[h]
        #subtract frequency where there are zeros
        vector -= f*np.array([1 for i in range(number_bits)])
        #add frequency where there are ones
        bits = np.array([int(i) for i in bin(hashes[h])[2:]])
        bits = np.pad(bits, [(number_bits-bits.size,0)], 'constant',constant_values=(1))
        vector += f*bits
        vector += f*bits

    #determine bitvector from numerical vector 
    bitvector = np.zeros((1,number_bits))
    bitvector[np.where(vector > 0)] = 1 #all postive numbers are 1

    #return binary string as an int to store
    return int("".join(['{:.0f}'.format(k) for k in bitvector[0]]),2)



# Content Similarity Checker
#---------------------------------------------------------------------
#helper functions to compute bitwise operations
def similar_bits(bits1,bits2,threshold,number_bits):
    different = (bits1^bits2)
    num_different_bits = sum([ 1 if b == '1' else 0 for b in bin(different)])
    #duplicate or near duplicate
    if (1-(num_different_bits/number_bits)) >= threshold:
        return True
    #unique
    return False


def isSimilar(simhashes,current_content_hash,number_bits,similarity_threshold):
    similar_content = False
    for compare_content_hash in simhashes:
        similar_content = similar_bits(current_content_hash,compare_content_hash,similarity_threshold,number_bits)
        if similar_content:
            break
    return similar_content