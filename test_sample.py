from main import operation_file, init, calculate, op_arg_parser
import random
import time
import pprint
import progressbar
import matplotlib.pyplot as plt

from settings import BATCH_SIZE
from indexing import InvertedFileBuilder

NbTest = 500
bar = progressbar.ProgressBar(maxval=NbTest, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

def test_answer():
    arg_parser,args,datafolder,filename,map = op_arg_parser()
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
    list_times = [[],[],[],[]]

    for k in range(NbTest):
    #while True:
        bar.update(k + 1)
        N = random.randint(1,20)
        terms = []
        N_terms = random.randint(1,5)
        # N_terms = 1
        for i in range(N_terms) :
            terms.append(random.choice(list(inverted_file.inverted_file.keys())))
        #print("-------------ans--------------")
        #print(k)
        #print(terms)
        list_nbterms.append(N_terms)
        list_k.append(N)

        for op_algo in [0,1,2,3]:
            t1 = time.time()
            ans[op_algo] = calculate(op_algo,N,terms,algoF,algoN,algoFT,algoFTE)
            t2 = time.time()
            t[op_algo] = t2 - t1
            #list_times[op_algo].append(t[op_algo])
            #pprint.pprint(ans[op_algo])
            #Sprint(t[op_algo])
        for j in range(len(ans[3])):
            for i in [1,2,3]:
                #assert(ans[i][j].score == ans[0][j].score)
                if ans[i][j].score != ans[0][j].score:
                    print("bad algo...."+str(i)+" "+str(terms))
        rate[1] += t[1]/t[0]
        rate[2] += t[2]/t[0]
        rate[3] += t[3]/t[0]
        list_times[0].append(1)
        list_times[1].append(t[1]/t[0])
        list_times[2].append(t[2]/t[0])
        list_times[3].append(t[3]/t[0])


        #print("-------------ans--------------\n")

    bar.finish()

    print( "Fagins :")
    print( "    " + str(int((1-rate[1]/1000)*100)) + "% acceleration compared with naive algo." )
    print( "Fagins Threshold :")
    print( "    " + str(int((1-rate[2]/1000)*100)) + "% acceleration compared with naive algo." )
    print( "    " + str(int((1-rate[2]/rate[1])*100)) + "% acceleration compared with Fagins." )
    print( "Fagins Threshold With Epsilon:")
    print( "    " + str(int((1-rate[3]/1000)*100)) + "% acceleration compared with naive algo," )
    print( "    " + str(int((1-rate[3]/rate[1])*100)) + "% acceleration compared with Fagins." )
    print( "    " + str(int((1-rate[3]/rate[2])*100)) + "% acceleration compared with Fagins Threshold." )

    plt.subplot(2,1,1)
    plt.title("4 algo")
    plt.plot(list_nbterms, list_times[0], 'ro')
    list_nbterms = [x+0.1 for x in list_nbterms]
    plt.plot(list_nbterms, list_times[1], 'go')
    list_nbterms = [x+0.1 for x in list_nbterms]
    plt.plot(list_nbterms, list_times[2], 'bo')
    list_nbterms = [x+0.1 for x in list_nbterms]
    plt.plot(list_nbterms, list_times[3], 'ko')

    plt.subplot(2,1,2)
    plt.title("k for fagins")
    plt.plot(list_k, list_times[1], 'go')
    list_k = [x+0.1 for x in list_k]
    plt.plot(list_k, list_times[2], 'bo')
    list_k = [x+0.1 for x in list_k]
    plt.plot(list_k, list_times[3], 'ko')
    plt.show()


def test_generate():
    arg_parser,args,datafolder,filename,map = op_arg_parser()
    times_m = []
    times_b = []
    times_bp = []
    times_tot = []
    batch_sizes = []
    MAX_SIZE = 100001
    BATCH_SIZE = 1
    for BATCH_SIZE in range(1, MAX_SIZE, 1000) :
        print("----------------b------------------")
        print(BATCH_SIZE)
        print("----------------bf------------------")

        t1_b = time.time()
        inverted_file = InvertedFileBuilder(datafolder, filename, map)
        t2_b = time.time()

        t1_bp = time.time()
        inverted_file.build_partial()
        t2_bp = time.time()

        t1_m = time.time()
        inverted_file.merge()
        t2_m = time.time()

        times_b.append(t2_b-t1_b)
        times_bp.append(t2_bp-t1_bp)
        times_m.append(t2_m-t1_m)
        times_tot.append(t2_m-t1_b)
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

test_answer()
