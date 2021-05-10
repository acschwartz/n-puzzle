#!/usr/bin/env python3
##==============================================================================================##
import logging

from helpers.memorytools import *
from helpers.timetools import *

from pdbgen import moves
from pdbgen import patterns

#mmaybe remove later
from pprint import pp as pp


RUN_ID = strftime(f'%y%m%d-%H%M%S')
OUTPUT_DIRECTORY = 'output/'