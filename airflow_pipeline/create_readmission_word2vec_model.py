#!/usr/bin/env python
# coding: utf-8

"""
Creates Word2Vec Model
input: raw unstructured EMR data (['text'] column in our schema)
output:Word2Vec model (.bin)
Last update: 1.29.20
Author:  Andrew Malinow, PhD
"""

"""
Imports
"""
import gensim
from gensim.models import Word2Vec
import pymongo
import gridfs
import datetime
import ast
import pickle
from workflow_read_and_write import standard_read_from_db, standard_write_to_db

"""
Get Data
"""
def create_word2vec_model():
    tokens_string = standard_read_from_db('readmission_word2vec_notes_tokenized').decode()
    
    # this statement kills the process. The alternative is below.
    #tokens = ast.literal_eval(tokens_string)
    
    tokens_string = tokens_string.replace('\'','')
    tokens = tokens_String.split(',')
    # get rid of brackets from serialized list
    tokens[0] = tokens[0].split('[')[1]
    tokens[-1] = tokens[-1].split(']')[0]
    
    #model = Word2Vec([tokens], size=100, window=10, min_count=2, workers=3)
    #found readmission as one of the tokens in tokens while testing, reduced min_count to get rid of that error

    #optimiztion opportunity for LDA
    model = Word2Vec([tokens], size=100, window=10, min_count=1, workers=3)
    model_pickled = pickle.dumps(model)
    standard_write_to_db('readmission_word2vec', model_pickled)

