import os
import pprint
import resource
import mmap
import pickle
from settings import DATAFOLDER, RAM_LIMIT_MB, TEST_DATAFOLDER, SAVE_INDEX, INDEX_NAME, DEBUG, MMAP_FILE

from processing import Tokenization, Scoring
from algorithms import NaiveAlgorithm
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


# limit RAM here.
# resource.setrlimit(resource.RLIMIT_AS, (RAM_LIMIT_MB*1024, RAM_LIMIT_MB*1024))
file = open(MMAP_FILE, 'wb')
mm_posting_lists = mmap.mmap(-1, 1024*1024*1024)

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
                mm_posting_lists.seek(mm_posting_lists[vocabulary_set[term]])
                mm_posting_lists.write(doc.encode())


    for vocabulary, index_pl in vocabulary_set.items():
        vocabulary.posting_list_size = len(posting_lists[index_pl])
        idf_for_term = score_calculator.__idf__(vocabulary.posting_list_size, nb_documents)
        for posting in posting_lists[index_pl]:
            posting.compute_score(idf_for_term)

    if SAVE_INDEX:
        pickle.dump(vocabulary_set, open(INDEX_NAME, 'wb'))

    import pdb
    pdb.set_trace()
    # pprint.pprint(mm_posting_lists)
    if DEBUG:
        algo = NaiveAlgorithm(vocabulary_set)
        pprint.pprint(algo.search(['reserved']))
        pprint.pprint(vocabulary_set['reserved'])

except MemoryError:
    flush_on_disk(vocabulary_set, posting_lists)
    print('explosion')
# except:
#     print('Crash !')
    # import pdb
    # pdb.set_trace()


file.close()
