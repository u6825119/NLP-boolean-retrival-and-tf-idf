from collections import defaultdict
import pickle
import os
import numpy as np
import nltk

from string_processing import *

def intersect_query(doc_list1, doc_list2):
    '''Returns the intersection of two doc_id lists, ordered
    Args:
        doc_list1 (list(int)): a list of doc_ids 
        doc_list1 (list(int)): a list of doc_ids 
    Returns:
        list(int): intersection of two given lists, ordered
    '''
    list1 = []
    i_1, i_2 = 0,0
    while i_1 < len(doc_list1) and i_2 < len(doc_list2):
        if doc_list1[i_1] == doc_list2[i_2]: #only append common elements
            list1.append(doc_list1[i_1])
            i_1 += 1
            i_2 += 1
        elif doc_list1[i_1] < doc_list2[i_2]: 
            i_1 += 1
        else:
            i_2 += 1
    
    return list1

def union_query(doc_list1, doc_list2):
    '''Returns the union of two doc_id lists, ordered
    Args:
        doc_list1 (list(int)): a list of doc_ids 
        doc_list1 (list(int)): a list of doc_ids 
    Returns:
        list(int): union of two given lists, ordered
    '''
    list1 = []
    i_1, i_2 = 0,0
    while i_1 < len(doc_list1) and i_2 < len(doc_list2):
        if doc_list1[i_1] == doc_list2[i_2]:
            list1.append(doc_list1[i_1])
            i_1 += 1
            i_2 += 1
        elif doc_list1[i_1] < doc_list2[i_2]: 
            list1.append(doc_list1[i_1])
            i_1 += 1
        else:
            list1.append(doc_list2[i_2])
            i_2 += 1
    if i_1 < len(doc_list1): #concat leftover elements not looped
        list1 += doc_list1[i_1:] 
    elif i_2 < len(doc_list2):    
        list1 += doc_list2[i_2:]
        
    return list1

def run_boolean_query(query, index):
    """Runs a boolean query using the index.

    Args:
        query (str): boolean query string
        index (dict(str : list(tuple(int, int)))): The index aka dictonary of posting lists

    Returns:
        list(int): a list of doc_ids which are relevant to the query
    """
    #tokenize query
    tok = query.split()
    return helper_boolean_query(tok, index)


def helper_boolean_query(tok, index):
    ''' Unfold boolean function from right to left through recursion, 
    returns the result of boolean query as a list of document ids.
    Args:
        query (list(str)): boolean query list
        index (dict(str : list(tuple(int, int)))): The index aka dictonary of posting lists

    Returns:
        list(int): a list of doc_ids which are relevant to the query'''
    
    if len(tok) <= 0:  #empty list
        return []
    
    right = [tup[0] for tup in index[tok[-1]]]
    # make the document IDs containing rightmost term a list
    if len(tok) ==3:                                   #Base case: 3 elements ['term', 'operator', 'term']
        left = [tup[0] for tup in index[tok[0]]]       # make the document IDs containing leftmost term a list
        if tok[1] == "AND":
            return intersect_query(left, right) 
        if tok[1] == "OR":              
            return union_query(left, right)
    elif len(tok) == 1: #only one element, return all document IDs containing this term
        return right
    else:     # recursion with rightmost term and operator eliminated(translated into operator helper function)
        if tok[-2] == "AND":
            return intersect_query(helper_boolean_query(tok[:-2], index), right)
        if tok[-2] == "OR":              
            return union_query(helper_boolean_query(tok[:-2], index), right)
    

# load the stored index
(index, doc_freq, doc_ids, num_docs) = pickle.load(open("stored_index.pik", "rb"))
print("Index length:", len(index))
if len(index) != 906290:
    print("Warning: the length of the index looks wrong.")
    print("Make sure you are using `process_tokens_original` when you build the index.")
    raise Exception()

# the list of queries asked for in the assignment text
queries = [
    "Welcoming",
    "unwelcome OR sam",
    "ducks AND water",
    "plan AND water AND wage",
    "plan OR record AND water AND wage",
    "space AND engine OR football AND placement"
]

# run each of the queries and print the result
ids_to_doc = {v:k for k, v in doc_ids.items()}
for q in queries:
    res = run_boolean_query(q, index)
    res.sort(key=lambda x: ids_to_doc[x])
    print(q)
    for r in res:
        print(ids_to_doc[r])





