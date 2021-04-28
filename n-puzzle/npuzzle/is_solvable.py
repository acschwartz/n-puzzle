EMPTY_TILE = 0
def count_inversions(puzzle, goal_state, size):
    res = 0
    for i in range(size * size - 1):
        for j in range(i + 1, size * size):            
                vi = puzzle[i]
                vj = puzzle[j]
                if goal_state.index(vi) > goal_state.index(vj):
                    res += 1
    return res

def is_solvable(puzzle, goal_state, size):
    inversions = count_inversions(puzzle, goal_state, size)
    puzzle_zero_row = puzzle.index(EMPTY_TILE) // size
    puzzle_zero_column = puzzle.index(EMPTY_TILE) % size
    goal_zero_row = goal_state.index(EMPTY_TILE) // size
    goal_zero_column = goal_state.index(EMPTY_TILE) % size
    taxicab = abs(puzzle_zero_row - goal_zero_row) + abs(puzzle_zero_column - goal_zero_column)
    if taxicab % 2 == 0 and inversions % 2 == 0:
        return True
    if taxicab % 2 == 1 and inversions % 2 == 1:
        return True
    return False
