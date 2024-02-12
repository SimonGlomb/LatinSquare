import time
import random
import sys
import numpy as np
import utils
import argparse

import local_search_methods
import metaheuristics
from visualize_matrix import visualize_matrix, visualize_matrix_row_color

def compute_latin_square(n, n_iter, derangement_strategy_row, metaheuristic):
    square = np.array([random.sample(range(1, n+1), n) for _ in range(n)])
    iterations = n_iter
    square, all_sum_number_of_conflicts, n_iter = metaheuristic(square, n, iterations, derangement_strategy_row)

    return all_sum_number_of_conflicts, square, n, n_iter

#derangement_strategies = [random_strategy, idea_1, idea_2, idea_5, most_conflict_derangement_neighborhood, most_conflict_derangement_neighborhood_rand]

derangement_strategies_row = [local_search_methods.derangement_for_lowest_replace_highest_conflicts]

#derangement_strategies_row = [lowest_conflict_derangement_neighborhood, 
#most_conflict_derangement_neighborhood, idea_1]#, all_possible_derangements_rand, all_possible_derangements_swap, all_possible_derangements_shuffle] # use only one strategy, it does not matter which one if you choose metaheuristic_SA, as it doesnt use the strategy
#derangement_strategies_row = [random_strategy, most_conflict_derangement_neighborhood, all_possible_derangements]#, all_possible_derangements_rand, all_possible_derangements_swap, all_possible_derangements_shuffle] # use only one strategy, it does not matter which one if you choose metaheuristic_SA, as it doesnt use the strategy
#derangement_strategies_row = [random_strategy, most_conflict_derangement_neighborhood, most_conflict_derangement_neighborhood_rand1, most_conflict_derangement_neighborhood_rand2, most_conflict_derangement_neighborhood_rand3] # use only one strategy, it does not matter which one if you choose metaheuristic_SA, as it doesnt use the strategy


# EXPERIMENT 1: 
#derangement_strategies_row = [local_search_methods.random_strategy, local_search_methods.derangement_for_lowest_replace_highest_conflicts, local_search_methods.derangement_for_lowest_random_replace_highest_conflicts, local_search_methods.derangement_for_lowest_replace_highest_conflicts_random, local_search_methods.derangement_for_lowest_random_replace_highest_conflicts_random]
metaheuristic_index = 0

# EXPERIMENT 2: 
#derangement_strategies_row  = [local_search_methods.random_strategy, local_search_methods.derangement_for_lowest_random_replace_highest_conflicts,  local_search_methods.lowest_conflict_derangement_neighborhood]

# Experiment 3:
#derangement_strategies_row  = [local_search_methods.random_strategy, local_search_methods.derangement_for_lowest_random_replace_highest_conflicts,  local_search_methods.lowest_conflict_derangement_neighborhood, local_search_methods.derangement_two_worst_solutions, local_search_methods.derangement_two_worst_solutions_random]

# Experiment 4:
#derangement_strategies_row  = [local_search_methods.random_strategy, local_search_methods.most_conflict_derangement_neighborhood, local_search_methods.most_conflict_derangement_neighborhood_rand1, local_search_methods.most_conflict_derangement_neighborhood_rand2, local_search_methods.most_conflict_derangement_neighborhood_rand3,local_search_methods.lowest_conflict_derangement_neighborhood]

# Experiment 5:

derangement_strategies_row  = [local_search_methods.random_strategy, local_search_methods.lowest_conflict_derangement_neighborhood, local_search_methods.most_conflict_derangement_neighborhood, local_search_methods.all_possible_derangements, local_search_methods.all_possible_rand, local_search_methods.all_possible_derangements_shuffle, local_search_methods.all_possible_derangements_swap]

# Metaheuristics Experiment 0:
derangement_strategies_row  = [local_search_methods.random_strategy, local_search_methods.derangement_for_lowest_random_replace_highest_conflicts_random, local_search_methods.lowest_conflict_derangement_neighborhood, local_search_methods.all_possible_derangements]
metaheuristic_index = 0

# Metaheuristics Experiment 1:
derangement_strategies_row  = [local_search_methods.random_strategy, local_search_methods.derangement_for_lowest_random_replace_highest_conflicts_random, local_search_methods.lowest_conflict_derangement_neighborhood, local_search_methods.all_possible_derangements]
metaheuristic_index = 1


# Metaheuristics Experiment 2:


# Metaheuristics Experiment 3:
derangement_strategies_row  = [local_search_methods.most_conflict_derangement_neighborhood, local_search_methods.all_possible_derangements]
metaheuristic_index = 3


# Metaheuristics Experiment 4:
#metaheuristic_index = 4


# Metaheuristics Experiment 5:
def tabu_strategy():
    return
derangement_strategies_row  = [tabu_strategy]
metaheuristic_index = 5


#### TEMP
#derangement_strategies_row  = [local_search_methods.derangement_for_lowest_random_replace_highest_conflicts]
#metaheuristic_index = 0
#def SA_strategy():
    #return
#derangement_strategies_row  = [SA_strategy]
#metaheuristic_index = 1

# Possible Metaheuristics
metaheuristics = [metaheuristics.metaheuristic, metaheuristics.metaheuristic_SA, metaheuristics.metaheuristic_shuffle, metaheuristics.metaheuristic_random_restart, metaheuristics.tabu_search, metaheuristics.only_tabu_search]

parser = argparse.ArgumentParser(description='Latin Square Generator')

parser.add_argument('--n_iter', type=int,
                    help='Maximum number of iterations')

parser.add_argument('--n', type=int, nargs='+', help='Sizes of Latin square to generate')
args = parser.parse_args()

sizes_n = args.n
n_iter_max=args.n_iter

with open(f'results_fixpoint.txt', 'w') as file:
    computation_times = {strategy_row: [] for strategy_row in derangement_strategies_row}
    for n in sizes_n:
        for strategy_row in derangement_strategies_row:
            start_time = time.time()
            all_sum_number_of_conflicts, square, n, n_iter= compute_latin_square(n, n_iter_max, strategy_row, metaheuristics[metaheuristic_index])
            end_time = time.time()
            if utils.compute_number_of_conflicts_row(square, n) != [0 for _ in range(n)]:
                    print(f"Global Optimum NOT found! Search ended after {n_iter} Iterations.")
            else:
                print(f"Found a Global Optimum! Search ended after {n_iter} Iterations.")
            print("Objective Function Value in the end: ")
            if len(all_sum_number_of_conflicts) == 0:
                #there were no conflicts, randomly generated was a solution already, just an edge case
                print("0")
            else:
                print(all_sum_number_of_conflicts[-1])
            computation_time = end_time - start_time
            computation_times[strategy_row].append(computation_time)
            print(f"Computation time: {computation_time}")
            file.write(f'Metaheuristic: {getattr(metaheuristics[metaheuristic_index], "__name__")} Local Search Strategy: {getattr(strategy_row, "__name__")}, n = {n}, time = {computation_time:.2f} seconds\n')

            #print(square)
            utils.visualize(all_sum_number_of_conflicts, strategy_row, n, getattr(metaheuristics[metaheuristic_index], "__name__"))
        curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
        visualize_matrix_row_color(square, curr_number_of_conflicts_row)
        #visualize_matrix(square)
    utils.visualize_scalability(computation_times, derangement_strategies_row, sizes_n, getattr(metaheuristics[metaheuristic_index], "__name__"))


