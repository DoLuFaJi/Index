import os
import pickle
import resource
import mmap
from struct import pack
from collections import Counter

from processing import Tokenization, idf
from settings import DATAFOLDER, TEST_DATAFOLDER, INVERTED_FILE, PL_FILE, \
LIMIT_RAM, RAM_LIMIT_MB, PL_FILE_RAM_LIMIT

STEP = 10*1024

class InvertedFileBuilder:
    def __init__(self):
        self.inverted_file = {}
        self.chunk_size = PL_FILE_RAM_LIMIT * 1024 * 1024
        file_size = 5 * 1024 * 1024 * 1024
        self.pl_file = open(PL_FILE, 'wb')
        self.pl_file.seek(file_size - 1)
        self.pl_file.write(b'\0')
        self.pl_file.close()

        self.pl_index = 0
        self.list_files = set(os.listdir(TEST_DATAFOLDER))
        self.nb_documents = 0
        self.complete = False
        self.part = 0

        self.pl_file = open(PL_FILE, 'r+b')
        self.__open_new_pl__()
        self.map_term_id = {}
        self.term_id = 0

    def __open_new_pl__(self):
        self.posting_list = mmap.mmap(self.pl_file.fileno(), self.chunk_size, access=mmap.ACCESS_WRITE, offset=self.part*self.chunk_size)
        self.posting_list.write(b'stop')
        self.posting_list.seek(0)

    def build_partial(self):
        try:
            filename_processed = set()
            tokenize = Tokenization()
            for filename in self.list_files:
                map_doc_terms = tokenize.tokenization(filename, remove_tags=True, remove_stopwords=True, stemming=False)
                documents_processed = 0
                for doc, terms in map_doc_terms.items():
                    documents_processed += 1
                    term_frequency = Counter(terms)
                    for term, frequency in term_frequency.items():
                        if term not in self.inverted_file:
                            self.map_term_id[term] = self.term_id
                            self.inverted_file[term] = {'index': [], 'size': 0, 'bytesize': 0}
                        # to_write = pack('III', *(int(doc), self.map_term_id[term], frequency))
                        to_write = (int(doc), self.map_term_id[term], frequency)
                        self.posting_list.append(to_write)
                        # if term == 'youth':
                        #     print(doc + ' ' + str(frequency) + ' ' + str(self.posting_list.tell()) + ' ' + str(len(to_write)))
                        self.inverted_file[term]['index'].append(self.part * self.chunk_size + self.posting_list.tell())
                        # self.posting_list.write(to_write)
                        self.inverted_file[term]['size'] += 1
                        self.inverted_file[term]['bytesize'] += len(to_write)
                filename_processed.add(filename)
                self.nb_documents += documents_processed

        except ValueError as e:
            print(e)
            self.list_files.difference_update(filename_processed)
            self.flush()
            self.build_partial()

    def compute_idf(self):
        for term, info in self.inverted_file.items():
            index = info['index']
            idf_score = idf(info['size'], self.nb_documents)
            for i in range(len(self.posting_list[index])):
                doc, frequency = self.posting_list[index][i]
                self.posting_list[index][i] = (doc, frequency * idf_score)

    def flush(self):
        self.part += 1
        self.posting_list.flush()
        self.__open_new_pl__()

        pickle.dump(self.inverted_file, open(INVERTED_FILE+'.'+str(self.part), 'wb'))
        self.inverted_file = {}
        print('Flushed if and pl to disk, part ' + str(self.part))

    def merge(self):
        self.inverted_file = pickle.load(open(INVERTED_FILE+'.'+str(1), 'rb'))
        for i in range(2, self.part+1):
            partial_if = pickle.load(open(INVERTED_FILE+'.'+str(i), 'rb'))
            for term, info in partial_if.items():
                if term not in self.inverted_file:
                    self.inverted_file[term] = info
                else:
                    self.inverted_file[term]['size'] += info['size']
                    self.inverted_file[term]['bytesize'] += info['bytesize']
                    self.inverted_file[term]['index'].extend(info['index'])
        import pdb; pdb.set_trace()

if LIMIT_RAM:
    resource.setrlimit(resource.RLIMIT_AS, (RAM_LIMIT_MB*1024*1024, RAM_LIMIT_MB*1024*1024))
ifb = InvertedFileBuilder()
try:
    ifb.build_partial()
except MemoryError:
    print(resource.getrusage(resource.RUSAGE_SELF))
    ifb.flush()
ifb.flush()
ifb.merge()

# from pprint import pprint as pp
# import pdb; pdb.set_trace()
