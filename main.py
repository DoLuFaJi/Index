import pprint
import argparse

from interface import input_terms, input_N_topN, input_choose_algo
from algorithms import FaginAlgorithm, NaiveAlgorithm, FaginsThreshold_Algorithm, FaginsThreshold_WithEpsilon_Algorithm
from indexing import InvertedFileBuilder
from htmlwriter import HtmlWriter
from settings import DATAFOLDER, TEST_DATAFOLDER, PL_FILE

def calculate(algo_op, N, terms):
    if algo_op == 0 :
        ans = algoN.search(N,terms)
    elif algo_op == 1 :
        ans = algoF.search(N,terms)
    elif algo_op == 2 :
        ans = algoFT.search(N,terms)
    elif algo_op == 3 :
        ans = algoFTE.search(N,terms)
    return ans

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--datafolder', help='Choose datafolder', type=str)
arg_parser.add_argument('-n', '--name', help='Choose filename', type=str)
arg_parser.add_argument('-m', '--map', help='Map id term, set to load an index', type=str)

datafolder = DATAFOLDER
filename = PL_FILE
map = ''
args = arg_parser.parse_args()
if args.datafolder is not None:
    datafolder = args.datafolder
    if datafolder is 't':
        datafolder = TEST_DATAFOLDER
if args.name is not None:
    filename = args.name
if args.map is not None:
    map = args.map

inverted_file = InvertedFileBuilder(datafolder, filename, map)
inverted_file.build_partial()
inverted_file.merge()
inverted_file.save()

algoF = FaginAlgorithm(inverted_file)
algoN = NaiveAlgorithm(inverted_file)
algoFT = FaginsThreshold_Algorithm(inverted_file)
algoFTE = FaginsThreshold_WithEpsilon_Algorithm(inverted_file)

html = HtmlWriter(datafolder)
while not input('Enter Q (or q) for quit, otherwise continue ...\n') in ['Q','q'] :
    algo_op = input_choose_algo()
    N = input_N_topN(algo_op)
    terms = input_terms()
    print(terms)
    ans = calculate(algo_op,N,terms)
    print("-------------ans--------------")
    # import pdb; pdb.set_trace()
    html.writeHTMLresponse(str(terms), ans)
    pprint.pprint(ans)
    print("-------------ans--------------")
