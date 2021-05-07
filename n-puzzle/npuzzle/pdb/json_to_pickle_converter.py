#!/usr/bin/env python3
import json
import pickle
from sys import argv


# DO NOT INCLUDE FILE EXTENSION THX
filename = argv[1].replace('.json', '')

jsonfile = ''.join([filename, '.json'])
with open(jsonfile, "r") as f:
	print ('Loading JSON file:', jsonfile, '.....')
	jsonDict = json.load(f)
	print ('JSON file loaded to dict:', jsonfile)

newDict = {}

print('Converting dictionary keys from string to tuple type ....')
entriesProcessed = 0
while jsonDict:
	k, v = jsonDict.popitem()
	k = tuple(eval(k))
	newDict[k] = v
	
	entriesProcessed += 1
	# Print a progress for every x entries processed
	if entriesProcessed % 10000 == 0:
		print("Entries processed:", entriesProcessed)
print("TOTAL entries processed:", entriesProcessed)
	


picklefile = ''.join([filename, '.pickle'])
with open(picklefile, "wb") as f:
	print ('Writing pickle file:', picklefile)
	pickle.dump(newDict, f)
	print("Done!")