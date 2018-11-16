import os
import pprint
import resource
import mmap
import numpy as np
from numpy.lib.format import open_memmap
import pickle

from settings import DATAFOLDER, RAM_LIMIT_MB, TEST_DATAFOLDER, SAVE_INDEX, INDEX_NAME, DEBUG, MMAP_FILE
from processing import Tokenization, Scoring
from algorithms import NaiveAlgorithm
from algorithms import FaginAlgorithm
from algorithms import FaginsThreshold_Algorithm
from algorithms import FaginsThreshold_WithEpsilon_Algorithm
from document import Document
from htmlwriter import HtmlWriter

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

class Posting:
    def __init__(self, doc, frequency):
        self.doc = doc
        self.score = frequency

    def compute_score(self, idf):
        self.score *= idf

    def __repr__(self):
        return self.doc + ' : ' + str(self.score)


def flush_on_disk(inverted_file, posting_lists):
    pickle.dump(inverted_file, open('if.p', 'wb'))
    posting_lists.flush()

def input_N_topN(algo_op):
    N = -1
    while (not algo_op == 0) and True:
        try :
            N = int(input('Top ?  (the X of the TopX results ) :'))
            if N > 0 :
                break
        except :
            print ("Enter an integer plz")
    return N

def input_terms():
    print("Enter terms one by one, line by line and end by 'E' : ")
    terms = []
    x = input('')
    while not x == "E" :
        terms.append(x)
        x = input('')
    return terms

def input_choose_algo():
    while True :
        try:
            algo_op = int(input("0 for Naive, 1 for Fagin, 2 for Fagins Threshold, 3 for Fagins Threshold With Epsilon\n"))
            if algo_op in [0,1,2,3] :
                break
            else :
                print ("0 or 1 or 2 or 3 plz")
        except :
            print ("0 or 1 or 2 or 3 plz")
    return algo_op

def calculate(algo_op,N,terms):
    if algo_op == 0 :
        ans = algoN.search(N,terms)
    elif algo_op == 1 :
        ans = algoF.search(N,terms)
    elif algo_op == 2 :
        ans = algoFT.search(N,terms)
    elif algo_op == 3 :
        ans = algoFTE.search(N,terms)
    return ans
# limit RAM here.
resource.setrlimit(resource.RLIMIT_AS, (RAM_LIMIT_MB*1024*1024, RAM_LIMIT_MB*1024*1024))
# file = open(MMAP_FILE, 'wb')
# mm_posting_lists = mmap.mmap(-1, 1024*1024*1024)
# mm_posting_lists = np.memmap(MMAP_FILE, dtype='float32', mode='w+', shape=(10**13,2))
# mm_posting_lists = open_memmap(MMAP_FILE, mode='w+', dtype=np.ubyte, shape=(10**9, 2))

posting_lists = []
vocabulary_set = {}
try:
    score_calculator = Scoring()
    tokenizator = Tokenization()
    list_files = os.listdir(TEST_DATAFOLDER)
    nb_files = len(list_files)
    nb_documents = 0
    index = 0
    for filename in list_files:
        doc_terms = tokenizator.tokenization(filename)
        for doc, terms in doc_terms.items():
            term_frequency = {}
            nb_documents += 1
            # Count frequency.
            for term in terms:
                if term not in term_frequency:
                    term_frequency[term] = 0
                term_frequency[term] += 1

            for term, frequency in term_frequency.items():
                vocabulary = Vocabulary(term)
                if term not in vocabulary_set:
                    vocabulary_set[vocabulary] = index
                    posting_lists.insert(index, [])
                    # import pdb
                    # pdb.set_trace()
                    # mm_posting_lists[index] = []

                    index += 1
                posting_lists[vocabulary_set[term]].append(Posting(doc, frequency))
                # import pdb; pdb.set_trace()
                # mm_posting_lists.seek(mm_posting_lists[vocabulary_set[term]])
                # mm_posting_lists.write(doc.encode())


    for vocabulary, index_pl in vocabulary_set.items():
        vocabulary.posting_list_size = len(posting_lists[index_pl])
        idf_for_term = score_calculator.__idf__(vocabulary.posting_list_size, nb_documents)
        for posting in posting_lists[index_pl]:
            posting.compute_score(idf_for_term)

    if SAVE_INDEX:
        pickle.dump(vocabulary_set, open(INDEX_NAME, 'wb'))
        pickle.dump(posting_lists, open(MMAP_FILE, 'wb'))

#    import pdb
#    pdb.set_trace()

    # pprint.pprint(mm_posting_lists)
    if DEBUG:
        algoF = FaginAlgorithm(vocabulary_set,posting_lists)
        algoN = NaiveAlgorithm(vocabulary_set,posting_lists)
        algoFT = FaginsThreshold_Algorithm(vocabulary_set,posting_lists)
        algoFTE = FaginsThreshold_WithEpsilon_Algorithm(vocabulary_set,posting_lists)
        while not input('Enter Q (or q) for quit, otherwise continue ...\n') in ['Q','q'] :
            algo_op = input_choose_algo()
            N = input_N_topN(algo_op)
            terms = input_terms()
            print(terms)
            ans = calculate(algo_op,N,terms)
            print("-------------ans--------------")
            pprint.pprint(ans)
            print("-------------ans--------------")
            # html = HtmlWriter()
            # terms_string = ''.join(terms)
            # print("---"+terms_string+"---")
            # html.writeHTMLresponse(terms_string,ans)


except MemoryError:
    print('explosion')
    import pdb; pdb.set_trace()
    # flush_on_disk(vocabulary_set, posting_lists)

# except:
#     print('Crash !')
    # import pdb
    # pdb.set_trace()

print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
print('memory used')
file.close()
