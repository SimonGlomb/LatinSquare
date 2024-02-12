import utils
import numpy as np

def test_compute_number_of_conflicts_row():
    square = [[1,2,3], [1,2,3], [1,2,3]]
    result = utils.compute_number_of_conflicts_row(square, len(square))
    assert result == [0,3,3]

    square = [[2,1,3], [1,2,3], [1,2,3]]
    result = utils.compute_number_of_conflicts_row(square, len(square))
    assert result == [0, 1, 3]
    
    square = [[1,2,3], [3,1,2], [2,3,1]]
    result = utils.compute_number_of_conflicts_row(square, len(square))
    assert result == [0, 0, 0]
    
def test_compute_map_column_to_conflicting_rows():
    square = np.array([[1,2,3,4,5], [2,3,4,5,1], [3,4,5,1,2], [4,5,1,3,2], [5,1,2,3,4]])
    
    result = utils.compute_rows_with_more_than_one_conflict_in_cols(square)
    print(result)
    assert result == {3: [3, 4]}

def test_create_list_with_constraints():    
    n = 10
    # value is the position
    # key is the numbers not allowed
    constraints = {4: [3, 4], 6: [8]}

    for _ in range(100):
        arr = utils.create_restart_with_constraints(n, constraints)
        assert arr[4] != 3
        assert arr[4] != 4
        assert arr[6] != 8


if __name__ == '__main__':
    test_compute_number_of_conflicts_row
    test_compute_map_column_to_conflicting_rows()
    test_create_list_with_constraints()