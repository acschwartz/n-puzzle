#!/usr/bin/env python3

from collections import deque
from patterngen.dbtools import db
from patterngen.pdbgen.moves import *
from sqlite3 import IntegrityError
import fringe15encoding

class Fringe15Node:
	__slots__: [pattern, cost]
	def __init__(self, pattern, cost=0):
		self.pattern = pattern
		self.cost = cost
	
	