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

#def ida_star_search(init_state, goal_state, size, HEURISTIC, TRANSITION_COST):
#    
#    def search(path, g, bound, evaluated):
#        evaluated += 1
#        node = path[0]
#        f = g + HEURISTIC(node, goal_state, size)
#        if f > bound:
#            return f, evaluated
#        if node == goal_state:
#            return True, evaluated
#        ret = inf
#        children = get_children(node, size)
#        for child in children:
#            if child not in path:
#                path.appendleft(child)
#                t, evaluated = search(path, g + TRANSITION_COST, bound, evaluated)
#                if t is True:
#                    return True, evaluated
#                if t < ret:
#                    ret = t
#                path.popleft()
#        return ret, evaluated
#
#    bound = HEURISTIC(init_state, goal_state, size)
#    path = deque([init_state])
#    evaluated = 0
#    while path:
#        t, evaluated = search(path, 0, bound, evaluated)
#        if t is True:
#            path.reverse()
#            return (True, path, {'space':len(path), 'time':evaluated})
#        elif t is inf:
#            return (False, [], {'space':len(path), 'time':evaluated})
#        else:
#            bound = t


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


#def ida_star_search(init_state, goal_state, size, HEURISTIC, TRANSITION_COST):
#    
#    # outer loop that calls DFS with depth limit = f-cost
#    # and tracks stats
#    goalFound = False
#    nodes_generated = 0
#    max_nodes_in_memory = 0
#    f_limit = HEURISTIC(init_state, goal_state, size)
#    
#    while not goalFound:
#        # call DFS
#        results = DFS_limited(init_state, goal_state, f_limit)
#        goalFound, min_fcost_over_limit, nodes_generated_this_search, max_nodes_in_memory_this_search, path = results
#        
#        # do updates:
#        f_limit = min_fcost_over_limit
#        nodes_generated += nodes_generated_this_search
#        max_nodes_in_memory = max(max_nodes_in_memory, max_nodes_in_memory_this_search)
#        
#        def DFS_limited(f_limit):
#            nodes_generated = 0
#            
#            frontier_stack = deque([{'node':init_state, 'g': 0, 'h': HEURISTIC(init_state, goal_state, size), 'parent': None}])  # LIFO queue / stack
#            
#            node = init_state
#            while node != goal_state:
#                # geneate children
#                children = get_children(init_state, size)
#                nodes_generated += len(children)
#                for child in children:
#                    # now we explore the child in the same way.....
#                    pass
                    
######

#def ida_star_search(init_state, goal_state, size, HEURISTIC, TRANSITION_COST):
#    
#    # outer loop that calls DFS with depth limit = f-cost
#    # and tracks stats
#    goalFound = False
#    nodes_generated = 0
#    max_nodes_in_memory = 0
#    f_limit = HEURISTIC(init_state, goal_state, size)
#    
#    while not goalFound:
#        # call DFS
#        results = DFS_limited(init_state, goal_state, f_limit)
#        goalFound, min_fcost_over_limit, nodes_generated_this_search, max_nodes_in_memory_this_search, path = results
#        
#        # do updates:
#        f_limit = min_fcost_over_limit
#        nodes_generated += nodes_generated_this_search
#        max_nodes_in_memory = max(max_nodes_in_memory, max_nodes_in_memory_this_search)
#        
#        
#def DFS_wrapper(node, goal_state, size, HEURISTIC, TRANSITION_COST, f_limit):
#    nodes_generated = 0
#    max_nodes_in_memory = 0
#    min_fcost_over_limit = inf
#    
#    path = deque([init_state])
    
            
            
            
#        
#        def DFS_limited(f_limit):
#            nodes_generated = 0
#            
#            frontier_stack = deque([{'node':init_state, 'g': 0, 'h': HEURISTIC(init_state, goal_state, size), 'parent': None}])  # LIFO queue / stack
#            
#            node = init_state
#            while node != goal_state:
#                # geneate children
#                children = get_children(init_state, size)
#                nodes_generated += len(children)
#                for child in children:
#                    # now we explore the child in the same way.....
#                    pass
                    
###### 
    
def depth_limited_search(problem, limit=50):
    """[Figure 3.17]"""
    
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None
        
    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)
                    

###

global ida_star_nodes_generated

def ida_star_search(init_state, goal_state, size, HEURISTIC, TRANSITION_COST):
    
    def DoSearch(path, g, f_limit):#, nodes_generated):
        # this really counts nodes explored
#        global nodes_generated
#        nodes_generated += 1
        
        # THIS IS FOR A "LEAF" NODE
        node = path[0]
        f_node = g + HEURISTIC(node, goal_state, size)
        if f_node > f_limit:		# if this node's f-cost exceeds limit, "prune" it and return the f...
            return False, f_node#, nodes_generated
#                return {'goal_found': False, 'min_fcost_over_limit': f}
            # I'm not sure that is correct
        if node == goal_state:
            return True, g#, nodes_generated
        
        # THIS IS FOR NODES THAT CAN BE EXPANDED
        min_fcost_exceeding_limit = inf
        children = get_children(node, size)
        global ida_star_nodes_generated
        ida_star_nodes_generated += len(children)
#        shuffle(children)
        for child in children:
            if child not in path:
                path.appendleft(child)   # add child to LIFO queue "try it on" in the path, so to speak
                result = {}
                #result['goal_found'], result['fcost_over_limit'], nodes_generated
                
                result['goal_found'], result['fcost_over_limit'] = DoSearch(path, g + TRANSITION_COST, f_limit)  # and then "try on" its children
                if result['goal_found'] is True:			# different than " == True" btw
                    return True, g+TRANSITION_COST#, nodes_generated
                if result['fcost_over_limit'] < min_fcost_exceeding_limit:
                    min_fcost_exceeding_limit = result['fcost_over_limit']
                # when that child's subtree is fully explored... pop it back off
                path.popleft()
#            else:
#                nodes_generated -= 1
        
        return False, min_fcost_exceeding_limit#, nodes_generated
#        return {'goal_found': False, 'min_fcost_over_limit': min_fcost_exceeding_limit}

        # searchresults = {'goal_found': True/False, 'min_fcost_over_limit': 5, 'nodes_generated_this_search':xx}
            
    
    
    global ida_star_nodes_generated
    ida_star_nodes_generated = 0
    max_nodes_in_memory = 0
    f_limit = HEURISTIC(init_state, goal_state, size)
    path = deque([init_state])
    
    while path:
#        results = DFS_limited(init_state, goal_state, f_limit)
#        goalFound, min_fcost_over_limit, nodes_generated_this_search, max_nodes_in_memory_this_search, path = results
        
        # searchresults = {'goal_found': True/False, 'min_fcost_over_limit': 5, 'nodes_generated_this_search':xx}
        
        searchresults = {}
        searchresults['goal_found'], searchresults['min_fcost_over_limit']  = DoSearch(path, 0, f_limit)#, nodes_generated)
#        nodes_generated += searchresults['nodes_generated']
        
        if searchresults['goal_found'] is True:
            path.reverse()
            return (True, path, {'space':len(path), 'time':ida_star_nodes_generated})
        elif searchresults['goal_found'] is False and searchresults['min_fcost_over_limit'] is inf:
            return (False, [], {'space':len(path), 'time':ida_star_nodes_generated}) 
        else:
            f_limit = searchresults['min_fcost_over_limit']
            
            
            
            
            