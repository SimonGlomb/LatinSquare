import pymzn
import time

values = [5, 10, 15, 20]
with open('results.txt', 'w') as file:
    for n in values:
        data = {"n": n}
        start_time = time.time()
        solutions = pymzn.minizinc('latin_square.mzn', all_solutions=False, data=data, solver=pymzn.Chuffed())
        end_time = time.time()
        computation_time = end_time - start_time
        print(computation_time)
        file.write(f'n = {n}, time = {computation_time:.2f} seconds\n')
        print(solutions)
print('Results saved to results.txt')
