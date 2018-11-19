#This file countains all the global variables

DATAFOLDER = "./data/latimes/"
TEST_DATAFOLDER = "./data/test/"
DATAFOLDER_ALGO = "./data/test_algo/"

LIMIT_RAM = False
DEFAULT_PYTHON_SIZE_MB = 450
PL_FILE_RAM_LIMIT = 30
RAM_LIMIT_MB = PL_FILE_RAM_LIMIT + DEFAULT_PYTHON_SIZE_MB

SAVE_INDEX = True
INDEX_NAME = 'index.p'
MMAP_FILE = 'mmap.txt'

DEBUG = False
EPSILON = 0.5

CHUNK_SIZE = 12
INVERTED_FILE = 'inverted_file_part'
PL_FILE = 'pl_file_part'
BATCH_SIZE = 1000
