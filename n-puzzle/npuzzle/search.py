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

def get_children(data, size):     # returns CHILDREN
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
        children = get_children(node, size)
        for child in children:
            if child not in path:
                path.appendleft(child)
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


def a_star_search(init_state, goal_state, size, HEURISTIC, TRANSITION_COST):
    
    counter = count()
    pqueue = [(0, next(counter), init_state, 0, None)]
            # (f, gen_order,     node,       g, parent)
    frontier = {init_state: (0, HEURISTIC(init_state, goal_state, size))}
        # frontier = {node: (g, h)}
    explored = {}
        # explored = {node: parent}

    '''
    There is a frontier set AND a priority queue for this reason:
    https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    '''
    
    while pqueue:
        _, _, node, g_node, parent = heappop(pqueue)
        
        if node == goal_state:
            path = [node]
            while parent is not None:
                path.append(parent)
                parent = explored[parent]
            path.reverse()
            nodes_generated = len(frontier) + len(explored)
            return (True, path, {'space':nodes_generated, 'time':nodes_generated})
        
        if node in explored:
            continue  #prune
        
        # (else:)
        explored[node] = parent
        # add node to explored set (dict.) with "pointer" to parent from which it was discovered
        del frontier[node]
        
        g_child_thispath = g_node + TRANSITION_COST
        children = get_children(node, size)
        for child in children:
            if child in explored:
                #prune
                continue
            if child in frontier:
                # check if this current path to it is better than what we've found so far
                g_child_in_frontier, h_child = frontier[child]
                if g_child_thispath >= g_child_in_frontier:
                    continue #prune this path
                else:
                    pass
            else:
                h_child = HEURISTIC(child, goal_state, size)
            
            frontier[child] = g_child_thispath, h_child
            heappush(pqueue, (h_child + g_child_thispath, next(counter), child, g_child_thispath, node))
        #\endfor
                
    nodes_generated = len(frontier) + len(explored)
    return (False, [], {'space':nodes_generated, 'time':nodes_generated})

