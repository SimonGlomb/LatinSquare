import utils
import random
import numpy as np
import math
from visualize_matrix import visualize_matrix, visualize_matrix_row_color

def metaheuristic(square, n, iterations, local_search_strategy):
    all_sum_number_of_conflicts = []
    n_iter = 0
    curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
    while sum(curr_number_of_conflicts_row) != 0 and n_iter < iterations:
        n_iter += 1

        index_to_replace, new_row = local_search_strategy(square, curr_number_of_conflicts_row)

        # The step which adjusts the square
        square[index_to_replace] = new_row

        curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
        sum_number_of_conflicts = utils.compute_objective_function(curr_number_of_conflicts_row)
        all_sum_number_of_conflicts.append(sum_number_of_conflicts)
    return square, all_sum_number_of_conflicts, n_iter

def metaheuristic_SA(square, n, iterations, derangement_strategy):
    all_sum_number_of_conflicts = []
    n_iter = 0
    temperature = 1000
    cooling_rate = 0.005
    curr_number_of_conflicts = utils.compute_number_of_conflicts_row(square, n)
    while temperature > 1 and curr_number_of_conflicts != [0 for _ in range(n)]:
        n_iter += 1

        index_of_element_with_highest_conflicts = utils.select_row_highest_conflicts(curr_number_of_conflicts)
        new_row = utils.fixpoint_free_permutation(square[index_of_element_with_highest_conflicts])
        neighbor_score = []
        for i, _ in enumerate(square):
            curr_square = square.copy()
            curr_square[i] = new_row
            neighbor_score.append(utils.compute_objective_function(utils.compute_number_of_conflicts_row(curr_square, len(square))))
        objective_function_difference = min(neighbor_score) - utils.compute_objective_function(utils.compute_number_of_conflicts_row(square, len(square)))
        index_to_replace = neighbor_score.index(min(neighbor_score))
        if objective_function_difference > 0:
            square[index_to_replace] = new_row
        else:
            acceptance_probability = math.exp(-objective_function_difference / temperature)
            if random.random() < acceptance_probability:
                square[index_to_replace] = new_row
        temperature *= 1 - cooling_rate

        curr_number_of_conflicts = utils.compute_number_of_conflicts_row(square, n)
        sum_number_of_conflicts = utils.compute_objective_function(curr_number_of_conflicts)
        all_sum_number_of_conflicts.append(sum_number_of_conflicts)
    return square, all_sum_number_of_conflicts, n_iter


def metaheuristic_random_restart(square, n, iterations, derangement_strategy):
    all_sum_number_of_conflicts = []
    n_iter = 0
    curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
    while sum(curr_number_of_conflicts_row) != 0 and n_iter < iterations:
        n_iter += 1

        # here restart happens every 100 iterations, does generate a new random row for all the rows which have at least one conflict
        if n_iter % 100 == 0:
            cnt = 0
            for row, conflicts in enumerate(curr_number_of_conflicts_row):
                if conflicts > 0:
                    cnt += 1
                    square[row] = np.array([random.sample(range(1, n+1), n)])
            #print("number of rows which have been restarted")
            with open(f"results_random_observation.txt", "a") as file:
                file.write("Number of Conflicting Rows:" + str(cnt) + "\n")
            #print("Number of Conflicting Rows:" + str(cnt))


        index_to_replace, new_row = derangement_strategy(square, curr_number_of_conflicts_row)

        # The step which adjusts the square
        square[index_to_replace] = new_row

        curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
        sum_number_of_conflicts = utils.compute_objective_function(curr_number_of_conflicts_row)
        all_sum_number_of_conflicts.append(sum_number_of_conflicts)
    return square, all_sum_number_of_conflicts, n_iter




def metaheuristic_shuffle(square, n, iterations, derangement_strategy_row):
    def shuffle_two_elements_in_row_for_col_duplicate(square, number_of_conflicts):
        max_element = max(number_of_conflicts)
        indices = [i for i, x in enumerate(number_of_conflicts) if x == max_element]
        col = random.choice(indices)
        for row in range(len(square)):
            for i in range(len(square)):
                if square[i][col] != square[row][col]:
                    square[row], square[i] = square[i], square[row]
                    return square
        return square
    all_sum_number_of_conflicts = []
    n_iter = 0
    curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
    curr_number_of_conflicts_col = utils.compute_number_of_conflicts_col(square, n)
    curr_number_of_conflicts = curr_number_of_conflicts_row + curr_number_of_conflicts_col
    while sum(curr_number_of_conflicts_row) != 0 and n_iter < iterations:
        n_iter += 1
        if random.random() > 0.5:
        #if curr_number_of_conflicts_row > curr_number_of_conflicts_col:
            index_to_replace, new_row = derangement_strategy_row(square, curr_number_of_conflicts_row)
            square[index_to_replace] = new_row
        else:
            square = shuffle_two_elements_in_row_for_col_duplicate(square, curr_number_of_conflicts_col)
            #index_to_replace, new_column = derangement_strategy_col(square, curr_number_of_conflicts_col)
            #square[:, index_to_replace] = new_column

        curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
        curr_number_of_conflicts_col = utils.compute_number_of_conflicts_col(square, n)
        curr_number_of_conflicts = curr_number_of_conflicts_row + curr_number_of_conflicts_col

        sum_number_of_conflicts = utils.compute_objective_function(curr_number_of_conflicts)
        all_sum_number_of_conflicts.append(sum_number_of_conflicts)
    return square, all_sum_number_of_conflicts, n_iter

def tabu_search(square, n, iterations, derangement_strategy):
    all_sum_number_of_conflicts = []
    n_iter = 0
    curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
    while sum(curr_number_of_conflicts_row) != 0 and n_iter < iterations:
        n_iter += 1

        # here restart happens every 100 iterations, does generate a new random row for all the rows which have at least one conflict

        if n_iter % 100 == 0:
            constraints_dict = {i: [] for i in range(0, n)}                
            for row, conflicts in enumerate(curr_number_of_conflicts_row):
                if conflicts == 0:
                    for col in range(0, n):
                        constraints_dict[col].append(square[row][col])
            cnt = 0
            for row, conflicts in enumerate(curr_number_of_conflicts_row):
                if conflicts > 0:
                    cnt += 1
                    square[row] = utils.create_restart_with_constraints(n, constraints_dict)  
            curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
            sum_number_of_conflicts = utils.compute_objective_function(curr_number_of_conflicts_row)
            all_sum_number_of_conflicts.append(sum_number_of_conflicts)
            print("number of rows which have been restarted")
            print(cnt)
            if sum(curr_number_of_conflicts_row) == 0:
                break
        else:
            index_to_replace, new_row = derangement_strategy(square, curr_number_of_conflicts_row)

            # The step which adjusts the square
            square[index_to_replace] = new_row

            curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
            sum_number_of_conflicts = utils.compute_objective_function(curr_number_of_conflicts_row)
            all_sum_number_of_conflicts.append(sum_number_of_conflicts)
    return square, all_sum_number_of_conflicts, n_iter

def only_tabu_search(square, n, iterations, derangement_strategy):
    # derangement strategy is ignored
    all_sum_number_of_conflicts = []
    n_iter = 0
    curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
    while sum(curr_number_of_conflicts_row) != 0 and n_iter < iterations:
        n_iter += 1
        # Do check for the constraints in every iteration; do not use a derangement strategy
        constraints_dict = {i: [] for i in range(0, n)}                
        for row, conflicts in enumerate(curr_number_of_conflicts_row):
            if conflicts == 0:
                for col in range(0, n):
                    constraints_dict[col].append(square[row][col])
        number_of_rows_with_conflicts = 0
        print("VISUALIZE MATRIX")
        print(constraints_dict)
        visualize_matrix_row_color(square, curr_number_of_conflicts_row)
        
        for row, conflicts in enumerate(curr_number_of_conflicts_row):
            if conflicts > 0:
                number_of_rows_with_conflicts += 1
                square[row] = utils.create_restart_with_constraints(n, constraints_dict)  

        curr_number_of_conflicts_row = utils.compute_number_of_conflicts_row(square, n)
        sum_number_of_conflicts = utils.compute_objective_function(curr_number_of_conflicts_row)
        all_sum_number_of_conflicts.append(sum_number_of_conflicts)
        print("number of rows which have been restarted")
        print(number_of_rows_with_conflicts)
        if sum(curr_number_of_conflicts_row) == 0:
            break

    return square, all_sum_number_of_conflicts, n_iter