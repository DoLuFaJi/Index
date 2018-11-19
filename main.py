import pprint
import argparse

from interface import input_terms, input_N_topN, input_choose_algo
from algorithms import FaginAlgorithm, NaiveAlgorithm, FaginsThreshold_Algorithm, FaginsThreshold_WithEpsilon_Algorithm
from indexing import InvertedFileBuilder
from htmlwriter import HtmlWriter
from processing import Tokenization, idf
from settings import DATAFOLDER, TEST_DATAFOLDER, PL_FILE

def operation_file(datafolder, filename, map):
    inverted_file = InvertedFileBuilder(datafolder, filename, map)
    inverted_file.build_partial()
    inverted_file.merge()
    inverted_file.save()
    return inverted_file

def calculate(algo_op,N,terms,algoF,algoN,algoFT,algoFTE):
    if algo_op == 0 :
        ans = algoN.search(N,terms)
    elif algo_op == 1 :
        ans = algoF.search(N,terms)
    elif algo_op == 2 :
        ans = algoFT.search(N,terms)
    elif algo_op == 3 :
        ans = algoFTE.search(N,terms)
    return ans

def init(inverted_file):
    algoF = FaginAlgorithm(inverted_file)
    algoN = NaiveAlgorithm(inverted_file)
    algoFT = FaginsThreshold_Algorithm(inverted_file)
    algoFTE = FaginsThreshold_WithEpsilon_Algorithm(inverted_file)
    return [algoF,algoN,algoFT,algoFTE]

def op_arg_parser():
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

    return [arg_parser,args,datafolder,filename,map]

def main():
    arg_parser,args,datafolder,filename,map = op_arg_parser()

    inverted_file = operation_file(datafolder, filename, map)
    algoF,algoN,algoFT,algoFTE = init(inverted_file)
    html = HtmlWriter(datafolder)
    while not input('Enter Q (or q) for quit, otherwise continue ...\n') in ['Q','q'] :
        algo_op = input_choose_algo()
        N = input_N_topN(algo_op)
        terms = input_terms()
        #remove stop words
        tokenize = Tokenization()
        terms = tokenize.remove_stopwords(terms)
        terms = [x.lower() for x in terms]
        print(terms)

        ans = calculate(algo_op,N,terms,algoF,algoN,algoFT,algoFTE)
        print("-------------ans--------------")
        # import pdb; pdb.set_trace()
        html.writeHTMLresponse(str(terms), ans)
        pprint.pprint(ans)
        print("-------------ans--------------")

# main()
if __name__ == '__main__':
    main()
