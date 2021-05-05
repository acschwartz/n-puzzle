#!/usr/bin/env python3
import main

'''
SET UP EACH EXPERIMENT:
1. READING OF INPUT FILE (CONTAINING an initial state)
2. SPECIFY ARGS TO CALL
3. ITERATIVELY CALL main
4. RECORD RESULTS TO JSON FILE
5. name file meaninfully (w datetime?)
'''

if __name__ == '__main__':
	args = ['--str', "(6, 3, 8, 7, 1, 2, 4, 0, 5)", '-f', 'manhattan']
	main.main(args)