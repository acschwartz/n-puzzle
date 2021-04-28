from itertools import count
from heapq import heappush, heappop
from collections import deque
from math import inf

EMPTY_TILE = 0

def clone_and_swap(data,y0,y1):
    clone = list(data)
    tmp = clone[y0]
    clone[y0] = clone[y1]
    clone[y1] = tmp
    return tuple(clone)

def possible_moves(data, size):     # returns CHILDREN
    res = []
    y = data.index(EMPTY_TILE)
    if y % size > 0:
        left = clone_and_swap(data,y,y-1)
        res.append(left)
    if y % size + 1 < size:
        right = clone_and_swap(data,y,y+1)
        res.append(right)
    if y - size >= 0:
        up = clone_and_swap(data,y,y-size)
        res.append(up)
    if y + size < len(data):
        down = clone_and_swap(data,y,y+size)
        res.append(down)
    return res      # PLEASE SHUFFLE LATER

def ida_star_search(puzzle, goal_state, size, HEURISTIC, TRANSITION_COST):
    def search(path, g, bound, evaluated):
        evaluated += 1
        node = path[0]
        f = g + HEURISTIC(node, goal_state, size)
        if f > bound:
            return f, evaluated
        if node == goal_state:
            return True, evaluated
        ret = inf
        moves = possible_moves(node, size)
        for m in moves:
            if m not in path:
                path.appendleft(m)
                t, evaluated = search(path, g + TRANSITION_COST, bound, evaluated)
                if t is True:
                    return True, evaluated
                if t < ret:
                    ret = t
                path.popleft()
        return ret, evaluated

    bound = HEURISTIC(puzzle, goal_state, size)
    path = deque([puzzle])
    evaluated = 0
    while path:
        t, evaluated = search(path, 0, bound, evaluated)
        if t is True:
            path.reverse()
            return (True, path, {'space':len(path), 'time':evaluated})
        elif t is inf:
            return (False, [], {'space':len(path), 'time':evaluated})
        else:
            bound = t

def a_star_search(puzzle, goal_state, size, HEURISTIC, TRANSITION_COST):
    c = count()
    queue = [(0, next(c), puzzle, 0, None)]
    open_set = {puzzle:None}
    closed_set = {}
    while queue:
        _, _, node, node_g, parent = heappop(queue)
        if node == goal_state:
            steps = [node]
            while parent is not None:
                steps.append(parent)
                parent = closed_set[parent]
            steps.reverse()
            nodes_generated = len(open_set) + len(closed_set)
            return (True, steps, {'space':nodes_generated, 'time':nodes_generated})
        if node in closed_set:
            continue
        closed_set[node] = parent
        del open_set[node]
        tentative_g = node_g + TRANSITION_COST
        moves = possible_moves(node, size)
        for m in moves:
            if m in closed_set:
                continue
            if m in open_set:
                move_g, move_h = open_set[m]
                if move_g <= tentative_g:
                    continue
            else:
                move_h = HEURISTIC(m, goal_state, size)
            open_set[m] = tentative_g, move_h
            heappush(queue, (move_h + tentative_g, next(c), m, tentative_g, node))
    return (False, [], {'space':len(open_set), 'time':len(closed_set)})
