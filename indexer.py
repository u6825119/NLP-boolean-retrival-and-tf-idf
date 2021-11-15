import numpy as np
import glob
import os
import pickle
import nltk
from collections import defaultdict

from string_processing import *

def read_doc(file_path):
    """Read a document from a path, tokenize, process it and return
    the list of tokens.

    Args:
        file_path (str): path to document file

    Returns:
        list(str): list of processed tokens
    """
    data = open(file_path, "r", encoding='utf-8').read()
    toks = tokenize_text(data)
    toks = process_tokens(toks)
    return toks

def gov_list_docs(docs_path):
    """List the documents in the gov directory.
    Makes explicit use of the gov directory structure and is not
    a general solution for finding documents.

    Args:
        docs_path (str): path to the gov directory

    Returns:
        list(str): list of paths to the document 
    """
    path_list = []
    # get all directories in gov root folder
    dirs = glob.glob(os.path.join(docs_path, "*"))
    for d in dirs:
        # get all the files in each of the sub directories
        files = glob.glob(os.path.join(d, "*"))
        path_list.extend(files)
    return path_list

def make_doc_ids(path_list):
    """Assign unique doc_ids to documents.

    Args:
        path_list (list(str)): list of document paths 

    Returns:
        dict(str : int): dictionary of document paths to document ids
    """
    cur_docid = 0
    doc_ids = {}
    for p in path_list:
        # assign docid
        doc_ids[p] = cur_docid
        # increase docid
        cur_docid += 1
    return doc_ids

def get_token_list(path_list, doc_ids):
    """Read all the documents and get a list of all the tokens

    Args:
        path_list (list(str)): list of paths
        doc_ids (dict(str : int)): dictionary mapping a path to a doc_id

    Returns:
        list(tuple(str, int)): an asc sorted list of token, doc_id tuples
    """
    all_toks = []
    for path in path_list:
        doc_id = doc_ids[path]
        toks = read_doc(path)
        for tok in toks:
            all_toks.append((tok, doc_id))
    return sorted(all_toks)

def index_from_tokens(all_toks):
    """Construct an index from the sorted list of token, doc_id tuples.

    Args:
        all_toks (list(tuple(str, int))): an asc sorted list of (token, doc_id) tuples
            this is sorted first by token, then by doc_id

    Returns:
        tuple(dict(str: list(tuple(int, int))), dict(str : int)): a dictionary that maps tokens to
        list of doc_id, term frequency tuples. Also a dictionary that maps tokens to document 
        frequency.
    """
    index = {}
    doc_freq = {}
    
    num = 1  #accumulator of number of documents
    idx_num = []
    flag = False  #indicates if there is unregistered values
    for i in range(0, len(all_toks)-1): #loop through the entire tok list (~second last for comparison)
        
        if all_toks[i][0]== all_toks[i+1][0]: #same word (current& next)
            flag = True
            if all_toks[i]== all_toks[i+1]:  #same doc_id
                num +=1
            else:                           #different doc_id
                idx_num.append((all_toks[i][1], num)) #add to temporary list before next tok of same name but different doc_id
                num = 1    #reset 
        elif flag:         #same word as above but not yet registered (the first 'if' cannot be satisfied due to the next word)
            idx_num.append((all_toks[i][1], num)) #add to the temp list
            index[all_toks[i][0]]= idx_num # add temp list to index
            doc_freq[all_toks[i][0]]= len(idx_num) #add to doc_freq by counting
            idx_num = [] #clear temp list for next word
            flag = False
            num = 1
            if i == len(all_toks)-2: #add last element if its the end of loop
                idx_num.append((all_toks[-1][1], num))
                index[all_toks[-1][0]]= idx_num
                doc_freq[all_toks[-1][0]]= len(idx_num)
        else: #append single valued terms
            idx_num.append((all_toks[i][1], num))
            index[all_toks[i][0]]= idx_num
            doc_freq[all_toks[i][0]]= len(idx_num)
            idx_num = []
            if i == len(all_toks)-2: #end of loop
                idx_num.append((all_toks[-1][1], num))
                index[all_toks[-1][0]]= idx_num
                doc_freq[all_toks[-1][0]]= len(idx_num)
                
    if flag: #if there is unregistered value until the end of loop
        idx_num.append((all_toks[-1][1], num))
        index[all_toks[-1][0]]= idx_num
        doc_freq[all_toks[-1][0]]= len(idx_num)

    return index, doc_freq

# run the index example given in the assignment text
print(index_from_tokens([("cat", 1), ("cat", 1), ("cat", 2), ("door", 1), ("water", 3)]))

# get a list of documents 
doc_list = gov_list_docs("./gov/documents")
print("Found %d documents." % len(doc_list))
num_docs = len(doc_list)

# assign unique doc_ids to each of the documents
doc_ids = make_doc_ids(doc_list)
ids_to_doc = {v:k for k, v in doc_ids.items()}

# get the list of tokens in all the documents
tok_list = get_token_list(doc_list, doc_ids)

# build the index from the list of tokens
index, doc_freq = index_from_tokens(tok_list)
#print(index_from_tokens(tok_list))
del tok_list # free some memory

# store the index to disk
pickle.dump((index, doc_freq, doc_ids, num_docs), open("stored_index.pik", "wb"))



