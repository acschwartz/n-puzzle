from npuzzle import goal_states
from npuzzle.pdb import pdb
from npuzzle.pdb.eightpuzzle.full8puzzle import full8puzzle

def uniform_cost(puzzle, goal_state, size, db=None):
    return 0

def hamming(candidate, goal_state, size, db=None): #aka tiles out of place
    res = 0
    for i in range(size*size):
        if candidate[i] != 0 and candidate[i] != goal_state[i]:
            res += 1
    return res

def gaschnig(candidate, goal_state, size, db=None):
    res = 0
    candidate = list(candidate)
    goal_state = list(goal_state)
    while candidate != goal_state:
        zi = candidate.index(0)
        if goal_state[zi] != 0:
            sv = goal_state[zi]
            ci = candidate.index(sv)
            candidate[ci], candidate[zi] = candidate[zi], candidate[ci]
        else:
            for i in range(size * size):
                if goal_state[i] != candidate[i]:
                    candidate[i], candidate[zi] = candidate[zi], candidate[i]
                    break
        res += 1
    return res

def manhattan(candidate, goal_state, size, db=None):
    res = 0
    for i in range(size*size):
        if candidate[i] != 0 and candidate[i] != goal_state[i]:
            ci = goal_state.index(candidate[i])
            y = (i // size) - (ci // size)
            x = (i % size) - (ci % size)
            res += abs(y) + abs(x)
    return res

def linear_conflicts(candidate, goal_state, size, db=None):

    def count_conflicts(candidate_row, goal_row, size, ans=0):
        counts = [0 for x in range(size)]
        for i, tile_1 in enumerate(candidate_row):
            if tile_1 in goal_row and tile_1 != 0:
                for j, tile_2 in enumerate(candidate_row):
                    if tile_2 in goal_row and tile_2 != 0:
                        if tile_1 != tile_2:
                            if (goal_row.index(tile_1) > goal_row.index(tile_2)) and i < j:
                                counts[i] += 1
                            if (goal_row.index(tile_1) < goal_row.index(tile_2)) and i > j:
                                counts[i] += 1
        if max(counts) == 0:
            return ans * 2
        else:
            i = counts.index(max(counts))
            candidate_row[i] = -1
            ans += 1
            return count_conflicts(candidate_row, goal_row, size, ans)

    res = manhattan(candidate, goal_state, size)
    candidate_rows = [[] for y in range(size)] 
    candidate_columns = [[] for x in range(size)] 
    goal_rows = [[] for y in range(size)] 
    goal_columns = [[] for x in range(size)] 
    for y in range(size):
        for x in range(size):
            idx = (y * size) + x
            candidate_rows[y].append(candidate[idx])
            candidate_columns[x].append(candidate[idx])
            goal_rows[y].append(goal_state[idx])
            goal_columns[x].append(goal_state[idx])
    for i in range(size):
            res += count_conflicts(candidate_rows[i], goal_rows[i], size)
    for i in range(size):
            res += count_conflicts(candidate_columns[i], goal_columns[i], size)
    return res


def pdb_Query_full8puzzle(state, goal_state, size, db_connection):
    table, pattern = full8puzzle.convertToQueryable(state)
    cost = pdb.queryPDB(table, pattern, db_connection)
    return cost


KV = {
        'hamming':      hamming,
        'gaschnig':     gaschnig,
        'manhattan':    manhattan,
        'lc':    linear_conflicts,
        'pdb_full8puzzle': pdb_Query_full8puzzle,
}