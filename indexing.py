import os
import pprint
import resource
import mmap
import pickle
from settings import DATAFOLDER, RAM_LIMIT_MB, TEST_DATAFOLDER, SAVE_INDEX, INDEX_NAME

from processing import Tokenization, Scoring
from algorithms import NaiveAlgorithm
from algorithms import FaginsThreshold_Algorithm
from document import Document

import nltk
from nltk.stem import *
from nltk.stem.porter import *

class Vocabulary:
    def __init__(self, term):
        self.term = term
        self.posting_list_size = 0

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, other):
        return self.term == other

    def __str__(self):
        return self.term

    def __repr__(self):
        return self.term

def flush_on_disk(inverted_file, posting_lists):
    pickle.dump(inverted_file, open('if.p', 'wb'))
    posting_lists.flush()


# limit RAM here.
# resource.setrlimit(resource.RLIMIT_AS, (RAM_LIMIT_MB*1024, RAM_LIMIT_MB*1024))

# posting_lists = mmap.mmap(-1, RAM_LIMIT_MB*1024)
posting_lists = []
vocabulary_set = {}
try:
    score_calculator = Scoring()
    tokenizator = Tokenization()
    list_documents = os.listdir(DATAFOLDER)
    nb_documents = len(list_documents)
    porter = nltk.PorterStemmer()
    for filename in list_documents:
        term_frequency = {}
        terms = tokenizator.tokenization(filename)
        nb_terms = len(terms)
        #print(str(len(terms)) + ' terms to process')
        for term in terms:
            porter.stem(term)
            # Compute frequency.
            if term not in term_frequency:
                term_frequency[term] = 0
            term_frequency[term] += 1

            vocabulary = Vocabulary(term)
            if vocabulary not in vocabulary_set:
                vocabulary_set[vocabulary] = {}
            if filename not in vocabulary_set[vocabulary]:
                 vocabulary_set[vocabulary][filename] = 0
            # Update frequency each time we encounted this term.
            vocabulary_set[vocabulary][filename] = term_frequency[term] / nb_terms
#        print(filename + ' done')

    for vocabulary, posting_lists in vocabulary_set.items():
        vocabulary.posting_list_size = len(posting_lists.keys())
        idf_for_term = score_calculator.__idf__(vocabulary.posting_list_size, nb_documents)
        for filename in posting_lists.keys():
            # set new score
            posting_lists[filename] *= idf_for_term

    if SAVE_INDEX:
        pickle.dump(vocabulary_set, open(INDEX_NAME, 'wb'))
    # pprint.pprint(vocabulary_set)

    algo = FaginsThreshold_Algorithm(vocabulary_set)
    pprint.pprint(algo.search(3,['156341']))
    pprint.pprint(vocabulary_set['156341'])

except MemoryError:
    flush_on_disk(vocabulary_set, posting_lists)
    print('explosion')
