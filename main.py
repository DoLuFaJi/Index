import pprint

from interface import input_terms, input_N_topN, input_choose_algo
from algorithms import FaginAlgorithm, NaiveAlgorithm, FaginsThreshold_Algorithm, FaginsThreshold_WithEpsilon_Algorithm
from indexing import InvertedFileBuilder

from htmlwriter import HtmlWriter

inverted_file = InvertedFileBuilder()
inverted_file.build_partial()
inverted_file.merge()

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


algoF = FaginAlgorithm(inverted_file)
algoN = NaiveAlgorithm(inverted_file)
algoFT = FaginsThreshold_Algorithm(inverted_file)
algoFTE = FaginsThreshold_WithEpsilon_Algorithm(inverted_file)

html = HtmlWriter()
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
