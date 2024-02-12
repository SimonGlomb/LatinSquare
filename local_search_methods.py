import utils
import random
import math
import numpy as np

def random_strategy(square, number_of_conflicts):
    random_index_replace = random.randint(0, len(square) - 1)
    random_index = random.randint(0, len(square) - 1)
    new_row = utils.fixpoint_free_permutation(square[random_index])
    return random_index_replace, new_row

def derangement_for_lowest_replace_highest_conflicts(square, number_of_conflicts):
    index_of_element_with_lowest_conflicts = utils.select_row_lowest_conflicts(number_of_conflicts)
    index_of_element_with_highest_conflicts = utils.select_row_highest_conflicts(number_of_conflicts)

    new_row = utils.fixpoint_free_permutation(square[index_of_element_with_lowest_conflicts])
    index_to_replace = index_of_element_with_highest_conflicts
    return index_to_replace, new_row

def derangement_for_lowest_random_replace_highest_conflicts(square, number_of_conflicts):
    minimum_el = min(number_of_conflicts)
    indices = [i for i, x in enumerate(number_of_conflicts) if x == minimum_el]
    index_of_element_with_lowest_conflicts = random.choice(indices)

    index_of_element_with_highest_conflicts = utils.select_row_highest_conflicts(number_of_conflicts)

    new_row = utils.fixpoint_free_permutation(square[index_of_element_with_lowest_conflicts])
    index_to_replace = index_of_element_with_highest_conflicts
    return index_to_replace, new_row

def derangement_for_lowest_replace_highest_conflicts_random(square, number_of_conflicts):
    # put in randomness for the ones with many conflicts if the max number is the same for some rows
    index_of_element_with_lowest_conflicts = utils.select_row_lowest_conflicts(number_of_conflicts)
    
    max_indices = [i for i, val in enumerate(number_of_conflicts) if val == max(number_of_conflicts)]
    random_index = random.choice(max_indices)
    index_of_element_with_highest_conflicts = number_of_conflicts.index(number_of_conflicts[random_index])

    index_to_replace = index_of_element_with_highest_conflicts
    new_row = utils.fixpoint_free_permutation(square[index_of_element_with_lowest_conflicts])
    return index_to_replace, new_row

def derangement_for_lowest_random_replace_highest_conflicts_random(square, number_of_conflicts):
    # like idea before, but put in randomness for the ones with many conflicts if the max number is the same for some rows
    minimum_el = min(number_of_conflicts)
    indices = [i for i, x in enumerate(number_of_conflicts) if x == minimum_el]
    index_of_element_with_lowest_conflicts = random.choice(indices)
    
    max_indices = [i for i, val in enumerate(number_of_conflicts) if val == max(number_of_conflicts)]
    random_index = random.choice(max_indices)
    index_of_element_with_highest_conflicts = number_of_conflicts.index(number_of_conflicts[random_index])

    index_to_replace = index_of_element_with_highest_conflicts
    new_row = utils.fixpoint_free_permutation(square[index_of_element_with_lowest_conflicts])
    return index_to_replace, new_row

def lowest_conflict_derangement_neighborhood(square, number_of_conflicts):    
    # Compute derangement for worst row, and then check all rows which to replace with objective function
    index_of_element_with_highest_conflicts = utils.select_row_lowest_conflicts(number_of_conflicts)
    new_row = utils.fixpoint_free_permutation(square[index_of_element_with_highest_conflicts])
    neighbor_score = []
    for i, _ in enumerate(square):
        curr_square = square.copy()
        curr_square[i] = new_row
        neighbor_score.append(utils.compute_number_of_conflicts_row(curr_square, len(square)))
    index_to_replace = neighbor_score.index(min(neighbor_score))
    return index_to_replace, new_row


def derangement_two_worst_solutions(square, number_of_conflicts):
    # compute derangement for worst one and change with second worst one
    second_lowest_value = sorted(set(number_of_conflicts))[1]
    second_lowest_indices = [i for i, val in enumerate(number_of_conflicts) if val == second_lowest_value]
    second_lowest_index = random.choice(second_lowest_indices)
    index_to_replace = second_lowest_index

    index_of_element_with_highest_conflicts = number_of_conflicts.index(number_of_conflicts[second_lowest_index])
    new_row = utils.fixpoint_free_permutation(square[index_of_element_with_highest_conflicts])
    return index_to_replace, new_row


def derangement_two_worst_solutions_random(square, number_of_conflicts):
    # compute derangement for worst one and change with second worst one, random pick

    sorted_conflicts = sorted(set(number_of_conflicts))
    second_highest_value = sorted_conflicts[-2]
    second_highest_indices = [i for i, val in enumerate(number_of_conflicts) if val == second_highest_value]
    
    highest_value = sorted_conflicts[-1]
    highest_indices= [i for i, val in enumerate(number_of_conflicts) if val == highest_value]

    random_index_second = random.choice(second_highest_indices)
    random_index = random.choice(highest_indices)

    index_of_element_with_highest_conflicts = number_of_conflicts.index(number_of_conflicts[random_index])
    
    index_of_element_with_second_highest_conflicts = number_of_conflicts.index(number_of_conflicts[random_index_second])
    new_row = utils.fixpoint_free_permutation(square[index_of_element_with_second_highest_conflicts])

    index_to_replace = index_of_element_with_highest_conflicts
    return index_to_replace, new_row

def most_conflict_derangement_neighborhood(square, number_of_conflicts):
    index_of_element_with_highest_conflicts = utils.select_row_highest_conflicts(number_of_conflicts)
    new_row = utils.fixpoint_free_permutation(square[index_of_element_with_highest_conflicts])
    neighbor_score = []
    for i, _ in enumerate(square):
        curr_square = square.copy()
        curr_square[i] = new_row
        neighbor_score.append(utils.compute_number_of_conflicts_row(curr_square, len(square)))
    index_to_replace = neighbor_score.index(min(neighbor_score))
        
    return index_to_replace, new_row

def most_conflict_derangement_neighborhood_rand1(square, number_of_conflicts):
    # additionally sprinkled in some randomness for which row to compute a derangement for
    index_of_element_with_highest_conflicts = utils.select_row_highest_conflicts(number_of_conflicts)
    if random.random() > 0.5:
        new_row = utils.fixpoint_free_permutation(square[index_of_element_with_highest_conflicts])
    else:
        new_row = new_row = utils.fixpoint_free_permutation(square[random.randint(0,len(square)-1)])
    neighbor_score = []
    for i, _ in enumerate(square):
        curr_square = square.copy()
        curr_square[i] = new_row
        neighbor_score.append(utils.compute_number_of_conflicts_row(curr_square, len(square)))
    index_to_replace = neighbor_score.index(min(neighbor_score))
        
    return index_to_replace, new_row

def most_conflict_derangement_neighborhood_rand2(square, number_of_conflicts):    
    # additionally sprinkled in some randomness for which row to replace (if it is not an improvement)
    index_of_element_with_highest_conflicts = utils.select_row_highest_conflicts(number_of_conflicts)
    new_row = utils.fixpoint_free_permutation(square[index_of_element_with_highest_conflicts])
    neighbor_score = []
    for i, _ in enumerate(square):
        curr_square = square.copy()
        curr_square[i] = new_row
        neighbor_score.append(utils.compute_number_of_conflicts_row(curr_square, len(square)))
    if min(neighbor_score) < utils.compute_number_of_conflicts_row(square, len(square)):
        index_to_replace = neighbor_score.index(min(neighbor_score))
    else:
        index_to_replace = random.randint(0,len(square)-1)
        
    return index_to_replace, new_row

def most_conflict_derangement_neighborhood_rand3(square, number_of_conflicts):    
    # additionally sprinkled in some randomness for which row to compute a derangement for AND which to replace (if it is not an improvement)
    index_of_element_with_highest_conflicts = utils.select_row_highest_conflicts(number_of_conflicts)
    if random.random() > 0.5:
        new_row = utils.fixpoint_free_permutation(square[index_of_element_with_highest_conflicts])
    else:
        new_row = new_row = utils.fixpoint_free_permutation(square[random.randint(0,len(square)-1)])
    neighbor_score = []
    for i, _ in enumerate(square):
        curr_square = square.copy()
        curr_square[i] = new_row
        neighbor_score.append(utils.compute_number_of_conflicts_row(curr_square, len(square)))
    if min(neighbor_score) < utils.compute_number_of_conflicts_row(square, len(square)):
        index_to_replace = neighbor_score.index(min(neighbor_score))
    else:
        index_to_replace = random.randint(0,len(square)-1)
        
    return index_to_replace, new_row


def rand_derangement_neighborhood(square, number_of_conflicts):    
    # Use random row to compute derangement
    index_to_compute_derangement = random.randint(0, len(square)-1)
    new_row = utils.fixpoint_free_permutation(square[index_to_compute_derangement])
    neighbor_score = []
    for i, _ in enumerate(square):
        curr_square = square.copy()
        curr_square[i] = new_row
        neighbor_score.append(utils.compute_number_of_conflicts_row(curr_square, len(square)))
    index_to_replace = neighbor_score.index(min(neighbor_score))
    return index_to_replace, new_row

def all_possible_derangements(square, number_of_conflicts):
    # The idea is to have a very huge neighborhood O(n^2) for both, the row generated (derangement) and the row to replace
    curr_best_row = [i for i in range(0, len(square))]
    curr_best_score = math.inf
    curr_best_index = random.randint(0,len(square)-1)
    for curr_best_index_to_compute_derangement in range(len(square)):
        curr_new_row = utils.fixpoint_free_permutation(square[curr_best_index_to_compute_derangement])
        for i, _ in enumerate(square):
            curr_square = square.copy()
            curr_square[i] = curr_new_row
            curr_score = utils.compute_objective_function(utils.compute_number_of_conflicts_row(curr_square, len(square)))
            if curr_best_score > curr_score:
                curr_best_score = curr_score
                curr_best_index = i
                curr_best_row = curr_new_row
    return curr_best_index, curr_best_row

def all_possible_rand(square, number_of_conflicts):
    # The idea is to have a very huge neighborhood O(n^2) for both, the row generated and the row to replace but pick new row at random and not as derangement
    curr_best_row = [i for i in range(0, len(square))]
    curr_best_score = math.inf
    curr_best_index = random.randint(0,len(square)-1)
    for _ in range(len(square)):
        curr_new_row = random.sample(range(1, len(square)+1), len(square))
        for i, _ in enumerate(square):
            curr_square = square.copy()
            curr_square[i] = curr_new_row
            curr_score = utils.compute_objective_function(utils.compute_number_of_conflicts_row(curr_square, len(square)))
            if curr_best_score > curr_score:
                curr_best_score = curr_score
                curr_best_index = i
                curr_best_row = curr_new_row
    return curr_best_index, curr_best_row

def all_possible_derangements_swap(square, number_of_conflicts):
    # Idea similar to all_possible_derangements, but swap an element that makes problems
    curr_best_row = [i for i in range(0, len(square))]
    curr_best_score = math.inf
    curr_best_index = random.randint(0,len(square)-1)
    for curr_best_index_to_compute_derangement in range(len(square)):
        if random.random() > 0.5:
            curr_new_row = utils.fixpoint_free_permutation(square[curr_best_index_to_compute_derangement])
            for i, _ in enumerate(square):
                curr_square = square.copy()
                curr_square[i] = curr_new_row
                curr_score = utils.compute_objective_function(utils.compute_number_of_conflicts_row(curr_square, len(square)))
                if curr_best_score > curr_score:
                    curr_best_score = curr_score
                    curr_best_index = i
                    curr_best_row = curr_new_row
        else:
            row_to_cols = utils.compute_rows_with_more_than_one_conflict_in_cols(square)
            if len(row_to_cols) <= 0:
                curr_square = square.copy()
                # if there are no rows which have common fixable columns
                curr_square[random.randint(0, len(square)-1), :], curr_square[random.randint(0, len(square)-1), :] = curr_square[random.randint(0, len(square)-1), :], curr_square[random.randint(0, len(square)-1), :]
            else:
                for row, col_list in row_to_cols.items():
                    curr_square = square.copy()
                    rand_col1 = random.randint(0, len(col_list)-1)
                    rand_col2 = random.randint(0, len(col_list)-1)
                    # TODO optimieren das rand_col1 != rand_col2
                    curr_square[row, col_list[rand_col1]], curr_square[row, col_list[rand_col2]] = curr_square[row, col_list[rand_col2]], curr_square[row, col_list[rand_col1]]

                    curr_score = utils.compute_objective_function(utils.compute_number_of_conflicts_row(curr_square, len(square)))
                    if curr_best_score > curr_score:
                        curr_best_score = curr_score
                        curr_best_index = row
                        curr_best_row = curr_square[row, :]

    return curr_best_index, curr_best_row

def all_possible_derangements_shuffle(square, number_of_conflicts):
    # Idea similar to all_possible_derangements, but shuffle a row that makes problems
    curr_best_row = [i for i in range(0, len(square))]
    curr_best_score = math.inf
    curr_best_index = random.randint(0,len(square)-1)
    for curr_best_index_to_compute_derangement in range(len(square)):
        if random.random() > 0.5:
            curr_new_row = utils.fixpoint_free_permutation(square[curr_best_index_to_compute_derangement])
            for i, _ in enumerate(square):
                curr_square = square.copy()
                curr_square[i] = curr_new_row
                curr_score = utils.compute_objective_function(utils.compute_number_of_conflicts_row(curr_square, len(square)))
                if curr_best_score > curr_score:
                    curr_best_score = curr_score
                    curr_best_index = i
                    curr_best_row = curr_new_row
        else:
            row_to_cols = utils.compute_rows_with_more_than_one_conflict_in_cols(square)
            for row, col_list in row_to_cols.items():
                curr_square = square.copy()
                np.random.shuffle(curr_square[row])
                # TODO optimieren das rand_col1 != rand_col2
                curr_best_index = row
                curr_best_row = curr_square[row, :]

    return curr_best_index, curr_best_row
