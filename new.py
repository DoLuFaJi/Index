import os
import pickle
import resource
import mmap
import contextlib
from heapq import merge
from struct import pack, unpack
from collections import Counter

from processing import Tokenization, idf
from settings import DATAFOLDER, TEST_DATAFOLDER, INVERTED_FILE, PL_FILE, \
LIMIT_RAM, RAM_LIMIT_MB, PL_FILE_RAM_LIMIT

STEP = 10*1024

class InvertedFileBuilder:
    def __init__(self):
        self.inverted_file = {}

        self.list_files = set(os.listdir(TEST_DATAFOLDER))
        self.nb_documents = 0
        self.complete = False
        self.part = 0

        self.__open_new_pl__()
        self.cached_posting_list = {}
        self.map_term_id = {}
        self.map_id_term = {}
        self.term_id = 0


    def __open_new_pl__(self):
        self.posting_list = []


    def build_partial(self):
        filename_processed = set()
        tokenize = Tokenization()
        documents_processed = 0
        for filename in self.list_files:
            map_doc_terms = tokenize.tokenization(filename, remove_tags=True, remove_stopwords=True, stemming=False)
            for doc, terms in map_doc_terms.items():
                documents_processed += 1
                if documents_processed > 1000:
                    self.flush()
                    documents_processed = 0
                term_frequency = Counter(terms)
                for term, frequency in term_frequency.items():
                    if term not in self.map_term_id:
                        self.map_term_id[term] = self.term_id
                        self.map_id_term[self.term_id] = term
                        self.term_id += 1
                    to_write = (int(doc), self.map_term_id[term], frequency)
                    self.posting_list.append(to_write)
                    # if term == 'youth':
                    #     print(doc + ' ' + str(frequency) + ' ' + str(self.posting_list.tell()) + ' ' + str(len(to_write)))
            filename_processed.add(filename)
            self.nb_documents += documents_processed


    def compute_idf(self):
        for term, info in self.inverted_file.items():
            index = info['index']
            idf_score = idf(info['size'], self.nb_documents)
            for i in range(len(self.posting_list[index])):
                doc, frequency = self.posting_list[index][i]
                self.posting_list[index][i] = (doc, frequency * idf_score)


    def flush(self):
        self.part += 1
        self.posting_list.sort(key=lambda entry: (entry[1], entry[0]))
        pl_file = open(PL_FILE+'.'+str(self.part), 'w')
        for tuple in self.posting_list:
            pl_file.write('{} {} {}\n'.format(tuple[0], tuple[1], tuple[2]))
        pl_file.close()
        self.__open_new_pl__()
        print('Flushed pl to disk, part ' + str(self.part))


    def merge(self):
        self.inverted_file = {}
        merged = 1
        to_merge = []
        for i in range(1, self.part+1):
            to_merge.append(PL_FILE+'.'+str(i))

        merged_pl = []
        with contextlib.ExitStack() as stack:
            files = [stack.enter_context(open(fn)) for fn in to_merge]
            with open(PL_FILE, 'wb') as f:
                for line in merge(*files, key=lambda entry: (int(entry.split()[1]), int(entry.split()[0]))):
                    docid, termid, frequency = line.split(' ')
                    to_write = pack('III', *(int(docid), int(termid), int(frequency)))
                    f.write(to_write)

        nb_lines = 0
        end_of_file = False
        with open(PL_FILE, 'r+b') as f:
            while not end_of_file:
                chunk = f.read(12)
                if chunk:
                    docid, termid, frequency = unpack('III', chunk)
                    term = self.map_id_term[termid]
                    if term not in self.inverted_file:
                        self.inverted_file[term] = {'index': nb_lines, 'size': 0, 'idf': 0}
                    self.inverted_file[term]['size'] += 1
                    nb_lines += 1
                else:
                    end_of_file = True

        for term, info in self.inverted_file.items():
            self.inverted_file[term]['idf'] = idf(info['size'], self.nb_documents)

        self.complete = True


    def __getitem__(self, term):
        term_info = self.inverted_file[term]
        index, size, idf = term_info['index'], term_info['size'], term_info['idf']
        pl = []
        if term in self.cached_posting_list:
            print('cache')
            pl = self.cached_posting_list[term]
        else:
            with open(PL_FILE, 'rb') as f:
                f.seek(index * 12)
                end_pl = 12 * (index + size)
                while not f.tell() >= end_pl:
                    chunk = f.read(12)
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

from pprint import pprint as pp
import pdb; pdb.set_trace()
