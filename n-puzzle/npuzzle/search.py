from itertools import count
from heapq import heappush, heappop
from collections import deque
from math import inf
from random import shuffle

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
#    shuffle(res)
    return res

global a_star_nodes_generated
a_star_nodes_generated = 0
def a_star_search(init_state, goal_state, size, HEURISTIC, TRANSITION_COST, PDB_CONNECTION):
    global a_star_nodes_generated
    counter = count()
    pqueue = [(0, next(counter), init_state, 0, None)]
            # (f, gen_order,     node,       g, parent)
    frontier = {init_state: (0, HEURISTIC(init_state, goal_state, size, PDB_CONNECTION))}
        # frontier = {node: (g, h)}
    explored = {}
        # explored = {node: parent}
    a_star_nodes_generated = len(frontier)+len(explored)
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
            a_star_nodes_generated = len(frontier) + len(explored)
            return (True, path, {'space':a_star_nodes_generated, 'time':a_star_nodes_generated})
        
        if node in explored:
            continue  #prune
        
        # (else:)
        explored[node] = parent
        # add node to explored set (dict.) with "pointer" to parent from which it was discovered
        del frontier[node]
        
        g_child_thispath = g_node + TRANSITION_COST
        children = get_children(node, size)
        for child in children:
            a_star_nodes_generated += 1
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
                h_child = HEURISTIC(child, goal_state, size, PDB_CONNECTION)
            
            frontier[child] = g_child_thispath, h_child
            heappush(pqueue, (h_child + g_child_thispath, next(counter), child, g_child_thispath, node))
        #\endfor
                
    return (False, [], {'space':a_star_nodes_generated, 'time':a_star_nodes_generated})
                    


'''
Each iteration of IDA* is a complete depth-first search that keeps track of the cost, f(n) = g(n)+h(n), of each node generated. As soon as this cost exceeds some threshold, that branch is cut off, and the search BACKTRACKS to the most recently generated node. The cost threshold starts with the heuristic estimate of the initial state and in each successive iteration is increased to the minimum value that exceeded the previous threshold.
Since at any point IDA* is performing a depth-first search, the memory requirement of the algorithm is linear in the solution depth.
'''
global ida_star_nodes_generated
ida_star_nodes_generated = 0
global ida_star_max_path_length
ida_star_max_path_length = 0
def ida_star_search(init_state, goal_state, size, HEURISTIC, TRANSITION_COST, RANDOM_NODE_ORDER, PDB_CONNECTION):
    
    def DFS(path, g, f_limit):
        global ida_star_nodes_generated
        ida_star_nodes_generated += 1
        # Note: while I would normally consider the above to count "nodes expanded", since the line of code is executed when a node is expanded. However, after some research, it looks that this implementation features backtracking, where only one node is generated at a time (and uses O(m) memory instead of O(bm). Therefore the above count is correct.
        
        global ida_star_max_path_length
        ida_star_max_path_length = max(len(path)-1, ida_star_max_path_length)
        
        node = path[0]
        f_node = g + HEURISTIC(node, goal_state, size, PDB_CONNECTION)
        
        # THIS IS FOR A "LEAF" NODE (i.e. nodes that cannot be expanded)
        if f_node > f_limit:
            return False, f_node
        if node == goal_state:
            return True, g
        
        # THIS IS FOR NODES THAT CAN BE EXPANDED
        min_fcost_exceeding_limit = inf
        children = get_children(node, size)
        if RANDOM_NODE_ORDER: shuffle(children)
        for child in children:
            if child not in path:
                path.appendleft(child)   # add child to LIFO queue "try it on" in the path, so to speak
                result = {}
                result['goal_found'], result['fcost_over_limit'] = DFS(path, g + TRANSITION_COST, f_limit)  # and then "try on" its children
                if result['goal_found'] is True:			# different than " == True" btw
                    return True, g + TRANSITION_COST
                if result['fcost_over_limit'] < min_fcost_exceeding_limit:
                    min_fcost_exceeding_limit = result['fcost_over_limit']
                path.popleft()  # when that child's subtree is fully explored... pop it back off to backtrack up the path
        return False, min_fcost_exceeding_limit
            
    global ida_star_max_path_length
    global ida_star_nodes_generated
    ida_star_max_path_length = 0
    ida_star_nodes_generated = 0
    f_limit = HEURISTIC(init_state, goal_state, size, PDB_CONNECTION)
    
    path = deque([init_state])
    
    while path:
        searchresults = {}
        searchresults['goal_found'], searchresults['min_fcost_over_limit']  = DFS(path, 0, f_limit)
        
        if searchresults['goal_found'] is True:
            path.reverse()
            return (True, path, {'space':ida_star_max_path_length, 'time':ida_star_nodes_generated})
        
        elif searchresults['goal_found'] is False and searchresults['min_fcost_over_limit'] is inf:
            return (False, [], {'space':ida_star_max_path_length, 'time':ida_star_nodes_generated}) 
        else:
            f_limit = searchresults['min_fcost_over_limit']

            