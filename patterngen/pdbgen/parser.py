#!/usr/bin/env python3

from argparse import ArgumentParser
from pdbgen.patterns import PATTERN_INFO

def initParser():
    parser = ArgumentParser(description='n-puzzle pattern database generator')
#    parser.add_argument('pattern', help='choose a pattern', choices=list(PATTERN_INFO.keys()), default='full8puzzle')
    
    # for now, while working with default only
    parser.add_argument(dest='pattern', help='choose a pattern', choices=list(PATTERN_INFO.keys()))
    return parser

def parseArgs():
    parser = initParser()
    args = parser.parse_args()
    return args.pattern