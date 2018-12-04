# -*- coding: utf-8 -*-
"""
Created on Sun Nov  23 08:48:46 2018

@author: Surya

an article summarizer using LSA algorithm. 
"""
import math
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
MIN_DIMENSIONS = 3
REDUCTION_RATIO = 1

# function to remove stopwords
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new


def _create_matrix(clean_sentences, dictionary):
    word_count = len(dictionary)
    sentences_count = len(clean_sentences)
   # create matrix  of unique words× sentences 
    matrix = np.zeros((word_count, sentences_count))
    for col, sentence in enumerate(clean_sentences):
#stem each word in a sentence and see if it is unique words dictionary
        for w in sentence.split():
            w=lemmatizer.lemmatize(w)
            if w in dictionary:
                row = dictionary[w]
                matrix[row, col] += 1
    return matrix

def _compute_term_frequency(matrix):
#    normalizing each cell in matrix wrt to max word frequencies, and then adding the TF to it
    smooth=0.4
    assert 0.0 <= smooth < 1.0
    max_word_frequencies = np.max(matrix, axis=0)
    rows, cols = matrix.shape
    for row in range(rows):
        for col in range(cols):
            max_word_frequency = max_word_frequencies[col]
            if max_word_frequency != 0:
                frequency = matrix[row, col]/max_word_frequency
                matrix[row, col] = smooth + (1.0 - smooth)*frequency

    return matrix

def _compute_ranks(sigma, v_matrix):
    #checking the matrix dimensions for validity in multiplizations
    if len(sigma) != v_matrix.shape[0]:
        return None
    dimensions = max(MIN_DIMENSIONS,
    int(len(sigma)*REDUCTION_RATIO))
    powered_sigma = tuple(s**2 if i < dimensions else 0.0
    for i, s in enumerate(sigma))
    ranks = []
        # iterate over columns of matrix and computing the ranks
    for column_vector in v_matrix.T:
        rank = sum(s*v**2 for s, v in zip(powered_sigma, column_vector))
        ranks.append(math.sqrt(rank))

    return ranks
        
def summarize(sentences):
    sentences_new = []
    unique_words=set()
    for y in sentences:
        sentences_new.append(y)
#        in each sentence of an article doing all cleaning operations
    # remove punctuations, numbers and special characters
    clean_sentences = pd.Series(sentences_new).str.replace("[^a-zA-Z]"," ")    
    # remove stopwords from the sentences
    clean_sentences = [remove_stopwords(r.split()) for r in sentences_new]

# make each word to lowercase and getting unique words
    for s in clean_sentences:
        words=s.split()
        for w in words:
            w=w.lower()
            unique_words.add(lemmatizer.lemmatize(w))                
    #dict of unique words    
    dictionary=dict((w, i) for i, w in enumerate(unique_words))
    matrix= _create_matrix(clean_sentences,dictionary)
    matrix=_compute_term_frequency(matrix)
#    do svd and geth the most important ranks, 
    u, sigma, v = np.linalg.svd(matrix, full_matrices=False)
    ranks = _compute_ranks(sigma, v)
    if not ranks:
        print("error in summarization")
        return ''
    ranked_sentences={}
#   giving a 13 sentence summary.
    for num,sen in enumerate(clean_sentences):
        ranked_sentences[ranks[num]]=sen
        out=''    
        i=-1
        for key in sorted(ranked_sentences,reverse=True):
            if i<13:
                out+=ranked_sentences[key]
                i+=1
            else:
                break        
    return out