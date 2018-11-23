from main import operation_file, init, calculate, op_arg_parser
import random
import string
import time
import pprint
import progressbar
import matplotlib.pyplot as plt

from settings import BATCH_SIZE, EPSILON, DATAFOLDER, PL_FILE, TEST_DATAFOLDER, STEMMING
from indexing import InvertedFileBuilder

import argparse
import timeit


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def test_arg_parser():
    arg_parser = argparse.ArgumentParser("Run the tests")

    arg_parser.add_argument('-d', '--datafolder', help='Choose datafolder', type=str)
    arg_parser.add_argument('-n', '--name', help='Choose filename', type=str)
    arg_parser.add_argument('-m', '--map', help='Map id term, set to load an index', type=str)
    arg_parser.add_argument('-s', '--stemming', help='Do you want stemming ? (yes) -take a lit of time ==', type=str)
    arg_parser.add_argument('-b', '--batchsize', help='Choose your batch size - default=1000', type=int)
    arg_parser.add_argument('-e', '--epsilon', help='Epsilon for Fagins', type=float)

    arg_parser.add_argument('-c', '--numberoftest', help='How many times tests must be run', type=int)
    arg_parser.add_argument('-t', '--tests', help='Tests to run (a k e n b: algo, k, epsilon, nbterms, batchsize)', type=str)
    arg_parser.add_argument('-r', '--nbterms', help='nb terms in request', type=int)

    arg_parser.add_argument('-k', '--k', help='k for fagins', type=int)

    datafolder = DATAFOLDER
    filename = PL_FILE
    epsilon = EPSILON
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

    if args.stemming is not None:
        STEMMING = True
    if args.batchsize is not None:
        BATCHSIZE = args.batchsize
    if args.epsilon is not None:
        epsilon = args.epsilon

    NbTest = 500
    test_algo = False
    test_k = False
    test_epsilon = False
    test_nbterms = False
    test_batch = False

    k_fagins = 1
    N_terms = 2

    args = arg_parser.parse_args()
    if args.numberoftest is not None:
        NbTest = args.numberoftest
    if args.tests is not None:
        if "a" in args.tests:
            test_algo = True
            if "k" in args.tests:
                test_k = True
            if "e" in args.tests:
                test_epsilon = True
            if "n" in args.tests:
                test_nbterms = True
            if args.k is not None:
                k_fagins = args.k
        if "b" in args.tests:
                test_batch = True
        if args.nbterms is not None:
            N_terms = args.nbterms

    return [arg_parser,args,datafolder,filename,map, NbTest, test_algo, test_k, test_epsilon, test_nbterms, test_batch, k_fagins,epsilon,N_terms]

def test_answer():
    print("Start of loading files...")
    inverted_file = operation_file(datafolder, filename, map)
    print("End of loading files.")
    algoF,algoN,algoFT,algoFTE = init(inverted_file)
    print("End of init.")
    ans = [0,0,0,0]
    t = [0,0,0,0]
    rate = [0.0,0.0,0.0,0.0]
    print("Start of running the tests...")
    bar.start()

    list_nbterms = []
    list_k = []
    list_e = []
    list_times = [[],[],[],[]]
    list_results = [[],[],[],[]]

    for k in range(NbTest):
    #while True:
        bar.update(k + 1)
        N = k_fagins
        ep = epsilon
        nterms = N_terms
        if test_k:
            N = random.randint(1,3)
        terms = []
        if test_nbterms:
            nterms = random.randint(1,3)
        if test_epsilon:
            ep = random.random()
        # N_terms = 1
        for i in range(nterms) :
            term = random.choice(list(inverted_file.inverted_file.keys()))         # get random terms from dictionary
            while inverted_file.inverted_file[term]['size'] < 500 :
                term = random.choice(list(inverted_file.inverted_file.keys()))
            terms.append(term)
        #print("-------------ans--------------")
        #print(k)
        #print(terms)

        for op_algo in [0,1,2,3]:
            t1 = time.time()
            #import timeit
            #t[op_algo] = timeit.timeit("calculate(op_algo,N,terms,algoF,algoN,algoFT,algoFTE)", globals=globals())
            #cProfile.run('calculate(op_algo,N,terms,algoF,algoN,algoFT,algoFTE)')
            ans[op_algo] = calculate(op_algo,N,terms,algoF,algoN,algoFT,algoFTE)
            t2 = time.time()
            t[op_algo] = t2 - t1
            #list_times[op_algo].append(t[op_algo])
            #pprint.pprint(ans[op_algo])
            #Sprint(t[op_algo])
        for j in range(len(ans[3])):
            for i in [1,2]:
                #assert(ans[i][j].score == ans[0][j].score)
                #if abs (ans[i][j].score - ans[0][j].score)> 0.00001 :
                if ans[i][j].score != ans[0][j].score :
                    print("bad results for algo...."+str(i)+" "+str(terms)+" difference="+str(ans[i][j].score - ans[0][j].score)+" doc: "+str(j))

        for j in range(len(ans[3])):
            if abs (ans[i][j].score - ans[0][j].score) / ans[0][j].score > EPSILON :
                print("bad results for algo...."+str(i)+" "+str(terms)+" difference rate="+str((ans[i][j].score - ans[0][j].score) / ans[0][j].score))
        if len(ans[0]) > 50 :
            rate[1] += t[1]/t[0]
            rate[2] += t[2]/t[0]
            rate[3] += t[3]/t[0]
            list_times[0].append(1)
            list_times[1].append(t[1]/t[0])
            list_times[3].append(t[3]/t[0])
            list_times[2].append(t[2]/t[0])

            list_results[0].append(len(ans[0]))
            list_results[1].append(len(ans[1]))
            list_results[2].append(len(ans[2]))
            list_results[3].append(len(ans[3]))

            list_nbterms.append(nterms)
            list_k.append(N)
            list_e.append(ep)

            if t[1]/t[0] > 1:
                print("time too long for algo 1 "+str(terms)+str(t[1]/t[0]))
            if t[2]/t[0] > 1:
                print("time too long for algo 2 "+str(terms)+str(t[2]/t[0]))
            if t[3]/t[0] > 1:
                print("time too long for algo 3 "+str(terms)+str(t[3]/t[0]))


        #print("-------------ans--------------\n")

    bar.finish()

    Nb = len(list_nbterms)
    if Nb == 0:
        print("no results")
    else:
        print( "Fagins :")
        print( "    " + str(int((1-rate[1]/Nb)*100)) + "% acceleration compared with naive algo." )
        print( "Fagins Threshold :")
        print( "    " + str(int((1-rate[2]/Nb)*100)) + "% acceleration compared with naive algo." )
        print( "    " + str(int((1-rate[2]/rate[1])*100)) + "% acceleration compared with Fagins." )
        print( "Fagins Threshold With Epsilon:")
        print( "    " + str(int((1-rate[3]/Nb)*100)) + "% acceleration compared with naive algo." )
        print( "    " + str(int((1-rate[3]/rate[1])*100)) + "% acceleration compared with Fagins." )
        print( "    " + str(int((1-rate[3]/rate[2])*100)) + "% acceleration compared with Fagins Threshold." )

        plt.title("4 algo")
        plt.plot(list_nbterms, list_times[0], 'ro')
        list_nbterms = [x+0.1 for x in list_nbterms]
        plt.plot(list_nbterms, list_times[1], 'go')
        list_nbterms = [x+0.1 for x in list_nbterms]
        plt.plot(list_nbterms, list_times[2], 'bo')
        list_nbterms = [x+0.1 for x in list_nbterms]
        plt.plot(list_nbterms, list_times[3], 'ko')
        plt.show()

        plt.title("k for fagins")
        plt.plot(list_k, list_times[1], 'go')
        list_k = [x+0.1 for x in list_k]
        plt.plot(list_k, list_times[2], 'bo')
        list_k = [x+0.1 for x in list_k]
        plt.plot(list_k, list_times[3], 'ko')
        plt.show()

        plt.title("e for fagins_e")
        plt.plot(list_e, list_times[3], 'ko')
        plt.show()

        plt.title("lenght results")
        plt.plot(list_results[0], list_times[0], 'ro')
        list_nbterms = [x+0.1 for x in list_results[1]]
        plt.plot(list_results[1], list_times[1], 'go')
        list_nbterms = [x+0.2 for x in list_results[2]]
        plt.plot(list_results[2], list_times[2], 'bo')
        list_nbterms = [x+0.3 for x in list_results[3]]
        plt.plot(list_results[3], list_times[3], 'ko')
        plt.show()


def test_generate():

    times_m = []
    times_b = []
    times_bp = []
    times_tot = []
    batch_sizes = []
    MAX_SIZE = 800000
    BATCH_SIZE = 1
    for BATCH_SIZE in [1000, 10000, 50000, 100000]:
        filename = 'if/'+id_generator()
        print("----------------b------------------")
        print(str(BATCH_SIZE) + ' ' + filename)
        print("----------------bf------------------")

        inverted_file = InvertedFileBuilder(datafolder, filename, map, BATCH_SIZE, STEMMING)

        t1_bp = time.time()
        inverted_file.build_partial()
        t2_bp = time.time()

        t1_m = time.time()
        inverted_file.merge()
        t2_m = time.time()

        times_b.append(t2_bp-t1_bp)
        times_bp.append(t2_bp-t1_bp)
        times_m.append(t2_m-t1_m)
        times_tot.append(t2_m-t1_bp)
        batch_sizes.append(BATCH_SIZE)

    print(str(times_b))
    print(str(times_bp))
    print(str(times_m))
    print(str(times_tot))
    plt.plot(batch_sizes, times_b, 'r')
    plt.plot(batch_sizes, times_bp, 'g')
    plt.plot(batch_sizes, times_m, 'b')
    plt.plot(batch_sizes, times_tot, 'k')
    plt.show()

arg_parser,args,datafolder,filename,map,NbTest, test_algo, test_k, test_epsilon, test_nbterms, test_batch, k_fagins, epsilon, N_terms = test_arg_parser()

bar = progressbar.ProgressBar(maxval=NbTest, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

if test_algo:
    #import cProfile
    #cProfile.run('test_answer()', 'yayaya')
    test_answer()
if test_batch:
    test_generate()
