from random import shuffle
import matplotlib.pyplot as plt
import random 
import numpy as np

def visualize_scalability(computation_times, derangement_strategies_row, sizes_n, metaheuristic):
    for strategy_row in derangement_strategies_row:
        plt.plot(computation_times[strategy_row], label=f'{getattr(strategy_row, "__name__")}')
        plt.xlabel('Size n of the Latin square')
        plt.ylabel('Time needed to compute')
        plt.xticks(range(len(computation_times[strategy_row])), sizes_n)
        plt.title(f'Local Search for Latin square with sizes {sizes_n} using {metaheuristic}')
        plt.legend()
    plt.show()
    plt.savefig(f'./report/performance-images/performance{metaheuristic}.png')

def visualize(all_sum_number_of_conflicts, strategy_row, n, metaheuristic):
    plt.plot(all_sum_number_of_conflicts, label=f'{getattr(strategy_row, "__name__")}')
    plt.xlabel('Number of Steps')
    plt.ylabel('Number of Conflicts')
    plt.title(f'Local Search for Latin square with size {n} using {metaheuristic}')
    plt.legend()
    plt.savefig(f'./report/images/{getattr(strategy_row, "__name__")}.png')

def fixpoint_free_permutation(lst):
    n = len(lst)
    while True:
        perm = lst.copy()
        shuffle(perm)
        if all(perm[i] != lst[i] for i in range(n)):
            return perm

def swap_elements(lst, i):
    # Get a random index j that is different from i
    j = random.choice([x for x in range(len(lst)) if x != i])
    # Swap the elements at positions i and j
    lst[i], lst[j] = lst[j], lst[i]
    return lst

def compute_map_column_to_conflicting_rows(square):
    n = len(square)
    number_already_seen = [0 for _ in range(n)]
    # maps column to conflict row-indices
    col_to_conflict_row_indices = {j: [] for j in range(0,n)}
    for j in range(0, n):
        for i in range(0, n):
            # index minus 1, because e.g. number 1 is at index 0
            if number_already_seen[square[i][j] - 1] == 1:
                col_to_conflict_row_indices[j].append(i)
            else: 
                number_already_seen[square[i][j] - 1] = 1
        for k in range(0, n):
            number_already_seen[k] = 0
    for k in range(0,n):
        if len(col_to_conflict_row_indices[k]) > 0:
            indices = np.where(square[:, k] == square[col_to_conflict_row_indices[k][0], k])[0]
            col_to_conflict_row_indices[k] = indices
    return col_to_conflict_row_indices

def compute_rows_with_more_than_one_conflict_in_cols(square):
    """
    Returns the row as key and the cols with conflicts as a list 
    """
    result = compute_map_column_to_conflicting_rows(square)
    sets = [set(result[i].tolist()) for i in result if isinstance(result[i], (np.ndarray))]
    def get_keys_with_value(dictionary, value):
        return [key for key, val in dictionary.items() if value in val]
    common_rows = set.intersection(*sets)
    rows_and_conflicting_cols = {}
    for row in common_rows:
        rows_and_conflicting_cols[row] = (get_keys_with_value(result, row))
    return rows_and_conflicting_cols


def fixpoint_free_permutation_prob(permutation):
    """
    Computes the fixpoint-free permutation of a given permutation.
    """
    from itertools import permutations
    from math import factorial
    n = len(permutation)
    count = 0
    for p in permutations(permutation):
        for i in range(n):
            if p[i] == permutation[i]:
                break
        else:
            count += 1
    return count / factorial(n)

def compute_objective_function(number_of_conflicts):
    return sum(number_of_conflicts)

# computes number of conflicts for each row: in how many column conflicts is this row
# "how many entries in this row make problems as there is another row with this entry"
def compute_number_of_conflicts_row(square, n):
    # tells which number in [n] has already been seen for a certain column
    number_already_seen = [0 for _ in range(n)]
    # tells how many conflicts a certain row has
    number_of_conflicts = [0 for _ in range(n)]
    for j in range(0, n):
        for i in range(0, n):
            # index minus 1, because e.g. number 1 is at index 0
            if number_already_seen[square[i][j] - 1] == 1:
                number_of_conflicts[i] +=1
            else: 
                number_already_seen[square[i][j] - 1] = 1
        for k in range(0, n):
            number_already_seen[k] = 0
    return number_of_conflicts

def compute_number_of_conflicts_row_more_detail(square, n):
    # tells which number in [n] has already been seen for a certain column
    number_already_seen = [0 for _ in range(n)]
    # To account for conflicts as a symmetric relation: i.e. without this the row with first conflicts does not have any conflicts
    col_where_number_has_been_seen_first = [None for _ in range(n)]
    # tells how many conflicts a certain row has
    number_of_conflicts = [0 for _ in range(n)]
    for j in range(0, n):
        for i in range(0, n):
            # index minus 1, because e.g. number 1 is at index 0
            if number_already_seen[square[i][j] - 1] == 1:
                number_of_conflicts[j] +=1
            else: 
                number_already_seen[square[i][j] - 1] = 1
                col_where_number_has_been_seen_first[square[i][j] - 1] = j
        for k in range(0, n):
            number_already_seen[k] = 0
    for k in range(0, n):
        if col_where_number_has_been_seen_first[k] != None and number_of_conflicts[k] > 0:
            number_of_conflicts[col_where_number_has_been_seen_first[k]] += 1
    return number_of_conflicts

# computes number of conflicts for each col
def compute_number_of_conflicts_col(square, n):
    # tells which number in [n] has already been seen for a certain column
    number_already_seen = [0 for _ in range(n)]
    # tells how many conflicts a certain col has
    number_of_conflicts = [0 for _ in range(n)]
    for i in range(0, n):
        for j in range(0, n):
            # index minus 1, because e.g. number 1 is at index 0
            if number_already_seen[square[i][j] - 1] == 1:
                number_of_conflicts[j] +=1
            else: 
                number_already_seen[square[i][j] - 1] = 1
        for k in range(0, n):
            number_already_seen[k] = 0
    return number_of_conflicts

# index_of_element_with_lowest_conflicts
def select_row_lowest_conflicts(number_of_conflicts):
    return number_of_conflicts.index(min(number_of_conflicts))

# index_of_element_with_highest_conflicts
def select_row_highest_conflicts(number_of_conflicts):
    return number_of_conflicts.index(max(number_of_conflicts))

def select_col_highest_conflicts(number_of_conflicts):
    return number_of_conflicts.index(max(number_of_conflicts))

def create_restart_with_constraints_naive(n, constraints):
    arr = np.random.permutation(n) + 1
    for key, value in constraints.items():
        # have to loop
        # if it would not loop, it could happen that we swap two elements which both would be in "value"
        # PROBLEM WITH LOOP: it happens that it swaps two value back and forth and i stuck in the while loop
        # SO THIS METHOD IS NOT USEFUL AND CANNOT BE USED
        while arr[key] in value:
            #pick a random index to swap with
            available_numbers = set(arr) - set(value)
            idx = np.random.choice(list(available_numbers)) - 1
            arr[key], arr[idx] = arr[idx], arr[key]
    return arr.tolist()

def create_restart_with_constraints_not_efficient(n, constraints):
    for key, value in constraints.items():
        arr = np.random.permutation(n) + 1
        # have to loop
        # if it would not loop, it could happen that we swap two elements which both would be in "value"
        # put random array generation inside while loop
        while arr[key] in value:
            arr = np.random.permutation(n) + 1
            #pick a random index to swap with
            available_numbers = set(arr) - set(value)
            idx = np.random.choice(list(available_numbers)) - 1
            arr[key], arr[idx] = arr[idx], arr[key]
    return arr.tolist()

def create_restart_with_constraints_recursion(n, constraints_dict):
    all_possible_numbers = range(1, n+1)
    arr = np.random.permutation(n) + 1
    already_used_in_this_row = set()
    for col, constraints in constraints_dict.items():
        available_numbers = set(all_possible_numbers) - set(constraints) - already_used_in_this_row
        # if available numbers is empty, we already made a mistake by picking something wrong in this row
        # call function recursively to make these choices again
        if available_numbers == set() and len(constraints)<n-1:
            return create_restart_with_constraints_recursion(n, constraints_dict)
        arr[col] = np.random.choice(np.array(list(available_numbers)))
        if len(available_numbers) == 1:
            arr[col] = list(available_numbers)[0]
        already_used_in_this_row.add(arr[col])
    return arr.tolist()

def create_restart_with_constraints(n, constraints_dict):
    while True:
        all_possible_numbers = range(1, n+1)
        arr = np.random.permutation(n) + 1
        already_used_in_this_row = set()
        for col, constraints in constraints_dict.items():
            available_numbers = set(all_possible_numbers) - set(constraints) - already_used_in_this_row
            # if available numbers is empty, we already made a mistake by picking something wrong in this row
            # call function recursively to make these choices again
            if available_numbers == set() and len(constraints)<n-1:
                break
            arr[col] = np.random.choice(np.array(list(available_numbers)))
            if len(available_numbers) == 1:
                arr[col] = list(available_numbers)[0]
            already_used_in_this_row.add(arr[col])
        else:
            return arr.tolist()
