import sum_approximate
import numpy as np
import random
import subprocess
import time 
import csv
import cvxpy 

filename = "experiments.csv"
filename_average = "experiments_average.csv"
modes = [
# "local_offloading",
# "remote_offloading_random_compression",
# "remote_offloading_decide_compression",
# "random_offloading_random_compression",
# "random_offloading_decide_compression",
# "sdr_offloading_random_compression",
# "convex_offloading_decide_compression",
"sdr_offloading_decide_compression",
#"brute_force",
]

Lmax = 0.6 # 0.3 #seconds
Amin = 0.7 #0.7 
Lmax = 0.8 # 0.3 #seconds
Amin = 0.6 #0.7 
iterationss = 1

def main():
    iterations = [1,10,20,30,40,50,100,150,200,300,400,500]
    iterations = [400]
    nlist = [40]#,60,70]
    # nlist = [40]
    mlist = [5]
    seed = [(random.randint(1, 100)) for i in range(10)]
    seed = [99, 68, 5, 28, 47, 79, 23, 90, 93, 39]
    # R = [[0.1,0.5],[1,2],[5,10],[10,20]]

    # R = [[5,10],[10,20]]
    R = [[5,10]]
    bmax = [[5,4],[4,3],[3,2],[2,1],[1,0.5]]
    bmax = [[3,2]]
    alpha = [0.5,1,2]
    # alpha = [1]
    print (seed) 
    with open(filename_average, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([seed])
    for mode in modes:
        for m in mlist:
            for r in R:
                for n in nlist:
                    for itera in iterations:
                        for b in bmax:
                            for a in alpha: 
                                experiment(seed,n,m,mode,Lmax,Amin,itera,r,a,b)

def experiment(seed,n,m,mode,Lmax,Amin,itera,r,a,b): 
    counter = 0 
    start_time = time.time()
    total_cost = 0 
    total_latency = 0 
    total_accuracy = 0 
    total_trans = 0 
    total_comp = 0 
    sum_offloaded_ratio = 0 
    for i in range (iterationss):
        #seed = random.randint(0,1000)
        print ("iteration: ", i)
        print (n,m,mode)
        #temp2 = []
        #temp2.append(seed[0])
        for se in seed: 
            try: 
                #seed = random.randint(0,1000)
                result, Lfinal,Afinal, Ltrans, Lcomp, offloaded_ratio = sum_approximate.main(n,m,se,mode,Lmax,Amin,itera,r,a,b)
                try: 
                    solution_cost = float(result)
                    print("cost of solution", solution_cost)  
                    print ("\n\n\n\n")
   
                    total_cost += solution_cost
                    total_latency += Lfinal
                    total_accuracy += Afinal
                    total_trans += Ltrans
                    total_comp += Lcomp
                    sum_offloaded_ratio += offloaded_ratio
                    counter += 1
                    with open(filename, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([solution_cost])
                except (ValueError,IndexError):
                    print ("Value Error")   
            except (cvxpy.error.SolverError):
                print ("Solver Error")  
    print ("Averaged over iterations:", total_cost/counter)
    end_time = time.time() - start_time
    print ("execution time:", end_time)
    with open(filename_average, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([total_cost/counter,total_latency/counter,total_trans/counter, total_comp/counter, total_accuracy/counter,sum_offloaded_ratio/counter,n,m,mode,itera,r,a,b])
    


if __name__ == "__main__":
    main()


