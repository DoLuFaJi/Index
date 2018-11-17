from main import operation_file, init, calculate, op_arg_parser
import random
import time
import pprint
import progressbar

NbTest = 1000
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

        for op_algo in [0,2,3]:
            t1 = time.time()
            ans[op_algo] = calculate(op_algo,N,terms,algoF,algoN,algoFT,algoFTE)
            t2 = time.time()
            t[op_algo] = t2 - t1
            #pprint.pprint(ans[op_algo])
            #Sprint(t[op_algo])
        for j in range(len(ans[3])):
            for i in [2,3]:
                assert(ans[i][j].score == ans[0][j].score)
        rate[2] += t[2]/t[0]
        rate[3] += t[3]/t[0]

        #print("-------------ans--------------\n")

    bar.finish()

    print( "Fagins Threshold :")
    print( "    " + str(int((1-rate[2]/1000)*100)) + "% acceleration compared with naive algo." )
    print( "Fagins Threshold With Epsilon:")
    print( "    " + str(int((1-rate[3]/1000)*100)) + "% acceleration compared with naive algo," )
    print( "    " + str(int((1-rate[3]/rate[2])*100)) + "% acceleration compared with Fagins Threshold." )

test_answer()
