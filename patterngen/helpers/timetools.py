#!/usr/bin/env python3
from time import perf_counter

def pCounter():
	return perf_counter()

def timeDelta(t_start):
	return perf_counter() - t_start

def prettyTime(seconds):
	return sec_to_hours(seconds)

def sec_to_hours(seconds):
# SOURCE: https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
	h=seconds//3600
	m=(seconds%3600)//60
	s=(seconds%3600)%60
	return f'{h} hours {m} mins {s:.2f} sec'