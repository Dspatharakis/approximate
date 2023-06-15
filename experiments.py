import approximate
import numpy as np
import random
import subprocess
import time 
import csv 

filename = "experiments.csv"
filename_average = "experiments_average.csv"
n = 5
m = 5 
iterations = 10
def main():
    counter = 0 
    start_time = time.time()
    total_cost = 0 
    for i in range (iterations):
        print ("iteration: ", i)
        result = subprocess.run(["python3", "approximate.py"], capture_output=True)
        output = result.stdout.decode().strip()
        print (output)
        try: 
            solution_cost = float(output)
            print("cost of solution", solution_cost)     
            total_cost += solution_cost
            counter += 1
            with open(filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([solution_cost])
        except ValueError:
            print ("Value Error")   
    print ("Averaged over 30 iterations:", total_cost/counter)
    end_time = time.time() - start_time
    print ("execution time:", end_time)
    with open(filename_average, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([total_cost/counter,n,m])
if __name__ == "__main__":
    main()



