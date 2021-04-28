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

def ida_star_search(init_state, goal_state, size, HEURISTIC, TRANSITION_COST):
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

    bound = HEURISTIC(init_state, goal_state, size)
    path = deque([init_state])
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

def a_star_search(init_state, goal_state, size, HEURISTIC, TRANSITION_COST): # TODO: do we really need to pass in size?
    counter = count()
    queue = [(0, next(counter), init_state, 0, None)]
    # 	(fcost, count (order of expansion? tiebreaker?), curr node, g curr node, parent)   ? i think
    open_set = {init_state:None}
    # 'interesting' choice to have open set AND priority queue
    closed_set = {}
    while queue:
        _, _, node, node_g, parent = heappop(queue)    # _ throws away value 
        if node == goal_state:
            path = [node]
            while parent is not None:
                path.append(parent)
                parent = closed_set[parent]
            path.reverse()
            nodes_generated = len(open_set) + len(closed_set)
            return (True, path, {'space':nodes_generated, 'time':nodes_generated})
        if node in closed_set:
            continue   # prune
        closed_set[node] = parent # add node to explored set (dictionary) with a "pointer" to its paren
        del open_set[node]
        child_g_thispath = node_g + TRANSITION_COST
        children = possible_moves(node, size)
        for child in children:
            if child in closed_set:
                continue # prune
            if child in open_set: # child in frontier --> check if this path is better
                child_g_in_frontier, child_h = open_set[child] # get what's in the frontier
                if child_g_thispath >= child_g_in_frontier:
                    continue
            else:
                child_h = HEURISTIC(child, goal_state, size)
            open_set[child] = child_g_thispath, child_h
            heappush(queue, (child_h + child_g_thispath, next(counter), child, child_g_thispath, node))
    nodes_generated = len(open_set) + len(closed_set)
    return (False, [], {'space':nodes_generated, 'time':nodes_generated})
