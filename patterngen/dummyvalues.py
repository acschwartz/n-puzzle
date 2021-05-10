#!/usr/bin/env python3

# !!!!!!!!!!!!!!!!!
#DEBUG = False
# !!!!!!!!!!!!!!!!

#if DEBUG: from pprint import pp

#if DEBUG: n_entries = 256
#else:
#	n_entries = 10**8
	# hex(935124720) = '0x37bcdef0'  (index of empty tile is stored last so doesn't get cut off)



###==============================================================================================##
## e.g.  935124720  (representing '0x37bcdef0')
def ints_repr_hexvalues(n_entries, max_cost=100):
	first_key = 935124720
	ints_repr_hexvalues = {}
	for n in range(n_entries):
		cost = n % max_cost
		next_key = first_key + n
		ints_repr_hexvalues[next_key] = cost
	return ints_repr_hexvalues

#if DEBUG: pp(ints_repr_hexvalues)
###==============================================================================================##


###==============================================================================================##
## e.g. '37bcdef0'  (representing '0x37bcdef0')
def hexstrings(n_entries, max_cost=100):
	first_key = 935124720
	hexstrings = {}
	for n in range(n_entries):
		cost = n % max_cost
		next_key = hex(first_key + n)[2:]	# cuts off the leading '0x' in the string
		hexstrings[next_key] = cost
	return hexstrings

#if DEBUG: pp(hexstrings)
###==============================================================================================##

def hexstr_to_int_tuple(hexstr):
	if hexstr.startswith('0x'):
		hexstr = hexstr[2:]
		
	lst = [int(hexstr[i], 16) for i in range(len(hexstr))]
	return tuple(lst)

#if DEBUG: pp(hexstr_to_int_tuple(hex(first_key)))

###==============================================================================================##
## e.g. tuple pickled into a bytestring:
## b'\x80\x04\x95\x14\x00\x00\x00\x00\x00\x00\x00(K\x03K\x07K\x0bK\x0cK\rK\x0eK\x0fK\x00t\x94.'
## representing (3, 7, 11, 12, 13, 14, 15, 0) representing '0x37bcdef0'
def tuples_len8_pickled(n_entries, max_cost=100):
	import pickle
	tuples_len8_pickled = {}
	first_key = 935124720
	for n in range(n_entries):
		cost = n % max_cost
		next_key = pickle.dumps(hexstr_to_int_tuple(hex(first_key + n)))
		tuples_len8_pickled[next_key] = cost
	return tuples_len8_pickled

#if DEBUG: pp(tuples_len8_pickled)
###==============================================================================================##

###==============================================================================================##
## e.g. '3,7,11,12,13,14,15,0'  (representing '0x37bcdef0')
def string_repr_tuples_of_ints (n_entries, max_cost=100):
	string_repr_tuples_of_ints = {}
	first_key = 935124720
	for n in range(n_entries):
		cost = n % max_cost
		s = str(hexstr_to_int_tuple(hex(first_key + n)))
		next_key = ''.join((filter(lambda char: char not in ['(', ')', '[', ']', ' '], s)))
		string_repr_tuples_of_ints[next_key] = cost
	return string_repr_tuples_of_ints 
	
#if DEBUG: pp(string_repr_tuples_of_ints)

###==============================================================================================##
## e.g. '(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)' representing the whole puzzle
def string_repr_tuples_whole_puzzle(n_entries, max_cost=100):
	sixteenDigitHex = int(0x123456789abcdeff)
	string_repr_tuples_whole_puzzle = {}
	for n in range(n_entries):
		cost = n % max_cost
		next_key = str(hexstr_to_int_tuple(hex(sixteenDigitHex + n)))
		string_repr_tuples_whole_puzzle[next_key] = cost
	return string_repr_tuples_whole_puzzle
		
#if DEBUG: pp(string_repr_tuples_whole_puzzle)
##==============================================================================================##