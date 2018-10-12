import os
import pprint
import resource
import mmap
import pickle
from settings import DATAFOLDER, RAM_LIMIT_MB, TEST_DATAFOLDER

from processing import tokenization, Scoring


class Vocabulary:
    def __init__(self, term):
        self.term = term
        self.posting_list_size = 0

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, other):
        return self.term == other.term

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

#compute toi meme la frequency

posting_lists = []
vocabulary_set = {}
try:
    score_calculator = Scoring()
    list_documents = os.listdir(TEST_DATAFOLDER)
    nb_documents = len(list_documents)
    for filename in list_documents:
        terms = tokenization(filename)
        print(str(len(terms)) + ' terms to process')
        for term in terms:
            vocabulary = Vocabulary(term)
            if vocabulary not in vocabulary_set:
                vocabulary_set[vocabulary] = []
            print('frequency')
            score = score_calculator.__tf__(terms, term)
            print('frequency done')
            print('append')
            vocabulary_set[vocabulary].append((filename, score))
            print('append done')
            vocabulary.posting_list_size += 1
        print(filename + ' done')

    for vocabulary, posting_lists in vocabulary_set.items():
        for document, score in posting_lists:
            print('idf')
            score *= score_calculator.__idf__(vocabulary.posting_list_size, nb_documents)
            print('idf done')
    pprint.pprint(vocabulary_set)

except MemoryError:
    flush_on_disk(vocabulary_set, posting_lists)
    print('explosion')
