#!/usr/bin/env python3
import json
import pickle
from sys import argv


# DO NOT INCLUDE FILE EXTENSION THX
filename = argv[1].replace('.json', '')

with open(''.join([filename, '.json']), "r") as f:
	jsonDict = json.load(f)

newDict = {}
while jsonDict:
	k, v = jsonDict.popitem()
	k = tuple(eval(k))
	newDict[k] = v

with open(''.join([filename, '.pickle']), "wb") as f:
	pickle.dump(newDict, f)