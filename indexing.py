import os
import pickle
import resource
import mmap
import contextlib
from heapq import merge
from struct import pack, unpack
from collections import Counter
import numpy

from processing import Tokenization, idf
from settings import LIMIT_RAM, RAM_LIMIT_MB, PL_FILE_RAM_LIMIT, CHUNK_SIZE

class InvertedFileBuilder:
    def __init__(self, datafolder, filename, mit, batch_size, stemming):
        self.inverted_file = {}

        self.batch_size = batch_size
        self.stemming = stemming

        self.filename = filename
        self.datafolder = datafolder
        self.list_files = set(os.listdir(self.datafolder))
        self.nb_documents = 0
        self.complete = (mit is not '')
        self.part = 0

        self.__open_new_pl__()
        self.cached_posting_list = {}
        self.map_term_id = {}
        self.map_id_term = {}
        if self.complete:
            self.map_id_term = pickle.load(open(mit, 'rb'))
        self.term_id = 0

        self.random_indexing_doc = {}
        self.random_indexing_word = {}


    def __open_new_pl__(self):
        self.posting_list = []


    def save(self):
        pickle.dump(self.map_id_term, open(self.filename+'_mit', 'wb'))

    def build_partial(self):
        if not self.complete:
            tokenize = Tokenization()
            documents_processed = 0
            for filename in self.list_files:
                map_doc_terms = tokenize.tokenization(filename, self.datafolder, remove_tags=True, remove_stopwords=True, stemming=self.stemming)
                for doc, terms in map_doc_terms.items():
#########################################
                    random_indexing_doc[doc] = numpy.zeros(5000)
                    for i in range(0, 5):
                        random_indexing_doc[doc][i] = 1
                    for i in range(6, 11):
                       random_indexing_doc[doc][i] = -1
                    numpy.random.shuffle(random_indexing_doc[doc])
#########################################
                    documents_processed += 1
                    if documents_processed > self.batch_size:
                        self.flush()
                        documents_processed = 0
                    term_frequency = Counter(terms)
                    for term, frequency in term_frequency.items():
                        if term not in self.map_term_id:
                            self.map_term_id[term] = self.term_id
                            self.map_id_term[self.term_id] = term
############################################
                            random_indexing_word[term] = numpy.zeros(5000)
###########################################
                            self.term_id += 1
###########################################
                        random_indexing_word[term] += random_indexing_doc[doc]
###########################################
                        to_write = (int(doc), self.map_term_id[term], frequency)
                        self.posting_list.append(to_write)
                self.flush()
        else:
            print('Ignore building because complete')


    def flush(self):
        self.part += 1
        self.posting_list.sort(key=lambda entry: (entry[1], entry[0]))
        pl_file = open(self.filename+'.'+str(self.part), 'w')
        for tuple in self.posting_list:
            pl_file.write('{} {} {}\n'.format(tuple[0], tuple[1], tuple[2]))
        pl_file.close()
        self.__open_new_pl__()
        print('Flushed pl to disk, part ' + str(self.part))


    def merge(self):
        if not self.complete:
            self.inverted_file = {}
            merged = 1
            to_merge = []
            for i in range(1, self.part+1):
                to_merge.append(self.filename+'.'+str(i))

            merged_pl = []
            with contextlib.ExitStack() as stack:
                files = [stack.enter_context(open(fn)) for fn in to_merge]
                with open(self.filename, 'wb') as f:
                    for line in merge(*files, key=lambda entry: (int(entry.split()[1]), int(entry.split()[0]))):
                        docid, termid, frequency = line.split(' ')
                        to_write = pack('III', *(int(docid), int(termid), int(frequency)))
                        f.write(to_write)

        self.complete = True
        nb_lines = 0
        end_of_file = False
        doc_set = set()
        with open(self.filename, 'r+b') as f:
            while not end_of_file:
                chunk = f.read(CHUNK_SIZE)
                if chunk:
                    docid, termid, frequency = unpack('III', chunk)
                    doc_set.add(docid)
                    term = self.map_id_term[termid]
                    if term not in self.inverted_file:
                        self.inverted_file[term] = {'index': nb_lines, 'size': 0, 'idf': 0}
                    self.inverted_file[term]['size'] += 1
                    nb_lines += 1
                else:
                    end_of_file = True

        self.nb_documents = len(doc_set)
        for term, info in self.inverted_file.items():
            self.inverted_file[term]['idf'] = idf(info['size'], self.nb_documents)


    def __getitem__(self, term):
        if term not in self.inverted_file:
            return []
        term_info = self.inverted_file[term]
        index, size, idf = term_info['index'], term_info['size'], term_info['idf']
        pl = []
        if term in self.cached_posting_list:
            pl = self.cached_posting_list[term]
        else:
            with open(self.filename, 'rb') as f:
                f.seek(index * CHUNK_SIZE)
                end_pl = CHUNK_SIZE * (index + size)
                while not f.tell() >= end_pl:
                    chunk = f.read(CHUNK_SIZE)
                    if chunk:
                        docid, termid, frequency = unpack('III', chunk)
                        if term == self.map_id_term[termid]:
                            pl.append((docid, frequency * idf))
                        else:
                            print('going to far {} not {}'.format(self.map_id_term[termid], term))
                    else:
                        print('euuh')
            self.cached_posting_list[term] = pl
        return pl


# if LIMIT_RAM:
#     resource.setrlimit(resource.RLIMIT_AS, (RAM_LIMIT_MB*1024*1024, RAM_LIMIT_MB*1024*1024))
#
# ifb = InvertedFileBuilder()
# try:
#     ifb.build_partial()
# except MemoryError:
#     print(resource.getrusage(resource.RUSAGE_SELF))
#     ifb.flush()
# ifb.flush()
# ifb.merge()
#
# from pprint import pprint as pp
# import pdb; pdb.set_trace()
