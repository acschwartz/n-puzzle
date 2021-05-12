import random
from search import EightPuzzle

def generate_8puzzles_simple(number, filename=None):	# for goal_state = (0,1,2,3,4,5,6,7,8)
	def rand_solvable_state(goal=(0,1,2,3,4,5,6,7,8)):
		solvable = False
		while not solvable:
			init_state = [*range(9)]
			random.shuffle(init_state)
			puzzle = EightPuzzle(tuple(init_state), goal)
			solvable = puzzle.check_solvability(init_state)
		return tuple(init_state)
	
	states = []
	for i in range(0, number):
		isUnique = False
		while not isUnique:
			newstate = rand_solvable_state()
			if newstate not in states:
				isUnique = True
				states.append(newstate)
	
	if not filename:
		filename = f'{number}_random_8puzzles.txt'
	f = open(filename, 'w')
	lines = [" ".join([str(i) for i in state]) for state in states]
	lines = map(lambda l: ''.join([l, '\n']), lines)
	f.writelines(lines)
	f.close()
	return filename